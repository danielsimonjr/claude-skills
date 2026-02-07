# RLM Skill — Recursive Language Model Processing

A Claude Code skill for processing files and contexts that exceed the conversation context window. Based on the paper ["Recursive Language Models"](https://arxiv.org/abs/2512.24601) by Zhang, Kraska, and Khattab (MIT CSAIL, 2025).

## What It Does

When Claude Code encounters a document, codebase, or dataset too large to fit in its context window, the RLM skill offloads the content into Python variables and processes it in chunks using sub-LLM API calls. The results are aggregated hierarchically and returned as a coherent synthesis — enabling analysis of 10M+ token contexts with no quality loss from context rot.

### Key Capabilities

| Capability | Description |
|---|---|
| **Large document analysis** | Process PDFs, DOCX, codebases, and archives of any size |
| **Auto-chunking** | Detects document structure (markdown headers, code blocks, JSON arrays, separators) and picks the optimal chunking strategy |
| **Pre-filtering** | Keyword/regex filtering eliminates irrelevant chunks before expensive LLM calls |
| **Hierarchical aggregation** | Recursively combines results when output exceeds a single-call budget |
| **Multi-format ingestion** | PDF, DOCX, HTML, JSON/JSONL, CSV, YAML, XML, archives (.zip, .tar.gz), and 30+ code/text extensions |
| **Paper triage** | Batch-categorize ML/AI research papers into USEFUL / MEANINGFUL / IMPRACTICAL with structured reports |
| **Directory processing** | Walk entire directories of mixed files, filter smartly, process combined or per-file |
| **Model tiering** | Haiku for cheap chunk processing, Sonnet for quality aggregation |

## When to Use

- File(s) exceed ~100KB of text
- Multiple files need cross-referencing
- Analyzing a folder of documents
- Context would exceed working memory
- Task requires processing then synthesizing large amounts of information

## When NOT to Use

- File fits comfortably in context (<100KB)
- Simple single-file read or keyword search
- Task doesn't require synthesis across large content

## Directory Structure

```
rlm-skill/
├── SKILL.md                         # Skill definition (loaded by Claude Code)
├── README.md                        # This file
├── scripts/
│   ├── rlm_query.py                 # Core sub-LLM API client
│   ├── rlm_processor.py             # Full RLM pipeline with auto-chunking
│   ├── analyze_context.py           # Structure analysis for large files
│   ├── file_converter.py            # Multi-format file-to-text converter
│   ├── paper_organizer.py           # Batch ML paper categorization
│   └── directory_processor.py       # Directory-level RLM processing
└── references/
    ├── complete-example.md           # Standalone Python script implementing the 5-step loop
    ├── patterns.md                   # 5 emergent RLM patterns, cost optimization, benchmarks
    ├── rlm-claude-code-implementation.md  # Architecture mapping: RLM → Claude Code
    └── Recursive Language Models.pdf # Original paper (MIT CSAIL)
```

## The RLM Loop

The core methodology is a 5-step loop:

```
1. LOAD    →  Read file into Python variable (not conversation context)
2. EXAMINE →  Inspect structure: len(), headers, separators, line patterns
3. CHUNK   →  Split based on detected structure (markdown, code, JSON, fixed-size)
4. PROCESS →  For each chunk: sub-LLM call via Haiku (cheap/fast)
5. AGGREGATE → Combine results; use Sonnet for final synthesis
```

### Chunking Strategy Selection

The auto-chunker inspects the content and selects a strategy:

| Structure Detected | Strategy | Split On |
|---|---|---|
| Document separators (>5) | `document_separator` | `\n---` or `\n===` |
| Markdown headers (>10) | `markdown_headers` | `\n# ` / `\n## ` |
| Short lines, structured data | `line_count` | Every N lines |
| Default / unstructured | `character_count` | 40K chars with 500-char overlap |

### Aggregation Rules

| Result Count | Method |
|---|---|
| Few (<10 chunk results) | Concatenate all, send to Sonnet in one call |
| Many (10–50) | Batch into groups, aggregate each, then aggregate summaries |
| Huge (50+) | Hierarchical recursion — split in half, aggregate each side, combine at root |

## Scripts Reference

### `rlm_query.py` — Sub-LLM API Client

The core building block. Calls the Anthropic API from Python using `curl` for maximum cross-platform compatibility.

```bash
# Single query
python rlm_query.py "What is the capital of France?"

# Use fast model (Haiku)
python rlm_query.py "Summarize this paragraph..." --fast

# Read prompt from file
python rlm_query.py --file prompt.txt

# System prompt + JSON output
python rlm_query.py "Classify this text" --system "You are a classifier" --json

# Check API key configuration
python rlm_query.py --check-key
```

**Programmatic usage:**

```python
from rlm_query import llm_query, llm_query_fast

# Quality call (Sonnet)
result = llm_query("Synthesize these findings: ...")

# Cheap/fast call (Haiku) — use for chunk processing
result = llm_query_fast("Extract key points from: ...")
```

**Parameters:** `prompt`, `model`, `max_tokens` (default 4096), `temperature` (default 0.0), `system`

### `rlm_processor.py` — Full RLM Pipeline

End-to-end processing: load → detect format → chunk → filter → process → aggregate.

```bash
# Basic usage
python rlm_processor.py document.pdf "What are the main conclusions?"

# Use Haiku for chunk processing (cheaper)
python rlm_processor.py codebase.zip "Find security issues" --fast

# Custom chunk size for dense content
python rlm_processor.py data.json "Count entries by category" --chunk-size 20000

# Skip pre-filtering for comprehensive analysis
python rlm_processor.py report.txt "Summarize everything" --no-filter

# Quiet mode + save to file
python rlm_processor.py paper.pdf "Extract methodology" --quiet --output result.txt
```

**Supported input formats:** PDF, DOCX, TXT, MD, HTML, JSON, JSONL, CSV, YAML, XML, ZIP, TAR.GZ, and 30+ code file extensions. Format is auto-detected from extension and file content.

**Programmatic usage:**

```python
from rlm_processor import rlm_process

answer = rlm_process(
    context_file="huge_document.pdf",
    query="What are the key findings?",
    chunk_size=40000,      # chars per chunk
    fast_model=True,       # Haiku for chunks
    filter_chunks=True,    # keyword pre-filtering
    verbose=True           # progress logging
)
```

### `analyze_context.py` — Structure Inspector

Quick analysis of a file's structure before processing. Reports character count, line count, estimated tokens, detected patterns (markdown headers, code blocks, JSON objects, XML tags, separators), and recommends a chunking strategy.

```bash
python analyze_context.py large_file.txt
```

Output includes:
- File size and token estimate
- Structure pattern counts
- Line length statistics
- First/last lines preview
- Recommended chunking strategy
- RLM processing recommendations based on size

### `file_converter.py` — Universal File-to-Text Converter

Converts any supported file format to plain text. Auto-installs required packages (`pdfplumber`, `python-docx`, `beautifulsoup4`) on first use.

```bash
# Convert to stdout
python file_converter.py document.pdf

# Convert to file
python file_converter.py document.pdf output.txt

# File info only (no conversion)
python file_converter.py document.pdf --info
```

**Format support:** PDF (via pdfplumber → pdftotext → PyPDF2 fallback chain), DOCX (headings preserved as markdown, tables extracted), HTML (scripts/styles stripped), JSON/JSONL (pretty-printed), archives (recursively extracts all text files, skips `node_modules`, `.git`, `__pycache__`).

### `paper_organizer.py` — Batch Paper Triage

Scans a directory of PDF research papers, analyzes each using sub-LLM calls, and categorizes them:

| Category | Meaning |
|---|---|
| USEFUL | Practical, applicable now — has code, solves real problems |
| MEANINGFUL | Important research but not immediately applicable |
| IMPRACTICAL | Too theoretical, too far future, or not relevant |

```bash
# Basic analysis → generates papers_report.md
python paper_organizer.py "C:\Papers\ML"

# Organize into subfolders (copies files)
python paper_organizer.py "C:\Papers\ML" --organize

# Move files instead of copying
python paper_organizer.py "C:\Papers\ML" --organize --move

# Add personal context for better relevance scoring
python paper_organizer.py "C:\Papers\ML" --context "I work on multi-agent systems and ATE"

# Faster/cheaper with Haiku + JSON export
python paper_organizer.py "C:\Papers\ML" --fast --json results.json

# Test with first 3 papers only
python paper_organizer.py "C:\Papers\ML" --limit 3
```

**Output:** Markdown report with summary stats, quick-reference table, and detailed per-paper analysis (title, authors, year, category, confidence, summary, key contributions, practical applications, limitations, relevance reasoning, time-to-value estimate, tags). Optionally creates category subfolders (`01_Useful_Practical/`, `02_Meaningful_Research/`, `03_Impractical_Future/`).

### `directory_processor.py` — Directory-Level RLM Processing

Processes entire directories of mixed files through the RLM pipeline. Walks a directory tree, discovers files (with smart exclusions), converts each to text, and processes them either as a combined stream or per-file with cross-file aggregation.

**Two processing modes:**

| Mode | Flag | Best For |
|---|---|---|
| **Combined** (default) | — | Cross-file queries ("explain this codebase's architecture") |
| **Per-file** | `--per-file` | File-scoped queries ("find security issues in each file") |

```bash
# Analyze a codebase
python directory_processor.py ./my-project "Explain the architecture" --fast

# Only Python files, per-file analysis
python directory_processor.py ./src "Find bugs in each file" --per-file --include "*.py"

# Exclude tests, save output
python directory_processor.py ./src "Document the API" --exclude "*.test.js,*_test.py" -o docs.md

# Non-recursive scan with JSON export
python directory_processor.py ./configs "Summarize each config" --per-file --no-recursive --json results.json

# Quiet mode for scripting
python directory_processor.py ./project "What does this do?" --fast --quiet
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--include` | all | Comma-separated glob patterns to include (`"*.py,*.js"`) |
| `--exclude` | none | Comma-separated glob patterns to exclude (`"*.test.js"`) |
| `--per-file` | off | Process each file independently |
| `--fast` / `-f` | off | Use Haiku for chunk processing |
| `--chunk-size` / `-c` | 40000 | Target chunk size in characters |
| `--max-file-size` | 1000000 | Skip files larger than N bytes |
| `--no-recursive` | off | Don't recurse into subdirectories |
| `--quiet` / `-q` | off | Suppress progress output |
| `--output` / `-o` | stdout | Save result to file |
| `--json` | — | Save per-file results as JSON (per-file mode only) |

**Built-in exclusions:** `.git`, `node_modules`, `__pycache__`, `venv`, `dist`, `build`, `.next`, `.cache`, hidden dirs/files, binary files (images, fonts, media, compiled files, lock files).

**Smart file ordering:** README first, then docs, source code, tests, configs, data files, other.

**Programmatic usage:**

```python
from directory_processor import process_directory

answer = process_directory(
    directory="./my-project",
    query="Explain the architecture",
    include_patterns=["*.py"],
    fast_model=True
)
```

## API Key Setup

The scripts check these locations in order:

1. `ANTHROPIC_API_KEY` environment variable
2. `~/.claude/api_key.txt` (plain text file containing just the key)
3. `~/.claude/config.json` (JSON with `{"api_key": "sk-ant-..."}`)

### Windows (PowerShell)

```powershell
# Option 1: Environment variable (temporary, current session only)
$env:ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"

# Option 2: Persistent config file (recommended)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude"
"sk-ant-api03-your-key-here" | Out-File "$env:USERPROFILE\.claude\api_key.txt" -NoNewline -Encoding utf8

# Verify
python scripts\rlm_query.py --check-key
```

### Linux / macOS

```bash
# Option 1: Environment variable
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"

# Option 2: Config file
mkdir -p ~/.claude
echo -n "sk-ant-api03-your-key-here" > ~/.claude/api_key.txt

# Verify
python scripts/rlm_query.py --check-key
```

## RLM Patterns

Five emergent patterns from the paper (detailed in `references/patterns.md`):

| # | Pattern | When to Use |
|---|---|---|
| 1 | **Filter with Model Priors** | Large context but query targets specific info — keyword-filter chunks before LLM calls |
| 2 | **Hierarchical Decomposition** | Very large contexts (>1M tokens) — recursively break into tree, process leaves, aggregate up |
| 3 | **Answer Verification** | High-stakes queries — verify candidate answer against focused evidence subset |
| 4 | **Variable-Based Output** | Long output tasks — store intermediates in Python vars, build answer programmatically |
| 5 | **Semantic Transformation** | Structured data with labels — process each entry individually (parallelizable) |

## Performance (from the paper)

| Task | Base Model | RLM | Improvement |
|---|---|---|---|
| OOLONG (GPT-5) | 44% | 56.5% | +28% |
| OOLONG-Pairs (GPT-5) | <0.1% | 58% | >500x |
| BrowseComp+ 1K (GPT-5) | 0%* | 91.3% | N/A |
| CodeQA (GPT-5) | 24%* | 62% | +158% |

\*Base model cannot fit context.

## Cost Optimization

- **Model tiering:** Haiku for chunk processing (~$0.25/M input), Sonnet for aggregation (~$3/M input)
- **Pre-filtering:** Keyword/regex filtering before LLM calls eliminates 50-90% of irrelevant chunks
- **Early termination:** Stop processing if high-confidence answer found
- **Caching:** Save intermediate results to files for re-analysis
- **Adaptive chunk sizing:** Smaller chunks for dense code, larger for prose

## Common Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| Reading large files into conversation context | Context rot — quality degrades with volume | Load into Python REPL variables |
| Skipping the examine step | Wrong chunking strategy wastes API calls | Always inspect structure first |
| Using Sonnet for every chunk | 12x more expensive than Haiku | Haiku for chunks, Sonnet for aggregation only |
| No pre-filtering | Processing irrelevant chunks wastes money | Keyword/regex filter before LLM calls |

## Dependencies

**Required:**
- Python 3.8+
- `curl` (ships with Windows 10+, macOS, and most Linux distros)
- Anthropic API key

**Auto-installed on first use** (by `file_converter.py`):
- `pdfplumber` — PDF text extraction
- `python-docx` — Word document parsing
- `beautifulsoup4` — HTML text extraction

## References

- **Paper:** Zhang, Kraska, Khattab — "Recursive Language Models" (MIT CSAIL, arXiv:2512.24601, 2025)
- **Architecture:** `references/rlm-claude-code-implementation.md` — How RLM maps to Claude Code's tools
- **Patterns:** `references/patterns.md` — 5 emergent patterns, cost optimization, negative results
- **Example:** `references/complete-example.md` — Full standalone 5-step processing script
