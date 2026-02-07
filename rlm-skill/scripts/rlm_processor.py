#!/usr/bin/env python3
"""
rlm_processor.py - Full Recursive Language Model processing pipeline.

This implements the complete RLM workflow from the paper arXiv:2512.24601:
1. Load context as external variable (file) - AUTO-DETECTS file type!
2. Analyze and chunk the context
3. Process each chunk with sub-LLM calls
4. Aggregate results into final answer

Supported file types:
    - PDF (.pdf)
    - Word documents (.docx)
    - Text files (.txt, .md, .rst)
    - Code files (.py, .js, .java, .c, .go, etc.)
    - Data files (.json, .xml, .csv, .yaml)
    - HTML files (.html)
    - Archives (.zip, .tar.gz) - extracts all text files

Usage:
    python rlm_processor.py <context_file> "Your query"
    python rlm_processor.py document.pdf "Summarize the main points"
    python rlm_processor.py codebase.zip "Find security issues" --fast

Requires:
    ANTHROPIC_API_KEY environment variable

Reference: Zhang, Kraska, Khattab - "Recursive Language Models" (MIT CSAIL, 2025)
"""

import os
import sys
import json
import argparse
import re
from typing import List, Optional, Tuple
from pathlib import Path

# Import file converter for auto-detection
try:
    from file_converter import convert_to_text, detect_file_type, get_file_info
    FILE_CONVERTER_AVAILABLE = True
except ImportError:
    FILE_CONVERTER_AVAILABLE = False

# Import from sibling module
try:
    from rlm_query import llm_query, llm_query_fast, DEFAULT_MODEL, FAST_MODEL, load_api_key
except ImportError:
    # If running directly, define inline with Windows/.claude support
    import subprocess
    
    DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
    FAST_MODEL = "claude-haiku-4-5-20251001"
    
    def load_api_key():
        """Load API key from env var or .claude folder."""
        # 1. Environment variable
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if api_key:
            return api_key.strip()
        
        # 2. .claude folder
        if sys.platform == 'win32':
            base = os.environ.get('USERPROFILE', os.path.expanduser('~'))
        else:
            base = os.path.expanduser('~')
        
        claude_dir = Path(base) / '.claude'
        
        # Check api_key.txt
        api_key_file = claude_dir / 'api_key.txt'
        if api_key_file.exists():
            try:
                return api_key_file.read_text().strip()
            except:
                pass
        
        # Check config.json
        config_file = claude_dir / 'config.json'
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text())
                return config.get('api_key', '').strip()
            except:
                pass
        
        return None
    
    def llm_query(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 4096) -> str:
        api_key = load_api_key()
        if not api_key:
            if sys.platform == 'win32':
                claude_dir = Path(os.environ.get('USERPROFILE', '')) / '.claude'
            else:
                claude_dir = Path.home() / '.claude'
            raise ValueError(
                f"API key not found. Create: {claude_dir / 'api_key.txt'}\n"
                f"Or set ANTHROPIC_API_KEY environment variable."
            )
        
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        import tempfile
        payload_json = json.dumps(payload)
        tmp_file = None
        try:
            if len(payload_json) > 20000 or sys.platform == 'win32':
                tmp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
                tmp_file.write(payload_json)
                tmp_file.close()
                data_arg = f'@{tmp_file.name}'
            else:
                data_arg = payload_json
            cmd = [
                'curl', '-s', 'https://api.anthropic.com/v1/messages',
                '-H', 'Content-Type: application/json',
                '-H', f'x-api-key: {api_key}',
                '-H', 'anthropic-version: 2023-06-01',
                '-d', data_arg
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding='utf-8', errors='replace',
                shell=(sys.platform == 'win32')
            )
        finally:
            if tmp_file and os.path.exists(tmp_file.name):
                os.unlink(tmp_file.name)
        response = json.loads(result.stdout)
        
        if 'content' in response:
            return response['content'][0]['text']
        raise Exception(f"API error: {response}")
    
    def llm_query_fast(prompt: str, **kwargs) -> str:
        return llm_query(prompt, model=FAST_MODEL, **kwargs)


# ============================================================================
# Chunking Strategies
# ============================================================================

