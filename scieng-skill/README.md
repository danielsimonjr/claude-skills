# SciEng Skill

A Claude Code skill for creating, editing, visualizing, and rendering scientific and engineering documents — Mermaid diagrams, Graphviz DOT graphs, LaTeX equations, and self-contained HTML playgrounds with rich technical content.

## What It Does

| Capability | Description |
|---|---|
| **Mermaid Diagrams** | Flowcharts, state machines, sequence diagrams, class diagrams, ER diagrams, Gantt charts, pie charts, mindmaps, and 15+ diagram types with syntax validation |
| **Graphviz/DOT Graphs** | Hierarchical, spring-layout, force-directed, circular, and radial graph rendering with node shapes, record nodes, HTML labels, and subgraph clusters |
| **LaTeX Math** | Fast client-side rendering via KaTeX with fallback to MathJax for advanced packages; SI units, engineering notation, cross-referenced equations |
| **Engineering Notation** | Pre-configured macros for electrical engineering, control systems, semiconductors, and systems engineering |
| **Timing Diagrams** | WaveDrom JSON-based digital timing waveforms with signal grouping and edge annotations |
| **Circuit Schematics** | SVG-based circuit diagrams with component symbols and signal flow |
| **Scientific Plotting** | Interactive Plotly.js charts for Bode plots, Nyquist diagrams, root locus, step/impulse response, FFT, pole-zero plots |
| **Document Features** | Cross-referencing for auto-numbered figures/tables/equations, multi-panel layouts, parameter tables with uncertainty |
| **Self-Contained HTML** | Standalone browser-viewable playgrounds with embedded math, diagrams, charts, and code — no server required |

## When to Use

- Creating or editing Mermaid diagrams (flowcharts, state machines, sequence diagrams)
- Rendering Graphviz DOT graphs for hierarchical or force-directed layouts
- Writing LaTeX for academic papers, technical documentation, or CS coursework
- Building self-contained HTML documents with embedded math, diagrams, and interactive charts
- Generating scientific/engineering documentation with professional layout and cross-references
- Debugging diagram syntax or visualizing complex system architectures
- Creating timing diagrams for digital logic, bus protocols, or interface specifications

## When NOT to Use

- Pure terminal text output or simple inline code blocks
- User already has an existing rendering pipeline
- Real-time collaborative editing (skill generates static output)
- Documents requiring server-side processing or database integration

## Directory Structure

```
scieng-skill/
├── SKILL.md                      # Skill trigger definition (loaded by Claude Code)
├── SCIENG.md                     # Main scientific/engineering reference (41.5 KB)
├── MERMAID.md                    # Mermaid diagram syntax reference
├── LATEX.md                      # LaTeX & MathJax reference
├── GRAPHVIZ.md                   # DOT syntax reference
├── RENDERERS.md                  # Renderer implementation guide + CDN imports
├── render-mermaid-to-svg.js      # Mermaid to SVG renderer
├── render-latex-to-svg.js        # LaTeX to SVG renderer
└── render-dot-to-svg.js          # Graphviz/DOT to SVG renderer
```

## Renderers Reference

### `render-mermaid-to-svg.js`

Converts Mermaid diagram syntax to standalone SVG files via the mermaid.ink API.

```bash
node render-mermaid-to-svg.js <input.mmd> [output.svg]
```

**Dependencies:** Mermaid v11 (CDN), pako (base64url deflate encoding), mermaid.ink API

**Features:**
- 15+ diagram types: flowchart, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram, gantt, pie, gitGraph, mindmap, timeline, quadrantChart, sankey-beta, xychart-beta, block-beta, packet-beta, kanban, architecture-beta
- Configurable themes: default, dark, forest, neutral
- Dynamic rendering via `mermaid.run()` for post-load injection
- Security level 'loose' enables HTML and click functionality

---

### `render-latex-to-svg.js`

Converts LaTeX math expressions and documents to SVG via the latex.codecogs.com API.

