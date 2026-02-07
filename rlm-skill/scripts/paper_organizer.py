#!/usr/bin/env python3
"""
paper_organizer.py - Batch process and categorize ML/AI research papers.

Scans a directory of PDFs, analyzes each paper using RLM, and categorizes them into:
- USEFUL: Practical, applicable now or very soon
- MEANINGFUL: Important research, but not immediately applicable
- IMPRACTICAL: Too theoretical, too far future, or not relevant

Usage:
    python paper_organizer.py "C:\Papers\ML" --output report.md
    python paper_organizer.py "C:\Papers" --organize  # Creates subdirectories
    python paper_organizer.py "C:\Papers" --fast      # Uses cheaper model

Output:
    - Markdown report with categorized papers
    - Optional: Moves/copies papers into category folders

Requirements:
    - API key in %USERPROFILE%\.claude\api_key.txt or ANTHROPIC_API_KEY env var
    - pdfplumber (auto-installed)

Author: RLM Skill for Claude Code
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

# Add script directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from rlm_query import llm_query, llm_query_fast, load_api_key
except ImportError as e:
    print(f"Error: Required modules not found. Run from the scripts directory.")
    print(f"Details: {e}")
    sys.exit(1)


# Categories for paper classification
CATEGORIES = {
    "USEFUL": {
        "description": "Practical, applicable now or in the near term (< 1 year)",
        "folder": "01_Useful_Practical",
        "emoji": "🟢",
        "criteria": [
            "Has working code/implementation available",
            "Addresses a problem you're currently working on",
            "Provides techniques that can be applied immediately",
            "Improves existing workflows or tools",
            "Production-ready or near production-ready"
        ]
    },
    "MEANINGFUL": {
        "description": "Important research, foundational, but not immediately applicable",
        "folder": "02_Meaningful_Research",
        "emoji": "🟡",
        "criteria": [
            "Novel theoretical contributions",
            "Benchmarks or datasets that advance the field",
            "Architectural innovations (but complex to implement)",
            "State-of-the-art results but requires significant resources",
            "Good for understanding trends and directions"
        ]
    },
    "IMPRACTICAL": {
        "description": "Too theoretical, too far future, niche, or not relevant",
        "folder": "03_Impractical_Future",
        "emoji": "🔴",
        "criteria": [
            "Requires hardware/compute not available",
            "Purely theoretical without clear path to application",
            "Addresses problems you don't have",
            "Superseded by newer work",
            "Too niche or specialized for your needs"
        ]
    }
}


@dataclass
class PaperAnalysis:
    """Analysis result for a single paper."""
    filename: str
    filepath: str
    title: str
    authors: str
    year: str
    category: str
    confidence: str  # HIGH, MEDIUM, LOW
    summary: str
    key_contributions: List[str]
    practical_applications: List[str]
    limitations: List[str]
    relevance_reasoning: str
    estimated_time_to_value: str
    tags: List[str]
    error: Optional[str] = None


def extract_paper_text(pdf_path: str, max_pages: int = 15) -> Tuple[str, str]:
    """
    Extract text from a PDF paper.
    
    Returns:
        Tuple of (full_text, first_pages_text)
    """
    try:
        # Try pdfplumber first
        try:
            import pdfplumber
        except ImportError:
            import subprocess
            print("  Installing pdfplumber...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pdfplumber', 
                          '--break-system-packages', '-q'], check=True)
            import pdfplumber
        
        text_parts = []
        first_pages = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    if i < 3:  # First 3 pages for quick analysis
                        first_pages.append(page_text)
                
                if i >= max_pages:
                    text_parts.append(f"\n[... Truncated after {max_pages} pages ...]")
                    break
        
        full_text = '\n\n'.join(text_parts)
        first_text = '\n\n'.join(first_pages)
        
        return full_text, first_text
        
    except Exception as e:
        return "", f"Error extracting PDF: {e}"


def analyze_paper(
    pdf_path: str,
    user_context: str = "",
    fast_model: bool = False,
    verbose: bool = True
) -> PaperAnalysis:
    """
    Analyze a single paper and categorize it.
    """
    filename = Path(pdf_path).name
    
    if verbose:
        print(f"  📄 Extracting text...")
    
    # Extract text
    full_text, first_pages = extract_paper_text(pdf_path)
    
    if not full_text or full_text.startswith("Error"):
        return PaperAnalysis(
            filename=filename,
            filepath=str(pdf_path),
            title="[Extraction Failed]",
            authors="Unknown",
            year="Unknown",
            category="UNKNOWN",
            confidence="LOW",
            summary="Could not extract text from PDF",
            key_contributions=[],
            practical_applications=[],
            limitations=[],
            relevance_reasoning=first_pages if first_pages.startswith("Error") else "PDF extraction failed",
            estimated_time_to_value="Unknown",
            tags=["extraction-error"],
            error=first_pages if first_pages.startswith("Error") else "Empty PDF"
        )
    
    if verbose:
        print(f"  🤖 Analyzing with LLM...")
    
    # Build analysis prompt
    categories_desc = "\n".join([
        f"- {cat}: {info['description']}"
        for cat, info in CATEGORIES.items()
    ])
    
    user_context_section = ""
    if user_context:
        user_context_section = f"""
