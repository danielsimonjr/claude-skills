#!/usr/bin/env python3
"""
directory_processor.py - Process entire directories through the RLM pipeline.

Recursively discovers files in a directory, converts them to text, and processes
them through the Recursive Language Model pipeline for analysis.

Two modes:
    Combined (default):  Concatenate all files, process as single RLM stream.
                         Best for cross-file queries ("explain the architecture").
    Per-file (--per-file): Process each file independently, then aggregate.
                           Best for file-scoped queries ("find bugs in each file").

Supported file types: PDF, DOCX, HTML, JSON, CSV, YAML, XML, archives,
                      and 30+ code/text extensions (auto-detected via file_converter).

Usage:
    python directory_processor.py ./project "Explain the architecture"
    python directory_processor.py ./src "Find security issues" --per-file --fast
    python directory_processor.py ./project "Summarize" --include "*.py,*.js"

Requires:
    ANTHROPIC_API_KEY (env var or ~/.claude/api_key.txt)

Reference: Zhang, Kraska, Khattab - "Recursive Language Models" (arXiv:2512.24601)
"""

import os
import sys
import json
import argparse
import fnmatch
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict

# ============================================================================
# Path setup and imports
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import file converter
try:
    from file_converter import convert_to_text, detect_file_type, format_size
    FILE_CONVERTER_AVAILABLE = True
except ImportError:
    FILE_CONVERTER_AVAILABLE = False

    def detect_file_type(filepath):
        ext = Path(filepath).suffix.lower()
        text_exts = {'.txt', '.md', '.rst', '.py', '.js', '.ts', '.java', '.c',
                     '.cpp', '.go', '.rs', '.rb', '.sh', '.json', '.yaml', '.yml',
                     '.xml', '.csv', '.html', '.css', '.toml', '.cfg', '.ini'}
        if ext in text_exts:
            return 'text'
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.read(1000)
            return 'text'
        except (UnicodeDecodeError, Exception):
            return 'binary'

    def convert_to_text(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()

    def format_size(size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

# Import rlm_processor sub-functions
try:
    from rlm_processor import (
        auto_chunk, filter_relevant_chunks, process_chunk, aggregate_results
    )
    RLM_PROCESSOR_AVAILABLE = True
except ImportError:
    RLM_PROCESSOR_AVAILABLE = False

# Import rlm_query (for API key check and fallback LLM calls)
try:
    from rlm_query import llm_query, llm_query_fast, load_api_key
except ImportError:
    import subprocess

    def load_api_key():
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if api_key:
            return api_key.strip()
        if sys.platform == 'win32':
            base = os.environ.get('USERPROFILE', os.path.expanduser('~'))
        else:
            base = os.path.expanduser('~')
        claude_dir = Path(base) / '.claude'
        api_key_file = claude_dir / 'api_key.txt'
        if api_key_file.exists():
            try:
                return api_key_file.read_text().strip()
            except Exception:
                pass
        config_file = claude_dir / 'config.json'
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text())
                return config.get('api_key', '').strip()
            except Exception:
                pass
        return None

    def llm_query(prompt, model="claude-sonnet-4-5-20250929", max_tokens=4096):
        api_key = load_api_key()
        if not api_key:
            raise ValueError("API key not found.")
        payload = {"model": model, "max_tokens": max_tokens,
                   "messages": [{"role": "user", "content": prompt}]}
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
            cmd = ['curl', '-s', 'https://api.anthropic.com/v1/messages',
                   '-H', 'Content-Type: application/json',
                   '-H', f'x-api-key: {api_key}',
                   '-H', 'anthropic-version: 2023-06-01',
                   '-d', data_arg]
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding='utf-8', errors='replace',
                shell=(sys.platform == 'win32'))
        finally:
            if tmp_file and os.path.exists(tmp_file.name):
                os.unlink(tmp_file.name)
        response = json.loads(result.stdout)
        if 'content' in response:
            return response['content'][0]['text']
        raise Exception(f"API error: {response}")

    def llm_query_fast(prompt, **kwargs):
        return llm_query(prompt, model="claude-haiku-4-5-20251001", **kwargs)