def chunk_by_chars(content: str, chunk_size: int = 40000, overlap: int = 500) -> List[str]:
    """Chunk by character count with optional overlap."""
    chunks = []
    start = 0
    while start < len(content):
        end = min(start + chunk_size, len(content))
        chunks.append(content[start:end])
        start = end - overlap if overlap and end < len(content) else end
    return chunks


def chunk_by_lines(content: str, lines_per_chunk: int = 500) -> List[str]:
    """Chunk by line count."""
    lines = content.split('\n')
    chunks = []
    for i in range(0, len(lines), lines_per_chunk):
        chunks.append('\n'.join(lines[i:i + lines_per_chunk]))
    return chunks


def chunk_by_separator(content: str, separator: str = '\n---\n') -> List[str]:
    """Chunk by document separator."""
    chunks = content.split(separator)
    return [c.strip() for c in chunks if c.strip()]


def chunk_by_regex(content: str, pattern: str) -> List[str]:
    """Chunk by regex pattern matches."""
    parts = re.split(pattern, content)
    return [p.strip() for p in parts if p.strip()]


def auto_chunk(content: str, target_chunk_size: int = 40000) -> Tuple[List[str], str]:
    """
    Automatically detect the best chunking strategy.
    
    Returns:
        Tuple of (chunks, strategy_name)
    """
    # Detect structure
    doc_seps = len(re.findall(r'\n---+\n|\n===+\n', content))
    json_objs = len(re.findall(r'^\s*\{', content, re.MULTILINE))
    md_headers = len(re.findall(r'^#+\s+', content, re.MULTILINE))
    
    total_chars = len(content)
    total_lines = content.count('\n')
    
    # Choose strategy
    if doc_seps > 5 and total_chars / doc_seps < target_chunk_size * 2:
        return chunk_by_separator(content, '\n---'), 'document_separator'
    
    if md_headers > 10:
        # Chunk at H1/H2 headers
        chunks = chunk_by_regex(content, r'\n(?=#{1,2}\s+)')
        if all(len(c) < target_chunk_size * 2 for c in chunks):
            return chunks, 'markdown_headers'
    
    if total_lines > 100 and total_chars / total_lines < 200:
        # Short lines = structured data, chunk by lines
        lines_per_chunk = max(100, target_chunk_size // 100)
        return chunk_by_lines(content, lines_per_chunk), 'line_count'
    
    # Default: character-based chunking
    return chunk_by_chars(content, target_chunk_size), 'character_count'


# ============================================================================
# RLM Processing Pipeline
# ============================================================================

def filter_relevant_chunks(
    chunks: List[str], 
    query: str, 
    keywords: Optional[List[str]] = None
) -> List[Tuple[int, str]]:
    """
    Pre-filter chunks using keyword matching (RLM Pattern 1: Filter First).
    
    Returns list of (original_index, chunk) tuples for relevant chunks.
    """
    if not keywords:
        # Extract potential keywords from query
        query_words = re.findall(r'\b\w{4,}\b', query.lower())
        # Remove common words
        stopwords = {'what', 'when', 'where', 'which', 'about', 'this', 'that', 
                    'with', 'from', 'have', 'does', 'find', 'list', 'show'}
        keywords = [w for w in query_words if w not in stopwords]
    
    if not keywords:
        # No filtering possible, return all
        return [(i, c) for i, c in enumerate(chunks)]
    
    # Build regex pattern
    pattern = '|'.join(re.escape(kw) for kw in keywords)
    
    relevant = []
    for i, chunk in enumerate(chunks):
        if re.search(pattern, chunk, re.IGNORECASE):
            relevant.append((i, chunk))
    
    # If filtering removed too much, return all
    if len(relevant) < len(chunks) * 0.1:
        return [(i, c) for i, c in enumerate(chunks)]
    
    return relevant


def process_chunk(
    chunk: str, 
    chunk_index: int, 
    total_chunks: int, 
    query: str,
    fast_model: bool = False
) -> Optional[str]:
    """
    Process a single chunk with sub-LLM call.
    
    Returns None if no relevant info found.
    """
    chunk_prompt = f"""You are analyzing section {chunk_index + 1} of {total_chunks} of a large document.

ORIGINAL QUERY: {query}

DOCUMENT SECTION:
---
{chunk}
---

INSTRUCTIONS:
1. Extract any information from this section relevant to answering the query
2. If nothing relevant is found, respond with exactly: NO_RELEVANT_INFO
3. Be concise but preserve important details
4. Note any partial information that might be useful combined with other sections

YOUR ANALYSIS:"""

    query_fn = llm_query_fast if fast_model else llm_query
    
    try:
        result = query_fn(chunk_prompt, max_tokens=2048)
        
        if "NO_RELEVANT_INFO" in result:
            return None
        
        return result.strip()
        
    except Exception as e:
        print(f"  ⚠️ Error processing chunk {chunk_index + 1}: {e}", file=sys.stderr)
        return None


def aggregate_results(
    results: List[Tuple[int, str]], 
    query: str,
    fast_model: bool = False
) -> str:
    """
    Aggregate chunk results into final answer.
    
    Uses hierarchical aggregation for large result sets.
    """
    if not results:
        return "No relevant information found in the provided context for this query."
    
    # Format results with section references
    formatted = []
    for chunk_idx, result in results:
        formatted.append(f"[Section {chunk_idx + 1}]\n{result}")
    
    combined = "\n\n".join(formatted)
    
    # Check if we need hierarchical aggregation
    if len(combined) > 50000:
        print("  📊 Large result set - using hierarchical aggregation...")
        
        # Split results in half and aggregate recursively
        mid = len(results) // 2
        
        left_agg = aggregate_results(results[:mid], "Summarize these findings", fast_model)
        right_agg = aggregate_results(results[mid:], "Summarize these findings", fast_model)
        
        combined = f"Summary Part 1:\n{left_agg}\n\nSummary Part 2:\n{right_agg}"
    
    aggregation_prompt = f"""You analyzed a large document in sections. Here are the relevant findings:

{combined}

---

ORIGINAL QUERY: {query}

INSTRUCTIONS:
1. Synthesize all findings into a comprehensive answer
2. Resolve any contradictions between sections
3. Cite specific sections when relevant (e.g., "According to Section 3...")
4. If the query cannot be fully answered, explain what's missing

YOUR FINAL ANSWER:"""

    query_fn = llm_query_fast if fast_model else llm_query
    
    try:
        return query_fn(aggregation_prompt, max_tokens=4096)
    except Exception as e:
        return f"Error during aggregation: {e}\n\nRaw findings:\n{combined[:5000]}"


def rlm_process(
    context_file: str,
    query: str,
    chunk_size: int = 40000,
    fast_model: bool = False,
    filter_chunks: bool = True,
    verbose: bool = True
) -> str:
    """
    Main RLM processing pipeline.
    
    Args:
        context_file: Path to file containing long context (any supported format)
        query: User's query about the context
        chunk_size: Target chunk size in characters
        fast_model: Use faster/cheaper model for chunk processing
        filter_chunks: Pre-filter chunks by keywords
        verbose: Print progress information
        
    Returns:
        Final aggregated answer
    """
    def log(msg):
        if verbose:
            print(msg, file=sys.stderr)
    
    # Step 1: Load context with auto-detection
    log(f"[RLM] Loading context from {context_file}...")
    
    # Detect file type and convert if needed
    if FILE_CONVERTER_AVAILABLE:
        file_type = detect_file_type(context_file)
        log(f"[RLM] Detected file type: {file_type}")
        
        if file_type in ('pdf', 'docx', 'html', 'archive'):
            log(f"[RLM] Converting {file_type} to text...")
            try:
                content = convert_to_text(context_file)
                log(f"[RLM] Successfully extracted text from {file_type}")
            except Exception as e:
                log(f"[RLM] Warning: Conversion failed ({e}), trying direct read...")
                with open(context_file, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
        else:
            # Text-based file, read directly
            content = convert_to_text(context_file)
    else:
        # Fallback: try direct read
        ext = Path(context_file).suffix.lower()
        if ext == '.pdf':
            log("[RLM] PDF detected but file_converter not available. Attempting pdftotext...")
            import subprocess
            result = subprocess.run(['pdftotext', '-layout', context_file, '-'],
                                  capture_output=True, text=True,
                                  encoding='utf-8', errors='replace')
            if result.returncode == 0:
                content = result.stdout
            else:
                raise RuntimeError(f"Cannot read PDF. Install pdfplumber: pip install pdfplumber")
        elif ext == '.docx':
            raise RuntimeError("Cannot read .docx. Run: pip install python-docx --break-system-packages")
        else:
            with open(context_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
    
    total_chars = len(content)
    total_lines = content.count('\n')
    est_tokens = total_chars // 4
    
    log(f"[RLM] Context: {total_chars:,} chars, {total_lines:,} lines (~{est_tokens:,} tokens)")
    
    # Step 2: Auto-chunk
    log("[RLM] Analyzing structure and chunking...")
    chunks, strategy = auto_chunk(content, chunk_size)
    log(f"[RLM] Strategy: {strategy} -> {len(chunks)} chunks")
    
    # Step 3: Filter (optional)
    if filter_chunks and len(chunks) > 3:
        log("[RLM] Pre-filtering chunks by relevance...")
        indexed_chunks = filter_relevant_chunks(chunks, query)
        log(f"[RLM] Filtered: {len(chunks)} -> {len(indexed_chunks)} potentially relevant chunks")
    else:
        indexed_chunks = [(i, c) for i, c in enumerate(chunks)]
    
    # Step 4: Process chunks
    log(f"[RLM] Processing {len(indexed_chunks)} chunks...")
    
    results = []
    for i, (orig_idx, chunk) in enumerate(indexed_chunks):
        log(f"[RLM] Processing chunk {i+1}/{len(indexed_chunks)} (original #{orig_idx+1})...")
        
        result = process_chunk(
            chunk, orig_idx, len(chunks), query, fast_model
        )
        
        if result:
            results.append((orig_idx, result))
            log(f"  [+] Found relevant info")
        else:
            log(f"  [-] No relevant info")
    
    log(f"[RLM] Found relevant info in {len(results)}/{len(indexed_chunks)} chunks")
    
    # Step 5: Aggregate
    log("[RLM] Aggregating results...")
    final_answer = aggregate_results(results, query, fast_model)
    
    log("[RLM] Processing complete!")
    
    return final_answer


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Process long contexts using Recursive Language Model approach',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic usage
    python rlm_processor.py document.txt "What are the main conclusions?"
    
    # Process a codebase
    python rlm_processor.py codebase.txt "Find potential security issues" --fast
    
    # Smaller chunks for denser content
    python rlm_processor.py data.txt "Count entries by category" --chunk-size 20000
    
    # Skip pre-filtering for comprehensive analysis
    python rlm_processor.py report.txt "Summarize everything" --no-filter

Reference: Zhang, Kraska, Khattab - "Recursive Language Models" (arXiv:2512.24601)
        """
    )
    
    parser.add_argument('context_file', help='Path to file containing long context')
    parser.add_argument('query', help='Query about the context')
    parser.add_argument('--chunk-size', '-c', type=int, default=40000,
                        help='Target chunk size in characters (default: 40000)')
    parser.add_argument('--fast', '-f', action='store_true',
                        help='Use faster/cheaper model for chunk processing')
    parser.add_argument('--no-filter', action='store_true',
                        help='Disable keyword-based chunk pre-filtering')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress progress output')
    parser.add_argument('--output', '-o', help='Write result to file')
    
    args = parser.parse_args()
    
    # Validate input
    if not Path(args.context_file).exists():
        print(f"Error: File not found: {args.context_file}", file=sys.stderr)
        sys.exit(1)
    
    # Check API key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY environment variable required", file=sys.stderr)
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = rlm_process(
            context_file=args.context_file,
            query=args.query,
            chunk_size=args.chunk_size,
            fast_model=args.fast,
            filter_chunks=not args.no_filter,
            verbose=not args.quiet
        )
        
        # Output
        print("\n" + "=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)
        print(result)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\n[Saved to {args.output}]", file=sys.stderr)
            
    except KeyboardInterrupt:
        print("\n[Interrupted]", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