USER CONTEXT (consider this when determining relevance):
{user_context}
"""
    
    analysis_prompt = f"""Analyze this ML/AI research paper and categorize it.

PAPER TEXT (first pages for metadata):
---
{first_pages[:8000]}
---

ADDITIONAL CONTENT:
---
{full_text[8000:20000] if len(full_text) > 8000 else "[No additional content]"}
---
{user_context_section}
CATEGORIES:
{categories_desc}

Respond in this exact JSON format (no markdown, just JSON):
{{
    "title": "Full paper title",
    "authors": "First Author et al." or list of authors,
    "year": "2024" or "Unknown",
    "category": "USEFUL" or "MEANINGFUL" or "IMPRACTICAL",
    "confidence": "HIGH" or "MEDIUM" or "LOW",
    "summary": "2-3 sentence summary of what the paper does",
    "key_contributions": ["contribution 1", "contribution 2"],
    "practical_applications": ["application 1", "application 2"],
    "limitations": ["limitation 1", "limitation 2"],
    "relevance_reasoning": "Why this category? 2-3 sentences explaining the classification",
    "estimated_time_to_value": "Immediate" or "3-6 months" or "6-12 months" or "1+ years" or "Theoretical only",
    "tags": ["tag1", "tag2", "tag3"]
}}

Be practical and realistic. Consider:
- Is there working code available?
- How much compute/data is needed?
- Is this solving a real problem or just advancing benchmarks?
- Would a practitioner benefit from reading this?