# ============================================================================
# Constants
# ============================================================================

EXCLUDED_DIRS = {
    '.git', 'node_modules', '__pycache__', 'venv', '.venv',
    'dist', 'build', '.next', '.cache', '.tox', '.mypy_cache',
    '.pytest_cache', '.eggs', '.svn', '.hg', '.idea', '.vscode',
}

EXCLUDED_FILE_PATTERNS = [
    '*.pyc', '*.pyo', '*.so', '*.dll', '*.exe', '*.bin',
    '*.o', '*.obj', '*.class', '*.jar',
    '*.png', '*.jpg', '*.jpeg', '*.gif', '*.ico', '*.svg', '*.bmp', '*.webp',
    '*.woff', '*.woff2', '*.ttf', '*.eot',
    '*.mp3', '*.mp4', '*.avi', '*.mov', '*.wav', '*.flac',
    '*.zip', '*.tar', '*.gz', '*.rar', '*.7z',
    '*.lock', '*.map',
    '*.pdf',  # PDFs handled separately if file_converter available
]

FILE_ORDER_PRIORITY = {
    'readme': 0,
    'doc': 1,
    'source': 2,
    'test': 3,
    'config': 4,
    'data': 5,
    'other': 6,
}

DEFAULT_MAX_FILE_SIZE = 1_000_000  # 1MB
DEFAULT_CHUNK_SIZE = 40000


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class FileEntry:
    """A discovered file with metadata."""
    abs_path: str
    rel_path: str
    size_bytes: int
    file_type: str
    priority_group: str
    content: Optional[str] = None
    error: Optional[str] = None


# ============================================================================
# File discovery and classification
# ============================================================================

def _classify_priority(rel_path: str, file_type: str) -> str:
    """Classify a file into a priority group for ordering."""
    name = Path(rel_path).name.lower()
    stem = Path(rel_path).stem.lower()
    ext = Path(rel_path).suffix.lower()
    parts = rel_path.replace('\\', '/').lower()

    # README and similar top-level docs
    if stem in ('readme', 'changelog', 'contributing', 'license', 'authors'):
        return 'readme'

    # Documentation
    if '/docs/' in parts or '/doc/' in parts or ext in ('.md', '.rst', '.txt'):
        if stem.startswith('readme'):
            return 'readme'
        return 'doc'

    # Tests
    if ('/test/' in parts or '/tests/' in parts or '/spec/' in parts or
            '/specs/' in parts or '__tests__' in parts or
            name.startswith('test_') or name.endswith('_test' + ext) or
            '.test.' in name or '.spec.' in name):
        return 'test'

    # Source code
    if file_type == 'code':
        return 'source'

    # Configuration
    config_names = {'package.json', 'tsconfig.json', 'pyproject.toml',
                    'setup.py', 'setup.cfg', 'makefile', 'dockerfile',
                    'docker-compose.yml', 'docker-compose.yaml',
                    '.eslintrc', '.prettierrc', 'jest.config.js',
                    'webpack.config.js', 'vite.config.js', 'cargo.toml'}
    config_exts = {'.toml', '.cfg', '.ini', '.env'}
    if name in config_names or ext in config_exts:
        return 'config'

    # Data files
    if file_type in ('csv', 'json', 'yaml', 'xml'):
        return 'data'

    return 'other'


