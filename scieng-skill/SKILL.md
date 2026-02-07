---
name: scieng-skill
description: "Use when creating, editing, visualizing, previewing, rendering, or debugging Mermaid diagrams, Graphviz DOT graphs, LaTeX for CS papers, or self-contained HTML files with rich visual assets (math, charts, 3D, code). Also use for scientific/engineering documents with Bode plots, WaveDrom timing diagrams, SVG circuit schematics, SI units, or professional technical document layout."
---

# Science & Engineering Skill

## Overview

Unified reference for writing correct diagram/math/document markup and rendering it as self-contained HTML playgrounds opened in the user's browser. Covers syntax rules, rendering libraries, and scientific/engineering document authoring.

## Quick Reference

| Need | Reference | Renderer |
|------|-----------|----------|
| Flowcharts, sequence, ER, state, gantt, etc. | <MERMAID.md> | Mermaid.js |
| Directed/undirected graphs (DOT language) | <GRAPHVIZ.md> | Viz.js (@viz-js/viz) |
| CS paper LaTeX, algorithms, theorems | <LATEX.md> | KaTeX (simple) or MathJax (full) |
| CDN imports, version pins, all renderers | <RENDERERS.md> | — |
| Sci/eng docs: circuits, Bode plots, WaveDrom, SI units | <SCIENG.md> | MathJax + Plotly + WaveDrom + SVG |
| Data charts, scientific plots, 3D, code highlighting | <RENDERERS.md> | Chart.js / Plotly / D3 / Three.js / Highlight.js |

## When NOT to Use

- Pure terminal text output with no visualization needed
- User already has a rendering pipeline (e.g., local LaTeX install, Mermaid CLI)
- Simple inline code block -- just use markdown fenced blocks

## Core Workflow

1. Identify required renderers from the user's request.
2. Consult the syntax reference (<MERMAID.md>, <GRAPHVIZ.md>, <LATEX.md>).
3. Select CDN imports and the HTML skeleton template from <RENDERERS.md>.
4. For sci/eng documents, follow patterns in <SCIENG.md>.
5. Compose the HTML file. Include only libraries actually needed.
6. Write the file to the working directory.
7. Open in browser: `start <filename>.html` (Windows), `open <filename>.html` (macOS), or `xdg-open <filename>.html` (Linux).

## Renderer Content Patterns

### Mermaid

Wrap diagrams in `<pre class="mermaid">` blocks. See <MERMAID.md> for syntax rules.

```html
<pre class="mermaid">
graph TD
  A[Start] --> B{Decision}
  B -->|Yes| C[Action]
  B -->|No| D[Other Action]
</pre>
```

### KaTeX

Use `$$ ... $$` (display) and `\( ... \)` (inline). See <LATEX.md> for syntax.

```html
<p>The quadratic formula is $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$</p>
```

Switch to MathJax when the user needs `\newcommand` across blocks, `\begin{align}`, `\ce{}` chemistry, or `\qty{}` physics. See <RENDERERS.md> for MathJax config, or <SCIENG.md> for a complete engineering setup.

### Graphviz

Render DOT strings via Viz.js. See <GRAPHVIZ.md> for DOT syntax rules, <RENDERERS.md> for layout engines.

```html
<div id="graph"></div>
<script>
  Viz.instance().then(viz => {
    document.getElementById('graph').appendChild(
      viz.renderSVGElement('digraph { rankdir=LR; A -> B -> C; }')
    );
  });
</script>
```

### SVG

Embed directly. No library needed. For circuit schematics with `<defs>`/`<use>` symbol libraries, see <SCIENG.md>.

## Rendering to SVG (Standalone)

Three utility scripts render markup to SVG files without local installs:

| Script | Input | API Used |
|--------|-------|----------|
| `render-latex-to-svg.js` | `.tex` file | latex.codecogs.com |
| `render-dot-to-svg.js` | `.dot` file | quickchart.io/graphviz |
| `render-mermaid-to-svg.js` | `.mmd` file | mermaid.ink |

Usage: `node <script> <input> [output.svg]`

## Common Pitfalls

- **KaTeX `renderMathInElement` undefined**: Forgetting `defer` on scripts or no `DOMContentLoaded` listener.
- **Mermaid not rendering dynamic content**: Use `mermaid.run({ querySelector: '.mermaid' })` instead of `startOnLoad` for injected diagrams.
- **Viz.js synchronous call**: `Viz.instance()` is async. Always use `.then()` or `await`.
- **Dollar sign conflicts**: Prefer `\(...\)` for inline math if the document has currency `$` amounts.
- **Three.js r128 limits**: No `CapsuleGeometry`, no `OrbitControls`. Use `CylinderGeometry`/`SphereGeometry` and manual camera controls.

## Dependencies

All libraries load from CDN at runtime. No installation required. For the library size/compatibility matrix, see <RENDERERS.md>.