JSON response:"""

    query_fn = llm_query_fast if fast_model else llm_query
    
    try:
        response = query_fn(analysis_prompt, max_tokens=2000)
        
        # Parse JSON response
        response = response.strip()
        if response.startswith("```"):
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        response = response.strip()
        
        data = json.loads(response)
        
        return PaperAnalysis(
            filename=filename,
            filepath=str(pdf_path),
            title=data.get("title", filename),
            authors=data.get("authors", "Unknown"),
            year=data.get("year", "Unknown"),
            category=data.get("category", "MEANINGFUL"),
            confidence=data.get("confidence", "MEDIUM"),
            summary=data.get("summary", ""),
            key_contributions=data.get("key_contributions", []),
            practical_applications=data.get("practical_applications", []),
            limitations=data.get("limitations", []),
            relevance_reasoning=data.get("relevance_reasoning", ""),
            estimated_time_to_value=data.get("estimated_time_to_value", "Unknown"),
            tags=data.get("tags", [])
        )
        
    except json.JSONDecodeError as e:
        return PaperAnalysis(
            filename=filename,
            filepath=str(pdf_path),
            title=filename,
            authors="Unknown",
            year="Unknown",
            category="MEANINGFUL",
            confidence="LOW",
            summary="Analysis completed but response parsing failed",
            key_contributions=[],
            practical_applications=[],
            limitations=[],
            relevance_reasoning=f"JSON parsing error: {str(e)[:100]}",
            estimated_time_to_value="Unknown",
            tags=["parse-error"],
            error=f"JSON parse error: {e}"
        )
    except Exception as e:
        return PaperAnalysis(
            filename=filename,
            filepath=str(pdf_path),
            title=filename,
            authors="Unknown",
            year="Unknown",
            category="UNKNOWN",
            confidence="LOW",
            summary="Analysis failed",
            key_contributions=[],
            practical_applications=[],
            limitations=[],
            relevance_reasoning=str(e),
            estimated_time_to_value="Unknown",
            tags=["error"],
            error=str(e)
        )


def find_pdfs(directory: str, recursive: bool = True) -> List[str]:
    """Find all PDF files in a directory."""
    directory = Path(directory)
    
    if recursive:
        pdfs = list(directory.rglob("*.pdf"))
    else:
        pdfs = list(directory.glob("*.pdf"))
    
    return [str(p) for p in sorted(pdfs)]


def generate_report(
    analyses: List[PaperAnalysis],
    output_path: str,
    include_errors: bool = True
) -> str:
    """Generate a markdown report of all analyzed papers."""
    
    # Group by category
    by_category = {"USEFUL": [], "MEANINGFUL": [], "IMPRACTICAL": [], "UNKNOWN": []}
    for analysis in analyses:
        cat = analysis.category if analysis.category in by_category else "UNKNOWN"
        by_category[cat].append(analysis)
    
    # Build report
    report = []
    report.append("# ML/AI Papers Analysis Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**Total Papers:** {len(analyses)}")
    report.append("")
    
    # Summary stats
    report.append("## Summary\n")
    report.append("| Category | Count | Description |")
    report.append("|----------|-------|-------------|")
    for cat, info in CATEGORIES.items():
        count = len(by_category.get(cat, []))
        emoji = info['emoji']
        report.append(f"| {emoji} **{cat}** | {count} | {info['description']} |")
    if by_category.get("UNKNOWN"):
        report.append(f"| ❓ UNKNOWN | {len(by_category['UNKNOWN'])} | Could not be categorized |")
    report.append("")
    
    # Quick reference table
    report.append("## Quick Reference\n")
    report.append("| # | Title | Category | Time to Value | Tags |")
    report.append("|---|-------|----------|---------------|------|")
    
    for i, analysis in enumerate(analyses, 1):
        if analysis.error:
            continue
        emoji = CATEGORIES.get(analysis.category, {}).get('emoji', '❓')
        tags = ', '.join(analysis.tags[:3]) if analysis.tags else '-'
        title_short = analysis.title[:40] + "..." if len(analysis.title) > 40 else analysis.title
        report.append(f"| {i} | {title_short} | {emoji} {analysis.category} | {analysis.estimated_time_to_value} | {tags} |")
    
    report.append("")
    
    # Detailed sections
    for cat in ["USEFUL", "MEANINGFUL", "IMPRACTICAL"]:
        papers = by_category.get(cat, [])
        if not papers:
            continue
            
        info = CATEGORIES[cat]
        report.append(f"\n---\n\n## {info['emoji']} {cat}: {info['description']}")
        report.append(f"\n*{len(papers)} papers in this category*\n")
        
        # Sort by confidence (HIGH first) then by title
        papers.sort(key=lambda p: (0 if p.confidence == "HIGH" else 1 if p.confidence == "MEDIUM" else 2, p.title))
        
        for i, paper in enumerate(papers, 1):
            report.append(f"### {i}. {paper.title}")
            report.append(f"**Authors:** {paper.authors} ({paper.year})")
            report.append(f"**Confidence:** {paper.confidence} | **Time to Value:** {paper.estimated_time_to_value}")
            report.append(f"**File:** `{paper.filename}`")
            report.append("")
            report.append(f"**Summary:** {paper.summary}")
            report.append("")
            
            if paper.key_contributions:
                report.append("**Key Contributions:**")
                for contrib in paper.key_contributions[:3]:
                    report.append(f"- {contrib}")
                report.append("")
            
            if paper.practical_applications:
                report.append("**Practical Applications:**")
                for app in paper.practical_applications[:3]:
                    report.append(f"- {app}")
                report.append("")
            
            if paper.relevance_reasoning:
                report.append(f"**Why {cat}?** {paper.relevance_reasoning}")
                report.append("")
            
            if paper.tags:
                report.append(f"**Tags:** {', '.join(paper.tags)}")
            
            report.append("\n---\n")
    
    # Errors section
    if include_errors and by_category.get("UNKNOWN"):
        report.append("\n## ❓ Papers with Errors\n")
        for paper in by_category["UNKNOWN"]:
            report.append(f"- **{paper.filename}**: {paper.error or 'Unknown error'}")
    
    # Write report
    report_text = "\n".join(report)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return report_text


def organize_files(
    analyses: List[PaperAnalysis],
    source_dir: str,
    copy_mode: bool = True,
    verbose: bool = True
) -> Dict[str, int]:
    """
    Organize papers into category folders.
    """
    source_dir = Path(source_dir)
    counts = {"USEFUL": 0, "MEANINGFUL": 0, "IMPRACTICAL": 0, "UNKNOWN": 0}
    
    for analysis in analyses:
        cat = analysis.category if analysis.category in CATEGORIES else "UNKNOWN"
        
        if cat == "UNKNOWN":
            folder_name = "04_Needs_Review"
        else:
            folder_name = CATEGORIES[cat]["folder"]
        
        dest_dir = source_dir / folder_name
        dest_dir.mkdir(exist_ok=True)
        
        src_path = Path(analysis.filepath)
        dest_path = dest_dir / src_path.name
        
        # Skip if already in correct folder
        if src_path.parent == dest_dir:
            counts[cat] += 1
            continue
        
        try:
            if copy_mode:
                shutil.copy2(src_path, dest_path)
            else:
                shutil.move(src_path, dest_path)
            
            counts[cat] += 1
            
            if verbose:
                action = "Copied" if copy_mode else "Moved"
                print(f"  [{cat}] {action}: {src_path.name} -> {folder_name}/")

        except Exception as e:
            print(f"  [!] Error with {src_path.name}: {e}")
    
    return counts


def save_json_results(analyses: List[PaperAnalysis], output_path: str):
    """Save analysis results as JSON for programmatic use."""
    data = [asdict(a) for a in analyses]
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Batch analyze and categorize ML/AI research papers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze papers and generate report
    python paper_organizer.py "C:\\Papers\\ML"
    
    # Analyze and organize into folders (copy mode)
    python paper_organizer.py "C:\\Papers\\ML" --organize
    
    # Analyze and move files (not copy)
    python paper_organizer.py "C:\\Papers\\ML" --organize --move
    
    # Use faster/cheaper model
    python paper_organizer.py "C:\\Papers\\ML" --fast
    
    # Add context about your work for better relevance scoring
    python paper_organizer.py "C:\\Papers\\ML" --context "I work on automated testing and ATE systems"
    
    # Limit number of papers (for testing)
    python paper_organizer.py "C:\\Papers\\ML" --limit 5

Categories:
    🟢 USEFUL:      Practical, applicable now (has code, solves real problems)
    🟡 MEANINGFUL:  Important research, but not immediately applicable
    🔴 IMPRACTICAL: Too theoretical, too far future, or not relevant
        """
    )
    
    parser.add_argument('directory', help='Directory containing PDF papers')
    parser.add_argument('--output', '-o', default='papers_report.md', 
                        help='Output report path (default: papers_report.md)')
    parser.add_argument('--json', '-j', default='',
                        help='Also save results as JSON file')
    parser.add_argument('--organize', action='store_true',
                        help='Organize papers into category folders')
    parser.add_argument('--move', action='store_true',
                        help='Move files instead of copying (use with --organize)')
    parser.add_argument('--fast', '-f', action='store_true',
                        help='Use faster/cheaper model')
    parser.add_argument('--context', '-c', type=str, default='',
                        help='Your work context for relevance (e.g., "I work on computer vision")')
    parser.add_argument('--limit', '-l', type=int, default=0,
                        help='Limit number of papers to process (0 = all)')
    parser.add_argument('--no-recursive', action='store_true',
                        help='Do not search subdirectories')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output')
    
    args = parser.parse_args()
    
    # Validate directory
    if not Path(args.directory).is_dir():
        print(f"Error: Directory not found: {args.directory}")
        sys.exit(1)
    
    # Check API key
    if not load_api_key():
        print("Error: API key not configured.")
        print("Create file: %USERPROFILE%\\.claude\\api_key.txt")
        print("Or set ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)
    
    verbose = not args.quiet
    
    # Find PDFs
    if verbose:
        print(f"\n🔍 Scanning for PDFs in: {args.directory}")
    
    pdfs = find_pdfs(args.directory, recursive=not args.no_recursive)
    
    if not pdfs:
        print("No PDF files found.")
        sys.exit(0)
    
    if args.limit > 0:
        pdfs = pdfs[:args.limit]
    
    if verbose:
        print(f"📚 Found {len(pdfs)} PDF files\n")
    
    # Analyze papers
    analyses = []
    errors = 0
    
    for i, pdf_path in enumerate(pdfs, 1):
        if verbose:
            print(f"[{i}/{len(pdfs)}] {Path(pdf_path).name[:50]}...")
        
        analysis = analyze_paper(
            pdf_path,
            user_context=args.context,
            fast_model=args.fast,
            verbose=verbose
        )
        analyses.append(analysis)
        
        if analysis.error:
            errors += 1
        
        if verbose:
            if analysis.error:
                print(f"  [!] Error: {analysis.error[:50]}")
            else:
                print(f"  [{analysis.category}] ({analysis.confidence}) - {analysis.title[:40]}...")
        
        print()  # Blank line between papers
    
    # Generate report
    if verbose:
        print(f"📝 Generating report: {args.output}")
    
    generate_report(analyses, args.output)
    
    # Save JSON if requested
    if args.json:
        save_json_results(analyses, args.json)
        if verbose:
            print(f"📄 JSON saved: {args.json}")
    
    # Organize files if requested
    if args.organize:
        if verbose:
            print(f"\n📁 Organizing papers into folders...")
        
        counts = organize_files(
            analyses,
            args.directory,
            copy_mode=not args.move,
            verbose=verbose
        )
    
    # Summary
    if verbose:
        print(f"\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        
        by_cat = {}
        for a in analyses:
            by_cat[a.category] = by_cat.get(a.category, 0) + 1
        
        for cat in ["USEFUL", "MEANINGFUL", "IMPRACTICAL"]:
            count = by_cat.get(cat, 0)
            print(f"  [{cat}] {count} papers")

        if by_cat.get("UNKNOWN", 0) > 0:
            print(f"  [?] UNKNOWN/ERRORS: {by_cat['UNKNOWN']} papers")
        
        print(f"\n📄 Report saved to: {args.output}")
        
        if args.organize:
            print(f"📁 Papers organized into: {args.directory}")
        
        print("="*60)


if __name__ == "__main__":
    main()