def discover_files(
    directory: str,
    include_patterns: List[str] = None,
    exclude_patterns: List[str] = None,
    max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    recursive: bool = True,
    verbose: bool = True
) -> Tuple[List[FileEntry], Dict[str, int]]:
    """
    Discover and filter files in a directory.

    Returns:
        Tuple of (sorted file entries, skip counts dict)
    """
    directory = os.path.abspath(directory)
    files = []
    skip_counts = {'binary': 0, 'too_large': 0, 'excluded': 0, 'permission': 0}

    # Handle PDF separately: include if file_converter available
    excluded_patterns = list(EXCLUDED_FILE_PATTERNS)
    if FILE_CONVERTER_AVAILABLE:
        excluded_patterns.remove('*.pdf')

    if recursive:
        walker = os.walk(directory)
    else:
        # Single-level: yield just the top directory
        try:
            entries = os.listdir(directory)
            dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
            fnames = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
            walker = [(directory, dirs, fnames)]
        except PermissionError:
            skip_counts['permission'] += 1
            return files, skip_counts

    for root, dirs, filenames in walker:
        # Prune excluded directories (modifies walk in-place)
        dirs[:] = [d for d in sorted(dirs)
                   if not d.startswith('.') and d not in EXCLUDED_DIRS]

        for fname in sorted(filenames):
            if fname.startswith('.'):
                continue

            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, directory)

            # Check built-in exclusions
            if any(fnmatch.fnmatch(fname.lower(), pat) for pat in excluded_patterns):
                skip_counts['excluded'] += 1
                continue

            # Check user include patterns (must match at least one)
            if include_patterns:
                if not any(fnmatch.fnmatch(fname.lower(), pat.lower())
                           for pat in include_patterns):
                    continue

            # Check user exclude patterns (must not match any)
            if exclude_patterns:
                if any(fnmatch.fnmatch(fname.lower(), pat.lower())
                       for pat in exclude_patterns):
                    skip_counts['excluded'] += 1
                    continue

            # Check file size
            try:
                size = os.path.getsize(filepath)
            except OSError:
                skip_counts['permission'] += 1
                continue

            if size > max_file_size:
                skip_counts['too_large'] += 1
                continue

            if size == 0:
                continue

            # Detect file type
            try:
                ftype = detect_file_type(filepath)
            except Exception:
                ftype = 'unknown'

            if ftype in ('binary', 'unknown'):
                skip_counts['binary'] += 1
                continue

            priority = _classify_priority(rel_path, ftype)
            files.append(FileEntry(
                abs_path=filepath,
                rel_path=rel_path,
                size_bytes=size,
                file_type=ftype,
                priority_group=priority,
            ))

    # Sort by priority group then path
    files.sort(key=lambda f: (FILE_ORDER_PRIORITY.get(f.priority_group, 6), f.rel_path))

    return files, skip_counts


def load_file_contents(files: List[FileEntry], verbose: bool = True) -> int:
    """
    Load text content for each FileEntry using file_converter.

    Returns total content size in characters.
    """
    total_size = 0
    for entry in files:
        try:
            entry.content = convert_to_text(entry.abs_path)
            total_size += len(entry.content)
        except Exception as e:
            entry.error = str(e)
            if verbose:
                print(f"  [DIR] Warning: {entry.rel_path}: {e}", file=sys.stderr)
    return total_size


# ============================================================================
# Manifest generation
# ============================================================================

def generate_manifest(directory: str, files: List[FileEntry], total_content_size: int) -> str:
    """Generate a tree-format directory manifest for LLM context."""
    dir_name = Path(directory).name or directory

    # Count unique directories
    dirs_seen = set()
    for f in files:
        parts = Path(f.rel_path).parent.parts
        for i in range(len(parts)):
            dirs_seen.add(os.path.join(*parts[:i + 1]))

    lines = [
        f"=== DIRECTORY MANIFEST ===",
        f"{dir_name}/ ({len(files)} files, {len(dirs_seen)} dirs, "
        f"{format_size(total_content_size)} text content)",
    ]

    # Build tree lines
    for entry in files:
        rel = entry.rel_path.replace('\\', '/')
        depth = rel.count('/')
        indent = '  ' * (depth + 1)
        fname = Path(rel).name
        status = f"[{entry.file_type}]"
        size = format_size(entry.size_bytes)
        if entry.error:
            status = f"[error]"
        lines.append(f"{indent}{fname:<32s} {status:<10s} {size:>8s}")

    lines.append("=== END MANIFEST ===")
    return '\n'.join(lines)


