#!/usr/bin/env python3
"""
analyze_context.py - Analyze structure of long context files for RLM processing.

Usage: python analyze_context.py <context_file>
"""

import sys
import re
from collections import Counter
from pathlib import Path


def analyze_context(filepath: str) -> dict:
    """Analyze a context file and return structural information."""
    
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    analysis = {
        'file_path': filepath,
        'total_chars': len(content),
        'total_lines': len(lines),
        'estimated_tokens': len(content) // 4,  # Rough estimate
        'non_empty_lines': sum(1 for l in lines if l.strip()),
    }
    
    # Detect structure patterns
    patterns = {
        'json_objects': len(re.findall(r'^\s*\{', content, re.MULTILINE)),
        'markdown_headers': len(re.findall(r'^#+\s+', content, re.MULTILINE)),
        'code_blocks': len(re.findall(r'```', content)) // 2,
        'xml_tags': len(re.findall(r'<[a-zA-Z][^>]*>', content)),
        'document_separators': len(re.findall(r'\n---+\n|\n===+\n|\n\*\*\*+\n', content)),
        'numbered_items': len(re.findall(r'^\s*\d+[\.\)]\s+', content, re.MULTILINE)),
        'bullet_points': len(re.findall(r'^\s*[-*•]\s+', content, re.MULTILINE)),
    }
    analysis['patterns'] = patterns
    
    # Line length statistics
    line_lengths = [len(l) for l in lines]
    if line_lengths:
        analysis['line_stats'] = {
            'avg_length': sum(line_lengths) // len(line_lengths),
            'max_length': max(line_lengths),
            'min_non_empty': min((l for l in line_lengths if l > 0), default=0),
        }
    
    # Sample content
    analysis['first_lines'] = lines[:20]
    analysis['last_lines'] = lines[-10:] if len(lines) > 10 else lines
    
    # Suggest chunking strategy
    if patterns['document_separators'] > 5:
        analysis['suggested_chunking'] = 'document_boundaries'
    elif patterns['json_objects'] > 10:
        analysis['suggested_chunking'] = 'json_objects'
    elif patterns['markdown_headers'] > 10:
        analysis['suggested_chunking'] = 'markdown_sections'
    elif analysis['total_lines'] > 1000:
        analysis['suggested_chunking'] = 'line_count'
    else:
        analysis['suggested_chunking'] = 'character_count'
    
    return analysis


def print_analysis(analysis: dict):
    """Pretty print the analysis."""
    
    print("=" * 60)
    print("CONTEXT ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"\n📁 File: {analysis['file_path']}")
    print(f"📊 Size: {analysis['total_chars']:,} characters")
    print(f"📊 Lines: {analysis['total_lines']:,} total ({analysis['non_empty_lines']:,} non-empty)")
    print(f"📊 Estimated tokens: ~{analysis['estimated_tokens']:,}")
    
    print("\n📐 LINE STATISTICS:")
    if 'line_stats' in analysis:
        stats = analysis['line_stats']
        print(f"   Average length: {stats['avg_length']} chars")
        print(f"   Max length: {stats['max_length']} chars")
    
    print("\n🔍 STRUCTURE PATTERNS:")
    for pattern, count in analysis['patterns'].items():
        if count > 0:
            print(f"   {pattern}: {count}")
    
    print(f"\n💡 SUGGESTED CHUNKING: {analysis['suggested_chunking']}")
    
    print("\n📖 FIRST 20 LINES:")
    print("-" * 40)
    for i, line in enumerate(analysis['first_lines'], 1):
        preview = line[:80] + "..." if len(line) > 80 else line
        print(f"{i:4d} | {preview}")
    
    print("\n📖 LAST 10 LINES:")
    print("-" * 40)
    start_num = analysis['total_lines'] - len(analysis['last_lines']) + 1
    for i, line in enumerate(analysis['last_lines'], start_num):
        preview = line[:80] + "..." if len(line) > 80 else line
        print(f"{i:4d} | {preview}")
    
    print("\n" + "=" * 60)
    
    # RLM recommendations
    tokens = analysis['estimated_tokens']
    if tokens > 100000:
        print("⚠️  VERY LARGE CONTEXT - Aggressive chunking recommended")
        print(f"   Suggested chunk count: {tokens // 30000} chunks")
    elif tokens > 50000:
        print("⚠️  LARGE CONTEXT - Standard RLM processing recommended")
        print(f"   Suggested chunk count: {tokens // 40000} chunks")
    else:
        print("✅ MODERATE CONTEXT - May fit in context window, but RLM still beneficial")
    
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_context.py <context_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    analysis = analyze_context(filepath)
    print_analysis(analysis)
