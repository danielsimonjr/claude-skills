# Renderer Reference

Complete CDN imports, version-pinned configurations, and usage patterns for all supported rendering engines.

## Contents

- HTML playground skeleton template
- Mermaid.js (diagrams)
- KaTeX (math — default)
- MathJax (math — full-featured alternative)
- Viz.js (Graphviz/DOT)
- D3.js (custom visualizations)
- Plotly.js (scientific/interactive plots)
- Chart.js (lightweight charts)
- Three.js (3D/WebGL)
- Highlight.js (syntax highlighting)
- Interactive playground pattern
- Library compatibility matrix

-----

## HTML Playground Skeleton

Every playground follows this template. Remove renderer imports not needed for the task.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>

  <!-- KaTeX (math) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/contrib/auto-render.min.js"></script>

  <!-- Mermaid (diagrams) -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>

  <!-- Viz.js (Graphviz/DOT) -->
  <script src="https://unpkg.com/@viz-js/viz"></script>

  <!-- Highlight.js (syntax highlighting) -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/github-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>

  <style>
    :root { --bg: #1a1a2e; --fg: #e0e0e0; --accent: #00d2ff; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--fg); padding: 2rem; }
    .mermaid { background: transparent; }
    .katex-display { margin: 1.5rem 0; }
    pre code { border-radius: 8px; padding: 1rem; }
  </style>
</head>
<body>

  <!-- Content sections here -->

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      // Mermaid
      if (typeof mermaid !== 'undefined') {
        mermaid.initialize({ startOnLoad: true, theme: 'dark' });
      }
      // KaTeX auto-render
      if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(document.body, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '\\(', right: '\\)', display: false },
            { left: '\\[', right: '\\]', display: true }
          ]
        });
      }
      // Highlight.js
      if (typeof hljs !== 'undefined') { hljs.highlightAll(); }
    });
  </script>
</body>
</html>
```

-----

## Mermaid.js

**CDN import:**

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
```

**Initialization:**

```javascript
mermaid.initialize({
  startOnLoad: true,       // auto-render <pre class="mermaid"> blocks
  theme: 'dark',           // 'default' | 'dark' | 'forest' | 'neutral'
  securityLevel: 'loose',  // required for HTML/click in nodes
  fontFamily: 'system-ui, sans-serif',
  logLevel: 'error'        // 'debug' | 'info' | 'warn' | 'error' | 'fatal'
});
```

**Dynamic rendering** (for diagrams injected after page load):

```javascript
await mermaid.run({ querySelector: '.mermaid' });
```

**Supported diagram types:** flowchart/graph, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram, gantt, pie, gitGraph, mindmap, timeline, quadrantChart, sankey-beta, xychart-beta, block-beta, packet-beta, kanban, architecture-beta.

**Size:** ~800KB minified. CDN recommended.

-----

## KaTeX

Fast client-side LaTeX math rendering. Default choice for math equations.