# ============================================================================
# Processing modes
# ============================================================================

def build_combined_content(files: List[FileEntry], manifest: str) -> str:
    """Concatenate all file contents with manifest preamble and file markers."""
    parts = [manifest, ""]
    for entry in files:
        if entry.content is not None:
            parts.append(f"=== FILE: {entry.rel_path} ===")
            parts.append(entry.content)
            parts.append("")
    return '\n'.join(parts)


def process_combined(
    combined_content: str,
    query: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    fast_model: bool = False,
    verbose: bool = True
) -> str:
    """Process combined content through the RLM pipeline."""
    if not RLM_PROCESSOR_AVAILABLE:
        raise RuntimeError(
            "rlm_processor.py not found. Ensure it's in the same directory as this script."
        )

    def log(msg):
        if verbose:
            print(msg, file=sys.stderr)

    log(f"[DIR] Combined content: {len(combined_content):,} chars "
        f"(~{len(combined_content) // 4:,} tokens)")

    # Chunk
    chunks, strategy = auto_chunk(combined_content, chunk_size)
    log(f"[DIR] Chunking strategy: {strategy} -> {len(chunks)} chunks")

    # Filter
    if len(chunks) > 3:
        indexed_chunks = filter_relevant_chunks(chunks, query)
        log(f"[DIR] Pre-filtered: {len(chunks)} -> {len(indexed_chunks)} chunks")
    else:
        indexed_chunks = [(i, c) for i, c in enumerate(chunks)]

    # Process chunks
    results = []
    for i, (orig_idx, chunk) in enumerate(indexed_chunks):
        log(f"[DIR] Processing chunk {i + 1}/{len(indexed_chunks)}...")
        result = process_chunk(chunk, orig_idx, len(chunks), query, fast_model)
        if result:
            results.append((orig_idx, result))
            log(f"  {chr(10003)} Found relevant info")
        else:
            log(f"  {chr(9675)} No relevant info")

    log(f"[DIR] Relevant chunks: {len(results)}/{len(indexed_chunks)}")

    # Aggregate
    log("[DIR] Aggregating results...")
    return aggregate_results(results, query, fast_model)


def process_per_file(
    files: List[FileEntry],
    query: str,
    manifest: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    fast_model: bool = False,
    verbose: bool = True
) -> Tuple[str, List[Dict]]:
    """
    Process each file independently, then aggregate.

    Returns (final_answer, per_file_results_list).
    """
    if not RLM_PROCESSOR_AVAILABLE:
        raise RuntimeError(
            "rlm_processor.py not found. Ensure it's in the same directory as this script."
        )

    def log(msg):
        if verbose:
            print(msg, file=sys.stderr)

    per_file_results = []
    file_answers = []

    loadable = [f for f in files if f.content is not None]
    log(f"[DIR] Per-file mode: processing {len(loadable)} files...")

    for i, entry in enumerate(loadable):
        log(f"[DIR] [{i + 1}/{len(loadable)}] {entry.rel_path}...")

        try:
            content = entry.content
            file_context = f"File: {entry.rel_path} ({entry.file_type}, {format_size(entry.size_bytes)})\n\n{content}"

            if len(file_context) <= chunk_size:
                # Small file: single process_chunk call
                result = process_chunk(file_context, 0, 1, query, fast_model)
            else:
                # Large file: chunk and aggregate
                chunks, strategy = auto_chunk(file_context, chunk_size)
                chunk_results = []
                for ci, chunk in enumerate(chunks):
                    r = process_chunk(chunk, ci, len(chunks), query, fast_model)
                    if r:
                        chunk_results.append((ci, r))
                result = aggregate_results(chunk_results, query, fast_model) if chunk_results else None

            if result:
                file_answers.append((entry.rel_path, result))
                per_file_results.append({
                    'file': entry.rel_path,
                    'type': entry.file_type,
                    'size': entry.size_bytes,
                    'result': result,
                    'error': None
                })
                log(f"  {chr(10003)} Got result")
            else:
                per_file_results.append({
                    'file': entry.rel_path,
                    'type': entry.file_type,
                    'size': entry.size_bytes,
                    'result': None,
                    'error': 'No relevant info found'
                })
                log(f"  {chr(9675)} No relevant info")

        except Exception as e:
            per_file_results.append({
                'file': entry.rel_path,
                'type': entry.file_type,
                'size': entry.size_bytes,
                'result': None,
                'error': str(e)
            })
            log(f"  Warning: {e}")

    log(f"[DIR] Results from {len(file_answers)}/{len(loadable)} files")

    # Final aggregation across all files
    if not file_answers:
        return "No relevant information found in any files for this query.", per_file_results

    log("[DIR] Aggregating cross-file results...")
    cross_file_results = [(i, f"[File: {path}]\n{result}")
                          for i, (path, result) in enumerate(file_answers)]
    final = aggregate_results(cross_file_results, query, fast_model)

    return final, per_file_results


