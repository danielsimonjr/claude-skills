---
name: rlm-skill
description: "Use when files exceed ~100KB, multiple files need cross-referencing, analyzing folders of documents, or context would exceed working memory. Symptoms include context rot, missed details in long documents, or needing to process entire codebases."
---

# RLM: Recursive Language Model Processing

## Overview

Process files and contexts that exceed your context window using the Recursive Language Model methodology (MIT CSAIL, arXiv:2512.24601).

**Core Principle:** Don't fit everything in conversation context. Load data into a Python REPL, examine it programmatically, process in chunks with sub-LLM calls, and aggregate results.

## When to Use

- File(s) exceed ~100KB of text
- Multiple files need cross-referencing
- User asks to analyze a folder of documents
- Context would exceed your working memory
- Task requires processing then synthesizing large amounts of information

## When NOT to Use

- File fits comfortably in context (<100KB)
- Simple single-file read or keyword search
- Task doesn't require synthesis across large content

## The RLM Loop

```python
context = open("huge_file.txt").read()  # Load once
chunks = context.split('\n## ')          # Slice in memory
results = [llm_query(c) for c in chunks] # Process chunks
final = aggregate(results)               # Combine results
```

1. **Load into REPL** — `context = open(file).read()` — content lives in Python variable, not conversation
2. **Examine in memory** — `print(context[:1000])`, `len()`, structure detection
3. **Decide strategy** — Choose chunking based on observed structure (see table below)
4. **Process chunks** — `for chunk in chunks: result = llm_query(chunk)` using Haiku (cheap/fast)
5. **Aggregate results** — Combine in-memory results; use Sonnet for final synthesis

For full implementation code, see <references/complete-example.md>.

## Chunking Strategies

| Structure Detected | Strategy | Split On |
|-------------------|----------|----------|
| Markdown headers (>3) | `markdown` | `\n## ` |
| Function/class defs (>3) | `code` | `\ndef \|\nclass ` |
| JSON array | `json_array` | Array items |
| Plain text / other | `fixed_size` | 20K chars, 500 overlap |

**Always filter before LLM calls:**
```python
keywords = ["relevant", "terms", "here"]
chunks = [c for c in chunks if any(kw in c.lower() for kw in keywords)]
```

## Aggregation

- **Few results (<10):** Concatenate and send to Sonnet in one call
- **Many results (10-50):** Batch into groups of 10, aggregate each, then aggregate summaries
- **Huge results (50+):** Hierarchical — recurse until manageable (see Pattern 2 in <references/patterns.md>)

## Sub-LLM Calls

Use `scripts/rlm_query.py` for API calls, or inline the pattern:

```python
def llm_query(prompt, fast=True):
    model = "claude-haiku-4-5-20251001" if fast else "claude-sonnet-4-5-20250929"
    # Call via curl — see scripts/rlm_query.py for full implementation
```

API key lookup order: `ANTHROPIC_API_KEY` env var → `~/.claude/api_key.txt` → `~/.claude/config.json`. Run `python scripts/rlm_query.py --help` for setup instructions.

## Common Mistakes

- **Reading large files into conversation context** — use REPL variables instead; conversation context rots with volume
- **Skipping the examine step** — always inspect structure before choosing a chunking strategy
- **Using Sonnet for every chunk** — use Haiku for chunk processing, reserve Sonnet for aggregation only
- **No pre-filtering** — keyword/regex filtering before LLM calls saves significant API cost

## Helper Scripts

| Script | Purpose |
|--------|---------|
| `scripts/rlm_query.py` | Standalone sub-LLM API calls with key management |
| `scripts/rlm_processor.py` | Full RLM pipeline with auto-chunking strategies |
| `scripts/analyze_context.py` | Quick structure analysis of large files |
| `scripts/file_converter.py` | Convert PDF/DOCX/HTML/JSON/CSV to text |
| `scripts/paper_organizer.py` | Batch ML/AI paper categorization and organization |
| `scripts/directory_processor.py` | Process entire directories through RLM pipeline |

## Reference

| Document | Content |
|----------|---------|
| <references/complete-example.md> | Full standalone Python script implementing the 5-step loop |
| <references/patterns.md> | 5 emergent RLM patterns, cost optimization, benchmarks |

Based on: "Recursive Language Models" (Zhang, Kraska, Khattab — MIT CSAIL, arXiv:2512.24601)
