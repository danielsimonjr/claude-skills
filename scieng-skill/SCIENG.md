# Scientific & Engineering Document Reference

## Contents

- [MathJax Engineering Configuration](#mathjax-engineering-configuration)
- [SI Units and Physical Quantities](#si-units-and-physical-quantities)
- [Engineering Notation Macros](#engineering-notation-macros)
- [WaveDrom Timing Diagrams](#wavedrom-timing-diagrams)
- [SVG Circuit Schematics](#svg-circuit-schematics)
- [Control Systems Plotting](#control-systems-plotting)
- [Signal Processing Visualizations](#signal-processing-visualizations)
- [Systems Engineering Diagrams](#systems-engineering-diagrams)
- [Document Structure and Typography](#document-structure-and-typography)
- [Cross-Referencing System](#cross-referencing-system)
- [Multi-Panel Figure Layouts](#multi-panel-figure-layouts)
- [Data Tables with Uncertainty](#data-tables-with-uncertainty)
- [Complete Document Skeleton](#complete-document-skeleton)
- [Domain Quick Reference](#domain-quick-reference)

-----

## MathJax Engineering Configuration

Use MathJax (not KaTeX) when the document requires any of: `\ce{}` chemistry, `\SI{}` unit notation, `\begin{align}` environments, cross-referenced equation numbering, `\newcommand` macros across blocks, or the `physics` package bracket notation. MathJax v3 is the required version. Load the `mhchem` extension from the MathJax core; `siunitx` and `physics` require third-party extension hosting or custom macros (see below).

### CDN Import

```html
<!-- MathJax v3 with TeX-to-CHTML output, mhchem, and equation numbering -->
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']],
      packages: {'[+]': ['mhchem', 'ams']},
      tags: 'ams',          // auto-number display equations (\begin{equation})
      tagSide: 'right',
      macros: {}             // populated below per domain
    },
    loader: {
      load: ['[tex]/mhchem', '[tex]/ams']
    },
    chtml: {
      scale: 1.0,
      minScale: 0.5,
      mtextInheritFont: true // body font for \text{} blocks
    }
  };
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>
```

**Critical**: Never mix KaTeX and MathJax in the same document. Choose one. If any sci/eng feature below is needed, choose MathJax.

**Delimiter safety**: Use `\(...\)` for inline math, never `$...$`, to avoid conflicts with currency symbols, shell variables, and template literals.

### Equation Numbering

MathJax AMS tagging auto-numbers `\begin{equation}` environments and allows `\label{}`/`\eqref{}` cross-references:

```html
<p>The transfer function is</p>
$$\begin{equation}
  H(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}
  \label{eq:secondorder}
\end{equation}$$
<p>As shown in \(\eqref{eq:secondorder}\), the system has two poles.</p>
```

Use `\begin{align}` for multi-line derivations and `\notag` to suppress numbering on intermediate lines:

```latex
\begin{align}
  V_{out} &= A_{OL}(V^+ - V^-) \label{eq:opamp-ideal} \\
          &= A_{OL}\left(V_{in} - \frac{R_1}{R_1 + R_2} V_{out}\right) \notag \\
  \frac{V_{out}}{V_{in}} &= \frac{A_{OL}}{1 + A_{OL}\beta} \label{eq:closedloop}
\end{align}
```

-----

## SI Units and Physical Quantities

MathJax v3 does not natively ship `siunitx`. Define lightweight macros that cover the most common cases. Place these in the `macros` object of your MathJax configuration.

### Minimal SI Macro Set

```javascript
macros: {
  // \SI{value}{unit} — physical quantity with value and unit
  SI: ['{#1}\\;{\\mathrm{#2}}', 2],
  // \si{unit} — standalone unit (no value)
  si: ['{\\mathrm{#1}}', 1],
  // \num{value} — formatted number
  num: ['{#1}', 1],
  // Convenience unit macros
  ohm:     '\\Omega',
  kohm:    '{\\mathrm{k\\Omega}}',
  mohm:    '{\\mathrm{M\\Omega}}',
  uF:      '{\\mu\\mathrm{F}}',
  nF:      '{\\mathrm{nF}}',
  pF:      '{\\mathrm{pF}}',
  mH:      '{\\mathrm{mH}}',
  uH:      '{\\mu\\mathrm{H}}',
  MHz:     '{\\mathrm{MHz}}',
  kHz:     '{\\mathrm{kHz}}',
  GHz:     '{\\mathrm{GHz}}',
  dBm:     '{\\mathrm{dBm}}',
  dB:      '{\\mathrm{dB}}',
  Vpp:     '{\\mathrm{V_{pp}}}',
  Vrms:    '{\\mathrm{V_{rms}}}',
  Arms:    '{\\mathrm{A_{rms}}}',
  mA:      '{\\mathrm{mA}}',
  uA:      '{\\mu\\mathrm{A}}',
  nA:      '{\\mathrm{nA}}',
  mW:      '{\\mathrm{mW}}',
  kW:      '{\\mathrm{kW}}',
  ns:      '{\\mathrm{ns}}',
  us:      '{\\mu\\mathrm{s}}',
  ms:      '{\\mathrm{ms}}',
  // Per-unit construction
  per:     '{\\,/\\,}'
}
```

### Usage

```latex
The input impedance is \(\SI{10}{k\Omega}\) with a bandwidth of \(\SI{3.2}{MHz}\).

The slew rate is \(\SI{13}{V/\mu s}\) and the offset voltage is \(\SI{2.5}{mV}\).

Output power: \(\SI{-10}{dBm}\) at \(\SI{50}{\ohm}\) load.
```

For documents requiring strict `siunitx` compatibility (per-mode, number formatting, uncertainty), generate the quantities server-side with Python/LaTeX and embed them as static HTML, or use MathJax v2 with the third-party `siunitx.js` extension from `https://github.com/burnpanck/MathJax-siunitx`.

-----

## Engineering Notation Macros

Add domain-specific macro sets to the MathJax `macros` configuration. Each set below is additive — merge what you need.

### Electrical Engineering

```javascript
// Phasors, complex impedance, transforms
phasor:     ['\\tilde{#1}', 1],
conj:       ['{#1}^{*}', 1],
magn:       ['\\left|#1\\right|', 1],
phase:      ['\\angle{#1}', 1],
parallelop: '{\\,\\|\\,}',
laplace:    ['\\mathcal{L}\\left\\{#1\\right\\}', 1],
invlaplace: ['\\mathcal{L}^{-1}\\left\\{#1\\right\\}', 1],
fourier:    ['\\mathcal{F}\\left\\{#1\\right\\}', 1],
ztransform: ['\\mathcal{Z}\\left\\{#1\\right\\}', 1],
```

### Control Systems

```javascript
// Transfer functions and system analysis
tf:        ['\\frac{#1}{#2}', 2],           // shorthand: \tf{N(s)}{D(s)}
openloop:  '{G_{OL}(s)}',
closedloop:'{G_{CL}(s)}',
plant:     '{G_p(s)}',
controller:'{G_c(s)}',
feedback:  '{H(s)}',
natfreq:   '{\\omega_n}',
damprat:   '{\\zeta}',
phasemargin:'{\\phi_m}',
gainmargin: '{GM}',
bandwidth:  '{\\omega_{BW}}',
stepresponse: '{y_{step}(t)}',
```

### Semiconductor / Electronics

```javascript
// Device parameters and models
Vth:   '{V_{\\mathrm{th}}}',
Vgs:   '{V_{\\mathrm{GS}}}',
Vds:   '{V_{\\mathrm{DS}}}',
Vbe:   '{V_{\\mathrm{BE}}}',
Vce:   '{V_{\\mathrm{CE}}}',
Ic:    '{I_{\\mathrm{C}}}',
Ib:    '{I_{\\mathrm{B}}}',
Id:    '{I_{\\mathrm{D}}}',
gm:    '{g_m}',
rds:   '{r_{\\mathrm{ds}}}',
ro:    '{r_o}',
beta:  '{\\beta}',
hfe:   '{h_{\\mathrm{FE}}}',
Cgs:   '{C_{\\mathrm{GS}}}',
Cgd:   '{C_{\\mathrm{GD}}}',
fT:    '{f_T}',
CMRR:  '{\\mathrm{CMRR}}',
PSRR:  '{\\mathrm{PSRR}}',
SNR:   '{\\mathrm{SNR}}',
THD:   '{\\mathrm{THD}}',
BER:   '{\\mathrm{BER}}',
```

### Systems Engineering

```javascript
// Requirements, metrics, and analysis
MTBF:    '{\\mathrm{MTBF}}',
MTTR:    '{\\mathrm{MTTR}}',
availability: '{A_o}',
reliability: ['{R(#1)}', 1],
failure: ['{\\lambda_{#1}}', 1],
prob:    ['P\\left(#1\\right)', 1],
expect:  ['E\\left[#1\\right]', 1],
variance:['\\mathrm{Var}\\left[#1\\right]', 1],
```

-----

## WaveDrom Timing Diagrams

WaveDrom renders digital timing waveforms from JSON descriptions. Essential for digital logic, bus protocols, clocking, state machines, and interface timing specifications.

### CDN Import

```html
<!-- WaveDrom v3.1.0 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.1.0/skins/default.js"
        type="text/javascript"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.1.0/wavedrom.min.js"
        type="text/javascript"></script>
```

### Initialization

```javascript
document.addEventListener('DOMContentLoaded', () => {
  if (typeof WaveDrom !== 'undefined') {
    WaveDrom.ProcessAll();
  }
});
```

### Embedding Diagrams

Wrap WaveJSON in a `<script type="WaveDrom">` tag:

```html
<figure class="figure" id="fig-spi-timing">
  <script type="WaveDrom">
  { "signal": [
    { "name": "SCLK",  "wave": "p........" },
    { "name": "MOSI",  "wave": "x.345678x", "data": ["B7","B6","B5","B4","B3","B2","B1","B0"] },
    { "name": "MISO",  "wave": "x.345678x", "data": ["Q7","Q6","Q5","Q4","Q3","Q2","Q1","Q0"] },
    { "name": "SS_n",  "wave": "10.......1" }
  ],
    "config": { "hscale": 2 }
  }
  </script>
  <figcaption></figcaption>
</figure>
```

### WaveJSON Signal Characters

|Char   |Meaning               |Char|Meaning               |
|-------|----------------------|----|----------------------|
|`p`    |Positive clock edge   |`n` |Negative clock edge   |
|`P`    |Positive clock (arrow)|`N` |Negative clock (arrow)|
|`0`    |Low                   |`1` |High                  |
|`x`    |Undefined / don’t care|`z` |High impedance        |
|`=`    |Bus value (from data) |`.` |Continue previous     |
|`2`–`9`|Named data values     |`u` |Pull-up (weak 1)      |
|`d`    |Pull-down (weak 0)    |`l` |Low (same as 0)       |
|`h`    |High (same as 1)      |    |                      |

### Grouping and Gaps

```json
{ "signal": [
  ["SPI Master",
    { "name": "SCLK", "wave": "p...." },
    { "name": "MOSI", "wave": "x345x" }
  ],
  {},
  ["SPI Slave",
    { "name": "MISO", "wave": "x345x" },
    { "name": "SS",   "wave": "10..1" }
  ]
]}
```

An empty object `{}` inserts a visual gap between signal groups. Array-wrapped groups produce labeled sections.

### Edge Annotations

Add timing relationships between signals using the `edge` array:

```json
{
  "signal": [
    { "name": "clk",  "wave": "p......",  "node": ".a...e." },
    { "name": "data", "wave": "x.3.x..",  "node": "..b.d.." },
    { "name": "ack",  "wave": "0..1.0.",  "node": "...c..." }
  ],
  "edge": [
    "a~b t_setup",
    "c-~>d t_hold",
    "a<~>e T_clk"
  ]
}
```

Edge arrow types: `->` sharp, `~>` curved, `-~>` start-sharp end-curved, `<->` bidirectional. Labels follow the arrow specification after a space.

### Dark Theme Override

WaveDrom renders with a white background by default. Override with CSS:

```css
/* Invert WaveDrom for dark backgrounds */
.wavedrom-container svg { background: transparent !important; }
.wavedrom-container text { fill: #e0e0e0 !important; }
.wavedrom-container path,
.wavedrom-container line,
.wavedrom-container rect[fill="white"] { fill: transparent !important; }
```

Alternatively, set `"config": { "skin": "narrow" }` for a more compact rendering. For full dark-theme integration, render into a light-background container instead:

```css
.wavedrom-container {
  background: #f8f8f8;
  border-radius: 8px;
  padding: 1rem;
  margin: 1.5rem 0;
}
```

-----

## SVG Circuit Schematics

For circuit schematics in self-contained HTML, use inline SVG with a reusable symbol library defined in a `<defs>` block. This approach requires no external libraries, works offline, renders at any resolution, and produces publication-quality results.

### Symbol Library Pattern

Define symbols once in `<defs>`, instantiate with `<use>`. All symbols sit on a 100-unit grid (each grid unit = 1px at default scale). Terminal connection points are at grid-aligned coordinates for clean wiring.

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"
     style="width:100%; max-width:800px; background:transparent;">
  <defs>
    <!-- Resistor (horizontal, 100x20, terminals at x=0 and x=100) -->
    <symbol id="sym-resistor" viewBox="0 0 100 20" overflow="visible">
      <path d="M0,10 L20,10 L25,0 L35,20 L45,0 L55,20 L65,0 L75,20 L80,10 L100,10"
            fill="none" stroke="currentColor" stroke-width="2"
            stroke-linejoin="round"/>
    </symbol>

    <!-- Capacitor (horizontal, 100x30, terminals at x=0 and x=100) -->
    <symbol id="sym-capacitor" viewBox="0 0 100 30" overflow="visible">
      <line x1="0" y1="15" x2="42" y2="15" stroke="currentColor" stroke-width="2"/>
      <line x1="42" y1="0"  x2="42" y2="30" stroke="currentColor" stroke-width="2"/>
      <line x1="58" y1="0"  x2="58" y2="30" stroke="currentColor" stroke-width="2"/>
      <line x1="58" y1="15" x2="100" y2="15" stroke="currentColor" stroke-width="2"/>
    </symbol>

    <!-- Inductor (horizontal, 100x20, terminals at x=0 and x=100) -->
    <symbol id="sym-inductor" viewBox="0 0 100 20" overflow="visible">
      <path d="M0,15 L15,15 Q25,15 25,5 Q25,-5 35,5 Q35,15 45,15
               Q45,15 45,5 Q45,-5 55,5 Q55,15 65,15
               Q65,15 65,5 Q65,-5 75,5 Q75,15 85,15 L100,15"
            fill="none" stroke="currentColor" stroke-width="2"/>
    </symbol>

    <!-- Ground (20x20, terminal at top center x=10, y=0) -->
    <symbol id="sym-ground" viewBox="0 0 20 20" overflow="visible">
      <line x1="10" y1="0"  x2="10" y2="8"  stroke="currentColor" stroke-width="2"/>
      <line x1="0"  y1="8"  x2="20" y2="8"  stroke="currentColor" stroke-width="2"/>
      <line x1="3"  y1="12" x2="17" y2="12" stroke="currentColor" stroke-width="2"/>
      <line x1="6"  y1="16" x2="14" y2="16" stroke="currentColor" stroke-width="2"/>
    </symbol>

    <!-- Op-Amp (100x80, inv(-) at y=20, non-inv(+) at y=60, out at x=100,y=40) -->
    <symbol id="sym-opamp" viewBox="0 0 100 80" overflow="visible">
      <polygon points="10,0 10,80 90,40" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
      <line x1="0"   y1="20" x2="10"  y2="20" stroke="currentColor" stroke-width="2"/>
      <line x1="0"   y1="60" x2="10"  y2="60" stroke="currentColor" stroke-width="2"/>
      <line x1="90"  y1="40" x2="100" y2="40" stroke="currentColor" stroke-width="2"/>
      <text x="18" y="25" font-size="14" fill="currentColor">−</text>
      <text x="18" y="65" font-size="14" fill="currentColor">+</text>
    </symbol>

    <!-- NMOS (60x60, gate at x=0,y=30, drain at x=40,y=0, source at x=40,y=60) -->
    <symbol id="sym-nmos" viewBox="0 0 60 60" overflow="visible">
      <line x1="0"  y1="30" x2="15" y2="30" stroke="currentColor" stroke-width="2"/>
      <line x1="15" y1="10" x2="15" y2="50" stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="10" x2="20" y2="22" stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="26" x2="20" y2="34" stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="38" x2="20" y2="50" stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="15" x2="40" y2="15" stroke="currentColor" stroke-width="2"/>
      <line x1="40" y1="0"  x2="40" y2="15" stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="45" x2="40" y2="45" stroke="currentColor" stroke-width="2"/>
      <line x1="40" y1="45" x2="40" y2="60" stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="30" x2="40" y2="30" stroke="currentColor" stroke-width="2"/>
      <!-- Arrow on source -->
      <polygon points="30,30 25,26 25,34" fill="currentColor" stroke="none"/>
    </symbol>

    <!-- Voltage source (circle, 40x40, terminals at x=20,y=0 and x=20,y=40) -->
    <symbol id="sym-vsource" viewBox="0 0 40 40" overflow="visible">
      <circle cx="20" cy="20" r="18" fill="none"
              stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="0"  x2="20" y2="2"  stroke="currentColor" stroke-width="2"/>
      <line x1="20" y1="38" x2="20" y2="40" stroke="currentColor" stroke-width="2"/>
      <text x="14" y="16" font-size="12" fill="currentColor">+</text>
      <text x="14" y="32" font-size="12" fill="currentColor">−</text>
    </symbol>

    <!-- Diode (horizontal, 60x20, anode at x=0, cathode at x=60) -->
    <symbol id="sym-diode" viewBox="0 0 60 20" overflow="visible">
      <line x1="0"  y1="10" x2="20" y2="10" stroke="currentColor" stroke-width="2"/>
      <polygon points="20,0 20,20 40,10" fill="none"
               stroke="currentColor" stroke-width="2"/>
      <line x1="40" y1="0"  x2="40" y2="20" stroke="currentColor" stroke-width="2"/>
      <line x1="40" y1="10" x2="60" y2="10" stroke="currentColor" stroke-width="2"/>
    </symbol>

    <!-- Junction dot (connection point) -->
    <symbol id="sym-junction" viewBox="0 0 8 8" overflow="visible">
      <circle cx="4" cy="4" r="3" fill="currentColor"/>
    </symbol>
  </defs>

  <!-- Usage example: place components and wire them -->
  <g transform="translate(100,100)" color="#e0e0e0">
    <use href="#sym-resistor" x="0" y="0" width="100" height="20"/>
    <text x="50" y="-5" text-anchor="middle" font-size="12"
          fill="currentColor">R₁ = 10 kΩ</text>
  </g>
</svg>
```

### Wiring Pattern

Draw wires as `<line>` or `<polyline>` elements connecting symbol terminal coordinates. Use `stroke-linejoin="round"` for clean bends. Place `<use href="#sym-junction"/>` at every T-junction or crossing where wires connect.

```html
<!-- Horizontal wire from R1 output to C1 input -->
<line x1="200" y1="110" x2="300" y2="110"
      stroke="currentColor" stroke-width="2"/>
<!-- Right-angle wire -->
<polyline points="200,110 200,200 300,200"
          fill="none" stroke="currentColor" stroke-width="2"
          stroke-linejoin="round"/>
```

### Component Label Convention

Place component designators (R1, C1, U1) and values using `<text>` elements. Position labels 5–10 units above horizontal components or 10 units to the right of vertical components. Use `text-anchor="middle"` and align to the component center.

### Extended Symbols

For components not in the base library (Zener diodes, Schottky diodes, PNP transistors, PMOS, transformers, crystals, LEDs, potentiometers, switches, fuses, relays), define additional `<symbol>` elements following the same grid conventions. Terminal points must land on integer multiples of the grid unit.

-----

## Control Systems Plotting

Bode plots, Nyquist plots, root locus diagrams, and step/impulse response curves all use Plotly.js with log-scale axis configuration.

### Bode Plot (Magnitude + Phase)

Generate frequency response data in JavaScript, then plot with dual-subplot layout:

```html
<div id="bode-plot" style="width:100%; height:500px;"></div>
<script>
  // Second-order system: H(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
  const wn = 100;       // natural frequency (rad/s)
  const zeta = 0.3;     // damping ratio

  // Frequency sweep: 0.1 to 10000 rad/s, 500 log-spaced points
  const fMin = 0.1, fMax = 10000, N = 500;
  const omega = Array.from({length: N}, (_, i) =>
    fMin * Math.pow(fMax / fMin, i / (N - 1))
  );

  // Compute H(jw)
  const magDB = [], phaseDeg = [];
  for (const w of omega) {
    const reNum = wn * wn - w * w;   // Re{numerator} when num = wn^2
    const imNum = 0;
    const reDen = wn * wn - w * w;
    const imDen = 2 * zeta * wn * w;
    const denMagSq = reDen * reDen + imDen * imDen;

    const reH = (reNum * reDen + imNum * imDen) / denMagSq;
    const imH = (imNum * reDen - reNum * imDen) / denMagSq;

    const mag = Math.sqrt(reH * reH + imH * imH);
    magDB.push(20 * Math.log10(mag));
    phaseDeg.push(Math.atan2(imH, reH) * 180 / Math.PI);
  }

  // Plotly subplots
  const traceMag = {
    x: omega, y: magDB, type: 'scatter', mode: 'lines',
    name: '|H(jω)|', line: { color: '#00d2ff', width: 2 },
    xaxis: 'x', yaxis: 'y'
  };
  const tracePhase = {
    x: omega, y: phaseDeg, type: 'scatter', mode: 'lines',
    name: '∠H(jω)', line: { color: '#ff6b6b', width: 2 },
    xaxis: 'x2', yaxis: 'y2'
  };

  const layout = {
    grid: { rows: 2, columns: 1, pattern: 'independent', roworder: 'top to bottom' },
    xaxis:  { type: 'log', title: '', showticklabels: false,
              gridcolor: '#333', linecolor: '#555' },
    yaxis:  { title: 'Magnitude (dB)', gridcolor: '#333', linecolor: '#555',
              titlefont: { color: '#e0e0e0' }, tickfont: { color: '#aaa' } },
    xaxis2: { type: 'log', title: 'Frequency (rad/s)',
              gridcolor: '#333', linecolor: '#555',
              titlefont: { color: '#e0e0e0' }, tickfont: { color: '#aaa' } },
    yaxis2: { title: 'Phase (deg)', gridcolor: '#333', linecolor: '#555',
              titlefont: { color: '#e0e0e0' }, tickfont: { color: '#aaa' } },
    paper_bgcolor: 'transparent', plot_bgcolor: '#0d1117',
    font: { color: '#e0e0e0' },
    showlegend: false,
    margin: { t: 30, b: 60, l: 70, r: 30 }
  };

  Plotly.newPlot('bode-plot', [traceMag, tracePhase], layout, {responsive: true});
</script>
```

### Gain and Phase Margin Annotations

After computing the Bode data, find the gain crossover (0 dB) and phase crossover (−180°) frequencies, then add Plotly `annotations` and `shapes` to mark them:

```javascript
// Find gain crossover: first frequency where |H| crosses 0 dB
let wGC = null, phaseAtGC = null;
for (let i = 1; i < N; i++) {
  if (magDB[i - 1] > 0 && magDB[i] <= 0) {
    wGC = omega[i];
    phaseAtGC = phaseDeg[i];
    break;
  }
}
const phaseMargin = phaseAtGC !== null ? 180 + phaseAtGC : null;

// Add as Plotly annotation
if (wGC) {
  layout.annotations = [{
    x: Math.log10(wGC), y: phaseAtGC,
    xref: 'x2', yref: 'y2',
    text: `PM = ${phaseMargin.toFixed(1)}°`,
    showarrow: true, arrowhead: 2,
    font: { color: '#4ecdc4', size: 12 },
    arrowcolor: '#4ecdc4'
  }];
}
```

### Root Locus

Use Plotly scatter mode to plot pole/zero migration in the s-plane:

```javascript
// Poles of H(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2) as zeta varies
const zetaRange = Array.from({length: 200}, (_, i) => i * 0.01 + 0.01);
const realParts = [], imagParts = [];
for (const z of zetaRange) {
  const sigma = -z * wn;
  const wd = wn * Math.sqrt(Math.abs(1 - z * z));
  if (z < 1) {
    realParts.push(sigma, sigma);
    imagParts.push(wd, -wd);
  } else {
    realParts.push(sigma + wd, sigma - wd);
    imagParts.push(0, 0);
  }
}

Plotly.newPlot('root-locus', [{
  x: realParts, y: imagParts, mode: 'markers',
  marker: { size: 2, color: '#00d2ff' },
  type: 'scatter'
}], {
  xaxis: { title: 'Real', zeroline: true, zerolinecolor: '#555', gridcolor: '#333' },
  yaxis: { title: 'Imaginary', zeroline: true, zerolinecolor: '#555', gridcolor: '#333',
           scaleanchor: 'x' },
  paper_bgcolor: 'transparent', plot_bgcolor: '#0d1117',
  font: { color: '#e0e0e0' }, margin: { t: 30 }
});
```

### Step Response

```javascript
// Second-order underdamped step response: y(t) = 1 - (e^(-sigma*t)/wd)*sin(wd*t + phi)
const sigma_d = zeta * wn;
const wd = wn * Math.sqrt(1 - zeta * zeta);
const phi = Math.acos(zeta);
const tMax = 5 / sigma_d;
const t = Array.from({length: 500}, (_, i) => i * tMax / 499);
const y = t.map(ti =>
  1 - (Math.exp(-sigma_d * ti) / Math.sqrt(1 - zeta * zeta))
      * Math.sin(wd * ti + phi)
);

Plotly.newPlot('step-response', [{
  x: t, y: y, mode: 'lines',
  line: { color: '#00d2ff', width: 2 }
}], {
  xaxis: { title: 'Time (s)', gridcolor: '#333' },
  yaxis: { title: 'Amplitude', gridcolor: '#333' },
  paper_bgcolor: 'transparent', plot_bgcolor: '#0d1117',
  font: { color: '#e0e0e0' },
  shapes: [{   // Steady-state line
    type: 'line', x0: 0, x1: tMax, y0: 1, y1: 1,
    line: { color: '#ff6b6b', width: 1, dash: 'dash' }
  }]
});
```

-----

## Signal Processing Visualizations

### FFT Spectrum Plot

```javascript
// Plot magnitude spectrum with Plotly
// Assume `samples` is a Float64Array and `fs` is the sample rate
function plotSpectrum(samples, fs, elementId) {
  const N = samples.length;
  // Use a basic DFT for small N, or include an FFT library for large N
  const freqs = Array.from({length: Math.floor(N/2)}, (_, k) => k * fs / N);
  const mags = freqs.map((_, k) => {
    let re = 0, im = 0;
    for (let n = 0; n < N; n++) {
      const angle = -2 * Math.PI * k * n / N;
      re += samples[n] * Math.cos(angle);
      im += samples[n] * Math.sin(angle);
    }
    return 20 * Math.log10(Math.sqrt(re * re + im * im) / N + 1e-12);
  });

  Plotly.newPlot(elementId, [{
    x: freqs, y: mags, mode: 'lines',
    line: { color: '#00d2ff', width: 1.5 }
  }], {
    xaxis: { title: 'Frequency (Hz)', gridcolor: '#333' },
    yaxis: { title: 'Magnitude (dB)', gridcolor: '#333' },
    paper_bgcolor: 'transparent', plot_bgcolor: '#0d1117',
    font: { color: '#e0e0e0' }, margin: { t: 20 }
  });
}
```

### Pole-Zero Plot

Use Plotly scatter with distinct markers for poles (×) and zeros (○):

```javascript
function plotPoleZero(poles, zeros, elementId) {
  const traces = [];
  if (zeros.length > 0) {
    traces.push({
      x: zeros.map(z => z.re), y: zeros.map(z => z.im),
      mode: 'markers', name: 'Zeros',
      marker: { symbol: 'circle-open', size: 12, color: '#4ecdc4', line: { width: 2 } }
    });
  }
  if (poles.length > 0) {
    traces.push({
      x: poles.map(p => p.re), y: poles.map(p => p.im),
      mode: 'markers', name: 'Poles',
      marker: { symbol: 'x', size: 12, color: '#ff6b6b', line: { width: 2 } }
    });
  }

  // Unit circle
  const theta = Array.from({length: 361}, (_, i) => i * Math.PI / 180);
  traces.push({
    x: theta.map(t => Math.cos(t)),
    y: theta.map(t => Math.sin(t)),
    mode: 'lines', name: 'Unit Circle',
    line: { color: '#555', width: 1, dash: 'dash' }
  });

  Plotly.newPlot(elementId, traces, {
    xaxis: { title: 'Real', zeroline: true, zerolinecolor: '#555',
             gridcolor: '#333', scaleanchor: 'y' },
    yaxis: { title: 'Imaginary', zeroline: true, zerolinecolor: '#555',
             gridcolor: '#333' },
    paper_bgcolor: 'transparent', plot_bgcolor: '#0d1117',
    font: { color: '#e0e0e0' }, margin: { t: 20 }
  });
}
```

-----

## Systems Engineering Diagrams

Use Mermaid for system-level diagrams. Sci/eng documents commonly require functional block diagrams, interface definition diagrams, state machines, and requirement traceability. Below are templates for each.

### Functional Block Diagram

```html
<pre class="mermaid">
graph LR
  subgraph Sensor["Sensor Subsystem"]
    S1[Accelerometer] --> SF[Signal Filter]
    S2[Gyroscope] --> SF
  end
  subgraph Processor["Processing Unit"]
    SF --> ADC[ADC 16-bit]
    ADC --> DSP[DSP Core]
    DSP --> KF[Kalman Filter]
  end
  subgraph Actuator["Actuation"]
    KF --> DAC[DAC]
    DAC --> Motor[Motor Driver]
  end
  subgraph Power["Power Management"]
    PSU[5V Supply] -.-> Sensor
    PSU -.-> Processor
    PSU -.-> Actuator
  end
</pre>
```

### State Machine (Protocol or Mode Transition)

```html
<pre class="mermaid">
stateDiagram-v2
  [*] --> IDLE
  IDLE --> ACQUIRING : Start Command
  ACQUIRING --> TRACKING : Lock Achieved
  ACQUIRING --> FAULT : Timeout
  TRACKING --> ACQUIRING : Lock Lost
  TRACKING --> IDLE : Stop Command
  FAULT --> IDLE : Reset
  FAULT --> [*] : Critical Failure
</pre>
```

### Interface Control

```html
<pre class="mermaid">
sequenceDiagram
  participant Host
  participant FPGA
  participant ADC
  participant DAC

  Host->>FPGA: SPI Config (Mode, Gain)
  FPGA->>ADC: Start Conversion
  ADC-->>FPGA: Data Ready (IRQ)
  FPGA->>ADC: Read 16-bit Sample
  FPGA->>FPGA: DSP Processing
  FPGA->>DAC: Write Output Sample
  FPGA-->>Host: Status Register (DMA)
</pre>
```

### Requirement Traceability (Lightweight)

```html
<pre class="mermaid">
graph TD
  REQ1["REQ-001<br/>System shall acquire<br/>signal within 100 ms"]
  REQ2["REQ-002<br/>SNR ≥ 40 dB at input"]
  REQ3["REQ-003<br/>Power ≤ 500 mW"]

  DES1["DES-001<br/>Use correlator<br/>with 1024-point FFT"]
  DES2["DES-002<br/>LNA NF < 2 dB"]
  DES3["DES-003<br/>3.3V SMPS<br/>with 92% efficiency"]

  TEST1["TST-001<br/>Acquisition time test"]
  TEST2["TST-002<br/>SNR measurement"]
  TEST3["TST-003<br/>Power consumption test"]

  REQ1 --> DES1 --> TEST1
  REQ2 --> DES2 --> TEST2
  REQ3 --> DES3 --> TEST3
</pre>
```

-----

## Document Structure and Typography

Scientific and engineering HTML documents require consistent typographic hierarchy, not the generic dark-theme body used for playground rendering.

### CSS Framework

```css
:root {
  --bg:      #0d1117;
  --fg:      #c9d1d9;
  --heading: #e6edf3;
  --accent:  #58a6ff;
  --caption: #8b949e;
  --border:  #30363d;
  --code-bg: #161b22;
  --serif:   'Charter', 'Bitstream Charter', 'STIX Two Text', Georgia, serif;
  --sans:    'Inter', system-ui, -apple-system, sans-serif;
  --mono:    'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
}

body {
  font-family: var(--serif);
  font-size: 16px;
  line-height: 1.7;
  color: var(--fg);
  background: var(--bg);
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* ── Headings ── */
h1, h2, h3, h4 { font-family: var(--sans); color: var(--heading); margin-top: 2em; }
h1 { font-size: 1.8rem; border-bottom: 2px solid var(--accent); padding-bottom: 0.3em; }
h2 { font-size: 1.4rem; border-bottom: 1px solid var(--border); padding-bottom: 0.2em; }
h3 { font-size: 1.15rem; }

/* ── Document metadata block ── */
.doc-header { text-align: center; margin-bottom: 3rem; }
.doc-header h1 { border: none; margin-bottom: 0.5rem; }
.doc-header .authors { color: var(--caption); font-size: 0.95rem; }
.doc-header .date { color: var(--caption); font-size: 0.85rem; }
.doc-header .abstract {
  text-align: left;
  max-width: 720px;
  margin: 1.5rem auto;
  padding: 1rem 1.5rem;
  border-left: 3px solid var(--accent);
  background: var(--code-bg);
  font-size: 0.92rem;
}
.doc-header .abstract strong { color: var(--heading); }

/* ── Section numbering (auto via CSS counters) ── */
body { counter-reset: h2counter; }
h2 { counter-reset: h3counter; }
h2::before {
  counter-increment: h2counter;
  content: counter(h2counter) ". ";
  color: var(--accent);
}
h3::before {
  counter-increment: h3counter;
  content: counter(h2counter) "." counter(h3counter) " ";
  color: var(--accent);
}

/* ── Figures and captions ── */
.figure {
  margin: 2rem 0;
  text-align: center;
}
.figure figcaption {
  font-family: var(--sans);
  font-size: 0.85rem;
  color: var(--caption);
  margin-top: 0.5rem;
}

/* ── Data tables ── */
table.data {
  border-collapse: collapse;
  margin: 1.5rem auto;
  font-size: 0.9rem;
  font-family: var(--sans);
}
table.data th {
  background: var(--code-bg);
  color: var(--heading);
  padding: 0.5rem 1rem;
  border-bottom: 2px solid var(--accent);
  text-align: left;
}
table.data td {
  padding: 0.4rem 1rem;
  border-bottom: 1px solid var(--border);
}
table.data tr:hover td { background: rgba(88, 166, 255, 0.05); }
table.data caption {
  font-size: 0.85rem;
  color: var(--caption);
  margin-bottom: 0.5rem;
  caption-side: bottom;
}

/* ── Code listings ── */
pre {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
  font-family: var(--mono);
  font-size: 0.85rem;
  line-height: 1.5;
}

/* ── Math display spacing ── */
.MathJax_Display, .katex-display {
  margin: 1.5rem 0 !important;
  overflow-x: auto;
}

/* ── Print-friendly overrides ── */
@media print {
  body { color: #000; background: #fff; max-width: 100%; }
  h1, h2, h3 { color: #000; }
  .figure { break-inside: avoid; }
  table.data { break-inside: avoid; }
}
```

### Two-Column Layout (Optional)

For dense technical content resembling IEEE-format papers:

```css
.two-col {
  column-count: 2;
  column-gap: 2rem;
  column-rule: 1px solid var(--border);
}
.two-col .figure,
.two-col table.data {
  column-span: all;   /* figures and tables span full width */
}
```

-----

## Cross-Referencing System

Implement lightweight cross-referencing for figures, tables, and equations in vanilla JS. Run after all content has loaded and MathJax has finished rendering.

```javascript
document.addEventListener('DOMContentLoaded', () => {
  // Auto-number figures
  const figures = document.querySelectorAll('.figure');
  figures.forEach((fig, i) => {
    const num = i + 1;
    fig.dataset.figNum = num;
    const cap = fig.querySelector('figcaption');
    if (cap) {
      cap.innerHTML = `<strong>Figure ${num}.</strong> ${cap.innerHTML}`;
    }
  });

  // Auto-number tables
  const tables = document.querySelectorAll('table.data');
  tables.forEach((tbl, i) => {
    const num = i + 1;
    tbl.dataset.tblNum = num;
    const cap = tbl.querySelector('caption');
    if (cap) {
      cap.innerHTML = `<strong>Table ${num}.</strong> ${cap.innerHTML}`;
    }
  });

  // Resolve cross-references: <a class="xref" href="#fig-id">Figure ?</a>
  document.querySelectorAll('a.xref').forEach(ref => {
    const targetId = ref.getAttribute('href').slice(1);
    const target = document.getElementById(targetId);
    if (!target) return;

    if (target.classList.contains('figure')) {
      ref.textContent = `Figure ${target.dataset.figNum}`;
    } else if (target.tagName === 'TABLE') {
      ref.textContent = `Table ${target.dataset.tblNum}`;
    }
    // Equations: MathJax handles \eqref{} natively
  });
});
```

### Usage in HTML

```html
<p>The SPI timing is shown in <a class="xref" href="#fig-spi-timing">Figure ?</a>.</p>

<figure class="figure" id="fig-spi-timing">
  <!-- WaveDrom or SVG content -->
  <figcaption>SPI Mode 0 timing for full-duplex transfer.</figcaption>
</figure>

<p>Component values are listed in <a class="xref" href="#tbl-bom">Table ?</a>.</p>

<table class="data" id="tbl-bom">
  <caption>Bill of materials for the amplifier stage.</caption>
  <!-- table content -->
</table>
```

The `?` placeholder is replaced at runtime by the auto-computed number.

-----

## Multi-Panel Figure Layouts

Use CSS grid to compose multi-panel figures where several plots, schematics, or diagrams share a single figure number and caption.

```html
<figure class="figure" id="fig-freq-analysis">
  <div class="panel-grid" style="
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    align-items: start;
  ">
    <div class="panel">
      <div class="panel-label">(a)</div>
      <div id="bode-mag"></div>
    </div>
    <div class="panel">
      <div class="panel-label">(b)</div>
      <div id="bode-phase"></div>
    </div>
    <div class="panel">
      <div class="panel-label">(c)</div>
      <div id="step-response"></div>
    </div>
    <div class="panel">
      <div class="panel-label">(d)</div>
      <div id="pole-zero"></div>
    </div>
  </div>
  <figcaption>Frequency-domain and time-domain analysis of the closed-loop system.
    (a) Bode magnitude, (b) Bode phase, (c) Step response, (d) Pole-zero map.</figcaption>
</figure>
```

Panel label styling:

```css
.panel-label {
  font-family: var(--sans);
  font-weight: bold;
  font-size: 0.85rem;
  color: var(--accent);
  margin-bottom: 0.3rem;
}
```

-----

## Data Tables with Uncertainty

Engineering data tables frequently show measured values with uncertainty (±), units, and test conditions.

```html
<table class="data" id="tbl-amplifier-params">
  <caption>Measured amplifier parameters at \(T_A = 25\,°\text{C}\), \(V_{CC} = 5\,\text{V}\).</caption>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Symbol</th>
      <th>Min</th>
      <th>Typical</th>
      <th>Max</th>
      <th>Unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Open-loop gain</td>
      <td>\(A_{OL}\)</td>
      <td>90</td>
      <td>110</td>
      <td>—</td>
      <td>dB</td>
    </tr>
    <tr>
      <td>Unity-gain bandwidth</td>
      <td>\(f_T\)</td>
      <td>0.8</td>
      <td>1.0</td>
      <td>1.2</td>
      <td>MHz</td>
    </tr>
    <tr>
      <td>Input offset voltage</td>
      <td>\(V_{OS}\)</td>
      <td>—</td>
      <td>±0.5</td>
      <td>±3.0</td>
      <td>mV</td>
    </tr>
    <tr>
      <td>Slew rate</td>
      <td>\(SR\)</td>
      <td>0.3</td>
      <td>0.5</td>
      <td>—</td>
      <td>V/µs</td>
    </tr>
    <tr>
      <td>CMRR</td>
      <td>\(\mathrm{CMRR}\)</td>
      <td>80</td>
      <td>95</td>
      <td>—</td>
      <td>dB</td>
    </tr>
  </tbody>
</table>
```

For measurement results with explicit uncertainty, use the format `value ± uncertainty` in the cell and let MathJax render inline: `\(3.142 \pm 0.005\)`.

-----

## Complete Document Skeleton

A full sci/eng HTML document combining all systems above. Copy this skeleton and populate with content sections.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{DOCUMENT TITLE}}</title>

  <!-- ── MathJax v3 ── -->
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        packages: {'[+]': ['mhchem', 'ams']},
        tags: 'ams',
        macros: {
          SI: ['{#1}\\;{\\mathrm{#2}}', 2],
          si: ['{\\mathrm{#1}}', 1],
          ohm: '\\Omega',
          dB: '{\\mathrm{dB}}',
          dBm: '{\\mathrm{dBm}}',
          // Add domain macros from Engineering Notation Macros section
        }
      },
      loader: { load: ['[tex]/mhchem', '[tex]/ams'] },
      chtml: { scale: 1.0, mtextInheritFont: true }
    };
  </script>
  <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

  <!-- ── WaveDrom ── -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.1.0/skins/default.js"
          type="text/javascript"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.1.0/wavedrom.min.js"
          type="text/javascript"></script>

  <!-- ── Plotly (for Bode, step response, spectrum, pole-zero) ── -->
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

  <!-- ── Mermaid (for system diagrams) ── -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>

  <!-- ── Highlight.js (for code listings) ── -->
  <link rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/github-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>

  <style>
    /* Paste the Document Structure and Typography CSS here */
  </style>
</head>
<body>

  <!-- ── Title Block ── -->
  <div class="doc-header">
    <h1>{{DOCUMENT TITLE}}</h1>
    <div class="authors">{{Author Name(s)}}</div>
    <div class="date">{{Date}}</div>
    <div class="abstract">
      <strong>Abstract — </strong>{{Abstract text.}}
    </div>
  </div>

  <!-- ── Content Sections ── -->
  <h2>Introduction</h2>
  <p>...</p>

  <h2>System Design</h2>
  <p>...</p>
  <!-- Mermaid block diagram here -->

  <h2>Circuit Analysis</h2>
  <p>...</p>
  <!-- SVG schematic here -->
  <!-- Equations with \label{} and \eqref{} -->

  <h2>Simulation Results</h2>
  <p>...</p>
  <!-- Plotly Bode plot, step response, etc. -->
  <!-- Multi-panel figure layout -->

  <h2>Digital Interface</h2>
  <p>...</p>
  <!-- WaveDrom timing diagram here -->

  <h2>Test Results</h2>
  <p>...</p>
  <!-- Data tables with uncertainty -->

  <h2>Conclusion</h2>
  <p>...</p>

  <!-- ── Initialization ── -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      // Mermaid
      if (typeof mermaid !== 'undefined') {
        mermaid.initialize({ startOnLoad: true, theme: 'dark' });
      }
      // WaveDrom
      if (typeof WaveDrom !== 'undefined') {
        WaveDrom.ProcessAll();
      }
      // Highlight.js
      if (typeof hljs !== 'undefined') { hljs.highlightAll(); }

      // Cross-referencing (run after MathJax finishes)
      const initXref = () => {
        // Figure numbering
        document.querySelectorAll('.figure').forEach((fig, i) => {
          const num = i + 1;
          fig.dataset.figNum = num;
          const cap = fig.querySelector('figcaption');
          if (cap) cap.innerHTML = `<strong>Figure ${num}.</strong> ${cap.innerHTML}`;
        });
        // Table numbering
        document.querySelectorAll('table.data').forEach((tbl, i) => {
          const num = i + 1;
          tbl.dataset.tblNum = num;
          const cap = tbl.querySelector('caption');
          if (cap) cap.innerHTML = `<strong>Table ${num}.</strong> ${cap.innerHTML}`;
        });
        // Resolve references
        document.querySelectorAll('a.xref').forEach(ref => {
          const target = document.getElementById(ref.getAttribute('href').slice(1));
          if (!target) return;
          if (target.classList.contains('figure'))
            ref.textContent = `Figure ${target.dataset.figNum}`;
          else if (target.tagName === 'TABLE')
            ref.textContent = `Table ${target.dataset.tblNum}`;
        });
      };

      // Wait for MathJax to finish, then run xref
      if (window.MathJax && MathJax.startup) {
        MathJax.startup.promise.then(initXref);
      } else {
        initXref();
      }
    });
  </script>
</body>
</html>
```

-----

## Domain Quick Reference

|Document Need                     |Tool / Technique           |Section                         |
|----------------------------------|---------------------------|--------------------------------|
|Numbered equations with refs      |MathJax AMS tags + `\eqref`|MathJax Engineering Config      |
|SI units (\SI{10}{k\Omega})       |Custom MathJax macros      |SI Units and Physical Quantities|
|Transfer function notation        |EE/Controls macro sets     |Engineering Notation Macros     |
|Semiconductor parameters          |Electronics macro set      |Engineering Notation Macros     |
|Digital timing waveforms          |WaveDrom 3.1.0             |WaveDrom Timing Diagrams        |
|Circuit schematics                |Inline SVG `<defs>`/`<use>`|SVG Circuit Schematics          |
|Bode / Nyquist / Root locus       |Plotly.js log-axis subplots|Control Systems Plotting        |
|Step / impulse response           |Plotly.js                  |Control Systems Plotting        |
|FFT spectrum, pole-zero map       |Plotly.js                  |Signal Processing Visualizations|
|Functional block diagrams         |Mermaid flowchart          |Systems Engineering Diagrams    |
|State machine diagrams            |Mermaid stateDiagram-v2    |Systems Engineering Diagrams    |
|Interface timing / protocols      |Mermaid sequenceDiagram    |Systems Engineering Diagrams    |
|Requirement traceability          |Mermaid graph              |Systems Engineering Diagrams    |
|Auto-numbered figures / tables    |CSS counters + JS xref     |Cross-Referencing System        |
|Multi-panel figures               |CSS Grid panels            |Multi-Panel Figure Layouts      |
|Datasheet-style parameter tables  |HTML `<table>` + MathJax   |Data Tables with Uncertainty    |
|Professional typographic hierarchy|CSS framework (serif body) |Document Structure & Typography |
|Print-ready output                |`@media print` overrides   |Document Structure & Typography |