**CDN imports** (all three required for auto-render):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body);"></script>
```

**Auto-render configuration:**

```javascript
renderMathInElement(document.body, {
  delimiters: [
    { left: '$$', right: '$$', display: true },
    { left: '\\[', right: '\\]', display: true },
    { left: '\\(', right: '\\)', display: false }
  ],
  throwOnError: false,
  trust: true
});
```

**Render single element:**

```javascript
katex.render('E = mc^2', document.getElementById('formula'), { displayMode: true });
```

**KaTeX limitations** (use MathJax if these are needed):

- No `\newcommand` persistence across separate render calls
- Limited `\begin{align}` support (use `\begin{aligned}` inside `$$` instead)
- No `physics`, `mhchem`, or `siunitx` packages
- No `\operatorname*`

**Size:** ~300KB (CSS + JS). Small enough to inline for offline use.

-----

## MathJax

Complete LaTeX math rendering with broad package support. Use when KaTeX’s coverage is insufficient.

**CDN import:**

```html
<script>
  MathJax = {
    tex: {
      inlineMath: [['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']],
      packages: {'[+]': ['ams', 'physics', 'mhchem']}
    },
    svg: { fontCache: 'global' },
    startup: { typeset: true }
  };
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
```

**Re-render after dynamic content injection:**

```javascript
MathJax.typesetPromise();
```

**When to use over KaTeX:** `\newcommand` across blocks, `\begin{align}`, `\ce{}` (chemistry), `\qty{}` (physics), AMS math environments, or advanced LaTeX packages.

**Size:** ~1.5MB. Noticeably slower initial render than KaTeX.

-----

## Viz.js (@viz-js/viz)

WebAssembly port of Graphviz. Renders DOT language graphs in the browser.

**CDN import:**

```html
<script src="https://unpkg.com/@viz-js/viz"></script>
```

**Render to SVG element (recommended):**

```javascript
Viz.instance().then(viz => {
  const svg = viz.renderSVGElement(`
    digraph G {
      rankdir=LR;
      node [shape=box, style="rounded,filled", fillcolor="#2d2d44",
            fontcolor="#e0e0e0", color="#00d2ff"];
      edge [color="#666"];
      A [label="Input"];
      B [label="Process"];
      C [label="Output"];
      A -> B -> C;
    }
  `);
  document.getElementById('graph-container').appendChild(svg);
});
```

**Render to SVG string:**

```javascript
Viz.instance().then(viz => {
  const svgString = viz.renderString('digraph { A -> B }', { format: 'svg' });
  document.getElementById('container').innerHTML = svgString;
});
```

**Layout engines:** `dot` (default, hierarchical), `neato` (spring model), `fdp` (force-directed), `sfdp` (scalable force-directed), `circo` (circular), `twopi` (radial), `osage` (clustered), `patchwork` (treemap).

Specify engine: `viz.renderSVGElement(dotSource, { engine: 'neato' });`

**CRITICAL:** `Viz.instance()` is asynchronous. Always use `.then()` or `await`. No synchronous API exists.

**Size:** ~3–5MB (includes WASM binary). Always use CDN. Do not inline.

-----

## D3.js

Low-level data visualization library for custom interactive charts, force-directed layouts, maps, and tree diagrams.

**CDN import:**

```html
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
```

**Basic usage:**

```javascript
const svg = d3.select('#chart').append('svg')
  .attr('width', 800).attr('height', 400);

svg.selectAll('rect')
  .data(dataset)
  .join('rect')
  .attr('x', (d, i) => i * 40)
  .attr('y', d => 400 - d.value * 4)
  .attr('width', 35)
  .attr('height', d => d.value * 4)
  .attr('fill', 'var(--accent)');
```

**Dark theme configuration:**

```javascript
// Apply dark theme to axes and gridlines
svg.selectAll('.tick text').attr('fill', '#999');
svg.selectAll('.tick line').attr('stroke', '#333');
svg.selectAll('.domain').attr('stroke', '#333');
```

**Size:** ~280KB minified. Small enough to inline for offline use.

-----

## Plotly.js

High-level interactive scientific charting with zoom, pan, hover tooltips, and export.

**CDN import:**

```html
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
```

**Basic usage:**

```javascript
Plotly.newPlot('chart', [{
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  type: 'scatter',
  mode: 'lines+markers'
}], {
  paper_bgcolor: 'rgba(0,0,0,0)',  // transparent background
  plot_bgcolor: 'rgba(0,0,0,0)',
  font: { color: '#e0e0e0' },
  xaxis: { gridcolor: '#333' },
  yaxis: { gridcolor: '#333' }
});
```

**Size:** ~3.5MB. CDN only — do not inline.

-----

## Chart.js

Lightweight responsive charting for bar, line, pie, radar, doughnut, and polar area charts.

**CDN import:**

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
```

**Basic usage:**