# ============================================================================
# Main API
# ============================================================================

def process_directory(
    directory: str,
    query: str,
    include_patterns: List[str] = None,
    exclude_patterns: List[str] = None,
    per_file: bool = False,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    fast_model: bool = False,
    max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    recursive: bool = True,
    verbose: bool = True
) -> str:
    """
    Process a directory through the RLM pipeline.

    Args:
        directory: Path to directory to process
        query: Query about the directory contents
        include_patterns: Glob patterns to include (e.g., ["*.py", "*.js"])
        exclude_patterns: Glob patterns to exclude (e.g., ["*.test.js"])
        per_file: Process each file independently (default: combined)
        chunk_size: Target chunk size in characters
        fast_model: Use Haiku for chunk processing
        max_file_size: Skip files larger than this (bytes)
        recursive: Recurse into subdirectories
        verbose: Print progress to stderr

    Returns:
        Final aggregated answer string
    """
    def log(msg):
        if verbose:
            print(msg, file=sys.stderr)

    # Validate
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Step 1: Discover files
    log(f"[DIR] Scanning: {os.path.abspath(directory)}...")
    files, skip_counts = discover_files(
        directory, include_patterns, exclude_patterns,
        max_file_size, recursive, verbose
    )

    if not files:
        skip_msg = ', '.join(f"{v} {k}" for k, v in skip_counts.items() if v > 0)
        if skip_msg:
            return f"No processable files found in {directory}. Skipped: {skip_msg}."
        if include_patterns:
            return f"No files matched the include patterns: {', '.join(include_patterns)}"
        return f"No processable files found in {directory}."

    skipped_str = ', '.join(f"{v} {k}" for k, v in skip_counts.items() if v > 0)
    log(f"[DIR] Found {len(files)} files" +
        (f" (skipped: {skipped_str})" if skipped_str else ""))

    # Step 2: Load contents
    log("[DIR] Loading file contents...")
    total_size = load_file_contents(files, verbose)
    loaded = sum(1 for f in files if f.content is not None)
    log(f"[DIR] Loaded {loaded}/{len(files)} files, {format_size(total_size)} total")

    if loaded == 0:
        return "All files failed to load. Check file permissions and formats."

    # Warn on very large directories
    if total_size > 10_000_000:
        log(f"[DIR] Warning: {format_size(total_size)} of content. "
            f"Consider using --include to narrow scope.")

    # Step 3: Generate manifest
    manifest = generate_manifest(directory, files, total_size)

    # Step 4: Process
    mode = "per-file" if per_file else "combined"
    log(f"[DIR] Processing in {mode} mode...")

    if per_file:
        final, _ = process_per_file(files, query, manifest, chunk_size, fast_model, verbose)
    else:
        combined = build_combined_content(files, manifest)
        final = process_combined(combined, query, chunk_size, fast_model, verbose)

    log("[DIR] Processing complete!")
    return final


