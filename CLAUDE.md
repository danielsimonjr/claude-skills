# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of **Claude Code skills** — standalone knowledge modules that extend Claude Code's capabilities in specific domains. Each skill lives in its own directory with a `SKILL.md` entry point (YAML frontmatter with `name` and `description`, followed by the skill content). Skills are not traditional software with build/test pipelines; they are structured reference documents and supporting scripts.

## Skill Architecture

Each skill directory follows this pattern:
- **`SKILL.md`** — Primary skill definition loaded by Claude Code (required). Contains YAML frontmatter (`name`, `description`) and the full skill content.
- **`README.md`** — Human-readable overview and usage documentation.
- **`references/`** — Supporting reference materials, examples, and deep-dive documents.
- **`examples/`** — Worked examples demonstrating the skill in action.

### Skills in This Repository

| Directory | Skill Name | Domain |
|-----------|-----------|--------|
| `analytical-methology-skill/` | analytical-methodology | Structured analysis frameworks (5W1H, SWOT, Root Cause, Fishbone, PESTLE, etc.) for use with DeepThinking MCP |
| `john-carmack-programming-skill/` | carmack-programming | Performance-first programming: cache-conscious design, SoA patterns, arena allocators, SIMD, branchless code |
| `reasoning-skill/` | reasoning | 110+ reasoning types with cognitive bias detection/mitigation framework |
| `refactoring-skill/` | refactoring | Torvalds/Carmack-style code refactoring across C++, Python, Go, JS/TS |
| `rlm-skill/` | rlm-skill | Recursive Language Model processing for files exceeding context windows |
| `scieng-skill/` | scieng-skill | Mermaid, Graphviz, LaTeX, and scientific/engineering document rendering as self-contained HTML |
| `skill-validator/` | skill-validator | Claude-only skill that validates SKILL.md structure and YAML frontmatter |
| `universal-tensor-physics-skill/` | tensor-physics-research | Theoretical physics research (UPTF), tensor math, bridge equations |

## RLM Skill — The Only Skill with Runnable Code

The `rlm-skill/` is the only skill containing executable Python scripts. Key details:

- **Language:** Python 3.8+
- **External dependency:** `curl` (for API calls) and `ANTHROPIC_API_KEY`
- **Auto-installed packages:** `pdfplumber`, `python-docx`, `beautifulsoup4` (installed on first use by `file_converter.py`)
- **No test suite** — scripts are standalone CLI tools

### Running RLM Scripts

```bash
# From the rlm-skill/scripts/ directory:
python rlm_query.py "prompt here"                          # Sub-LLM API call
python rlm_processor.py document.pdf "Your query" --fast   # Full RLM pipeline
python analyze_context.py large_file.txt                   # Structure analysis
python file_converter.py document.pdf                      # Format conversion
python paper_organizer.py ./papers --organize              # Batch paper triage
python directory_processor.py ./src "Find bugs" --per-file # Directory processing
```

### RLM Script Architecture

`rlm_query.py` is the core building block — all other scripts import `llm_query` / `llm_query_fast` from it. The processing pipeline flows: `file_converter.py` (format detection) → `rlm_processor.py` (chunk + process + aggregate). `directory_processor.py` wraps `rlm_processor` for multi-file workflows.

## Conventions

- Skill content is Markdown with embedded code examples (not meant to be executed directly, except RLM scripts).
- YAML frontmatter in `SKILL.md` must have `name` and `description` fields — Claude Code uses `description` to decide when to activate the skill.
- The `scieng-skill/` includes three Node.js renderer scripts (`render-*.js`) that call external APIs (codecogs, quickchart.io, mermaid.ink) to produce SVG files. These require Node.js but no npm dependencies.
- Cross-references within skills use relative links and `<filename.md>` tag syntax.