```javascript
new Chart(document.getElementById('myChart'), {
  type: 'bar',
  data: {
    labels: ['A', 'B', 'C'],
    datasets: [{
      label: 'Values',
      data: [12, 19, 8],
      backgroundColor: '#00d2ff'
    }]
  },
  options: {
    plugins: { legend: { labels: { color: '#e0e0e0' } } },
    scales: {
      y: { ticks: { color: '#999' }, grid: { color: '#333' } },
      x: { ticks: { color: '#999' }, grid: { color: '#333' } }
    }
  }
});
```

**Size:** ~200KB. Small enough to inline for offline use.

-----

## Three.js (WebGL / 3D)

3D rendering for mathematical surfaces, molecular structures, architectural models, and interactive scenes.

**CDN import:**

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

**IMPORTANT:** r128 is the last version on the Cloudflare CDN. Do NOT use `THREE.CapsuleGeometry` (introduced in r142). Use `CylinderGeometry`, `SphereGeometry`, or custom geometry. `OrbitControls` and other add-ons are unavailable on this CDN — implement camera controls manually if needed.

**Basic scene setup:**

```javascript
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('scene').appendChild(renderer.domElement);

// Geometry + material
const geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
const material = new THREE.MeshStandardMaterial({
  color: 0x00d2ff, metalness: 0.7, roughness: 0.2
});
scene.add(new THREE.Mesh(geometry, material));

// Lighting
scene.add(new THREE.DirectionalLight(0xffffff, 1).position.set(5, 5, 5));
scene.add(new THREE.AmbientLight(0x404040));

// Render loop
camera.position.z = 4;
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();
```

**Size:** ~600KB. CDN recommended.

-----

## Highlight.js

Syntax highlighting for code blocks. Supports 180+ languages with automatic detection.

**CDN imports:**

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>
```

Wrap code in `<pre><code class="language-python">...</code></pre>` and call `hljs.highlightAll()` after DOM load.

**Available dark themes:** `github-dark`, `atom-one-dark`, `monokai`, `nord`, `dracula`, `tokyo-night-dark`, `vs2015`.

**Size:** ~50KB core + ~5KB per language. Very lightweight.

-----

## Interactive Playground Pattern

For playgrounds with user-adjustable parameters (sliders, dropdowns, presets), follow this pattern:

**Central state + instant update:**

```javascript
const state = {
  param1: 1.0,
  param2: 'option-a',
  // ... all configurable values with sensible defaults
};

function updateAll() {
  renderPreview();   // re-render visual output (chart, diagram, 3D scene)
  updateOutput();    // update any text/numeric output panels
}

// Every control calls updateAll() on change — no "Apply" button
document.querySelectorAll('input, select').forEach(el => {
  el.addEventListener('input', () => {
    state[el.dataset.param] = el.type === 'range' ? parseFloat(el.value) : el.value;
    updateAll();
  });
});
```

**Guidelines:**

- **Dark theme**: Use `--bg: #1a1a2e`, `--fg: #e0e0e0`, `--accent: #00d2ff` (from the skeleton template).
- **Presets**: Provide 3–5 named presets (buttons or dropdown) that set `state` to interesting configurations and call `updateAll()`.
- **Live preview**: Every parameter change triggers an immediate re-render. No "Submit" or "Apply" buttons.
- **Layout**: Place controls in a sidebar or top bar; reserve the main area for the visualization.

-----

## Library Compatibility Matrix

All listed libraries coexist in a single HTML file. No known conflicts, with one caveat: if using both KaTeX and MathJax (unusual), ensure delimiter configurations do not overlap.

|Renderer    |Size (approx.)|Inline feasible?|Async init?       |
|------------|--------------|----------------|------------------|
|KaTeX       |~300KB        |Yes             |No (use `defer`)  |
|MathJax     |~1.5MB        |No              |Yes               |
|Mermaid     |~800KB        |Marginal        |No (`startOnLoad`)|
|Viz.js      |~3–5MB        |No              |Yes (`.then()`)   |
|D3.js       |~280KB        |Yes             |No                |
|Plotly.js   |~3.5MB        |No              |No                |
|Chart.js    |~200KB        |Yes             |No                |
|Three.js    |~600KB        |Marginal        |No                |
|Highlight.js|~50KB         |Yes             |No                |