```bash
node render-latex-to-svg.js <input.tex> [output.svg]
```

**Rendering engines (choose one per document):**

| Engine | Size | Best For |
|---|---|---|
| **KaTeX v0.16.21** (default) | ~300KB | Fast client-side rendering, standard math |
| **MathJax v3** (fallback) | ~1.5MB | Advanced packages: `\newcommand`, `\begin{align}`, chemistry, physics, AMS environments |

**Engineering macros (MathJax):** Electrical engineering (phasors, impedance, transforms), control systems (transfer functions, stability metrics), semiconductors (device parameters), systems engineering (reliability), SI units

**Delimiter support:** Display math `$$...$$` or `\[...\]`, inline math `\(...\)` (recommended over `$...$`)

**Critical constraint:** Never mix KaTeX and MathJax in the same document.

---

### `render-dot-to-svg.js`

Converts Graphviz DOT language to SVG via Viz.js (WebAssembly-based Graphviz).

```bash
node render-dot-to-svg.js <input.dot> [output.svg]
```

**Dependencies:** Viz.js (@viz-js/viz v3, ~3-5MB WASM, CDN-only)

**Layout engines:** dot (hierarchical), neato (spring), fdp (force-directed), sfdp (scalable force-directed), circo (circular), twopi (radial), osage (clustered), patchwork (treemap)

**Critical constraint:** Async-only API — always use `.then()` or `await`. CDN-only due to WASM binary size.

## Sub-skill Reference

| Document | Size | Content |
|---|---|---|
| **SCIENG.md** | 41.5 KB | Main reference: MathJax engineering config, SI units, WaveDrom timing diagrams, SVG circuits, control systems plotting (Bode/Nyquist/root locus), signal processing, systems engineering diagrams, document structure/typography, cross-referencing, multi-panel layouts, data tables with uncertainty, complete document skeleton, domain quick reference |
| **MERMAID.md** | 5.8 KB | Mermaid syntax: 10+ diagram types, critical syntax rules, node shapes/styling, edge types/labels, subgraph clusters, validation checklist |
| **LATEX.md** | 6.8 KB | LaTeX reference: algorithm packages (algorithm2e vs algorithmicx), document classes (acmart, IEEEtran, NeurIPS), theorems/proofs, math notation, tables (booktabs), code listings, subfigures, SI units, validation checklist |
| **GRAPHVIZ.md** | 5.3 KB | DOT syntax: graph basics, node shapes, record nodes, HTML labels, subgraph clusters, edge styling, layout engines, validation checklist |
| **RENDERERS.md** | 13.4 KB | Implementation guide: CDN imports + version pins, library compatibility matrix, HTML playground template, renderer integration patterns, dark theme styling, conditional imports |

## Usage

The skill triggers in Claude Code when you need to create or work with scientific/engineering content:

1. **Identify the renderer** — Mermaid for diagrams, Graphviz for graph layouts, LaTeX for math
2. **Consult syntax references** — Review MERMAID.md, GRAPHVIZ.md, LATEX.md, or SCIENG.md
3. **Select CDN imports** — All libraries load at runtime via CDN; no installation needed
4. **Compose HTML** — Write a self-contained file with embedded diagrams, math, and styling
5. **Write to disk and open** — User views the result in their browser

## Dependencies

All rendering dependencies load at runtime via CDN — no local installation required:

| Library | Version | Size | Purpose |
|---|---|---|---|
| Mermaid | v11 | ~800KB | Diagram rendering |
| KaTeX | v0.16.21 | ~300KB | Fast LaTeX math (default) |
| MathJax | v3 | ~1.5MB | Advanced LaTeX math (fallback) |
| Viz.js | v3 | ~3-5MB | Graphviz DOT rendering (WASM) |
| Plotly.js | latest | ~3MB | Scientific plotting |
| WaveDrom | latest | ~100KB | Timing diagrams |
| Highlight.js | latest | ~50KB | Code syntax highlighting |

**Node.js** is required for the standalone renderer scripts (`render-*.js`).