# ============================================================================
# CLI entry point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Process a directory of files through the RLM pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze a Python project
    python directory_processor.py ./my-project "Explain the architecture"

    # Find security issues per file
    python directory_processor.py ./src "Find security vulnerabilities" --per-file

    # Process only Python files, fast mode
    python directory_processor.py ./project "Summarize" --include "*.py" --fast

    # Exclude tests, save output
    python directory_processor.py ./src "Document the API" --exclude "*.test.js,*_test.py" -o docs.md

    # Non-recursive with JSON results
    python directory_processor.py ./configs "Check for issues" --no-recursive --json results.json

Reference: Zhang, Kraska, Khattab - "Recursive Language Models" (arXiv:2512.24601)
        """
    )

    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('query', help='Query about the directory contents')
    parser.add_argument('--include', type=str, default='',
                        help='Comma-separated include patterns (e.g., "*.py,*.js")')
    parser.add_argument('--exclude', type=str, default='',
                        help='Comma-separated exclude patterns (e.g., "*.test.js")')
    parser.add_argument('--per-file', action='store_true',
                        help='Process each file independently (default: combined)')
    parser.add_argument('--chunk-size', '-c', type=int, default=DEFAULT_CHUNK_SIZE,
                        help=f'Target chunk size in characters (default: {DEFAULT_CHUNK_SIZE})')
    parser.add_argument('--fast', '-f', action='store_true',
                        help='Use faster/cheaper model for chunk processing')
    parser.add_argument('--max-file-size', type=int, default=DEFAULT_MAX_FILE_SIZE,
                        help=f'Skip files larger than N bytes (default: {DEFAULT_MAX_FILE_SIZE})')
    parser.add_argument('--no-recursive', action='store_true',
                        help='Do not recurse into subdirectories')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress progress output')
    parser.add_argument('--output', '-o', help='Write final result to file')
    parser.add_argument('--json', type=str, default='',
                        help='Save per-file results as JSON (per-file mode only)')

    args = parser.parse_args()

    # Validate directory
    if not Path(args.directory).is_dir():
        print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(1)

    # Check API key
    if not load_api_key():
        print("Error: API key not configured.", file=sys.stderr)
        print("Create file: ~/.claude/api_key.txt", file=sys.stderr)
        print("Or set ANTHROPIC_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    # Parse patterns
    include = [p.strip() for p in args.include.split(',') if p.strip()] or None
    exclude = [p.strip() for p in args.exclude.split(',') if p.strip()] or None

    try:
        if args.per_file and args.json:
            # Per-file mode with JSON output: call internal functions directly
            verbose = not args.quiet

            def log(msg):
                if verbose:
                    print(msg, file=sys.stderr)

            log(f"[DIR] Scanning: {os.path.abspath(args.directory)}...")
            files, skip_counts = discover_files(
                args.directory, include, exclude,
                args.max_file_size, not args.no_recursive, verbose
            )

            if not files:
                print("No processable files found.", file=sys.stderr)
                sys.exit(0)

            log("[DIR] Loading file contents...")
            total_size = load_file_contents(files, verbose)
            manifest = generate_manifest(args.directory, files, total_size)

            final, per_file_results = process_per_file(
                files, args.query, manifest,
                args.chunk_size, args.fast, verbose
            )

            # Write JSON results
            with open(args.json, 'w', encoding='utf-8') as f:
                json.dump(per_file_results, f, indent=2, ensure_ascii=False)
            print(f"[DIR] Per-file results saved: {args.json}", file=sys.stderr)

        else:
            final = process_directory(
                directory=args.directory,
                query=args.query,
                include_patterns=include,
                exclude_patterns=exclude,
                per_file=args.per_file,
                chunk_size=args.chunk_size,
                fast_model=args.fast,
                max_file_size=args.max_file_size,
                recursive=not args.no_recursive,
                verbose=not args.quiet,
            )

        # Output
        print("\n" + "=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)
        print(final)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(final)
            print(f"\n[Saved to {args.output}]", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n[Interrupted]", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
