# CS Paper LaTeX Syntax Reference

## Overview

Write compilable LaTeX for computer science papers and algorithms. Key principle: know which packages conflict, which environments your document class already defines, and how algorithm packages differ.

## Algorithm Packages: Choose One Per Document

**algorithm2e and algorithmicx are INCOMPATIBLE.** Both redefine the `algorithm` float. Never load both.

| Package | Float | Pseudocode Style | Key Commands |
|---------|-------|-------------------|--------------|
| `algorithm2e` | Built-in | Keyword-based | `\KwIn`, `\KwOut`, `\While{}{}`, `\If{}{}`, `\Return`, `\SetKwFunction` |
| `algorithm` + `algpseudocode` | `algorithm` pkg | Procedural | `\Procedure{}{}`, `\State`, `\While{}`, `\If{}`, `\Return`, `\Call{}{}` |

### algorithm2e

```latex
\usepackage[lined,boxed,ruled]{algorithm2e}

\begin{algorithm}[H]
\caption{Binary Search}\label{alg:bsearch}
\KwIn{Sorted array $A[1..n]$, target $x$}
\KwOut{Index of $x$ or $-1$}
$l \gets 1$, $r \gets n$\;
\While{$l \leq r$}{
  $m \gets \lfloor(l+r)/2\rfloor$\;
  \lIf{$A[m] = x$}{\Return $m$}
  \eIf{$A[m] < x$}{$l \gets m+1$\;}{$r \gets m-1$\;}
}
\Return $-1$\;
\end{algorithm}
```

### algorithmicx + algpseudocode

```latex
\usepackage{algorithm}       % float wrapper
\usepackage{algpseudocode}   % pseudocode commands (loads algorithmicx)

\begin{algorithm}[H]
\caption{Dijkstra}\label{alg:dijkstra}
\begin{algorithmic}[1]       % [1] = line numbers
\Procedure{Dijkstra}{$G, s$}
  \State $d[s] \gets 0$; $d[v] \gets \infty\ \forall v \neq s$
  \While{$Q \neq \emptyset$}
    \State $u \gets$ \Call{ExtractMin}{$Q$}
    \For{each $v$ adjacent to $u$}
      \If{$d[u] + w(u,v) < d[v]$}
        \State $d[v] \gets d[u] + w(u,v)$
      \EndIf
    \EndFor
  \EndWhile
  \State \Return $d$
\EndProcedure
\end{algorithmic}
\end{algorithm}
```

**Never:** `\usepackage{algorithm2e}` + `\usepackage{algpseudocode}` in the same document.

## Document Classes

### acmart (ACM)

```latex
\documentclass[sigconf]{acmart}  % or sigplan, acmtog, etc.
```

**acmart already defines:** `theorem`, `lemma`, `corollary`, `proposition`, `conjecture`, `definition`, `example`, `proof`. Do NOT `\newtheorem` these -- you'll get "already defined" errors.

**CCS concepts:** Use `\begin{CCSXML}...\end{CCSXML}` (note: `\end{CCSXML}`, not `</end{CCSXML}>`).

### IEEEtran (IEEE)

```latex
\documentclass[conference]{IEEEtran}
```

Define your own theorem envs. Use `\IEEEauthorblockN` and `\IEEEauthorblockA` for authors.

### NeurIPS / ICML

```latex
\usepackage{neurips_2024}  % or icml2024
```

Check the style file for pre-defined environments before defining your own.

## Common Preamble

```latex
\usepackage[utf8]{inputenc}   % NOT utf-8 (no hyphen!)
\usepackage{amsmath,amssymb,amsthm}
\usepackage{booktabs}          % \toprule, \midrule, \bottomrule
\usepackage{graphicx}
\usepackage{subcaption}        % subfigures
\usepackage{listings}          % code listings
\usepackage{xcolor}            % colors for listings
\usepackage{hyperref}          % clickable refs (load LAST)
```

**inputenc option is `utf8`** -- not `utf-8`. The hyphen causes an "unknown option" error.

## Theorems and Proofs

For `article` class (define your own):
```latex
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}        % shares counter with theorem
\newtheorem{definition}{Definition}[section]
\theoremstyle{remark}
\newtheorem{remark}{Remark}
```

For `acmart`: already defined. Just use `\begin{theorem}...\end{theorem}` directly.

## Math Quick Reference

```latex
% Complexity notation
\newcommand{\bigO}[1]{O\!\left(#1\right)}
\newcommand{\bigTheta}[1]{\Theta\!\left(#1\right)}
\newcommand{\bigOmega}[1]{\Omega\!\left(#1\right)}

% Expectation, probability
\newcommand{\E}[1]{\mathbb{E}\!\left[#1\right]}
\newcommand{\Pr}{\operatorname{Pr}}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}

% Multi-line equations
\begin{align}
  f(x) &= ax^2 + bx + c \label{eq:quad} \\
       &= a(x-h)^2 + k   \nonumber
\end{align}
```

## Tables with booktabs

```latex
\begin{table}[t]
\centering
\caption{Results}\label{tab:results}
\begin{tabular}{lrrr}
\toprule
Method     & Accuracy & F1    & Time (s) \\
\midrule
Baseline   & 85.2     & 0.83  & 120 \\
Ours       & \textbf{91.7} & \textbf{0.90} & 95 \\
\bottomrule
\end{tabular}
\end{table}
```

**Never use `\hline`** with booktabs. Use `\toprule`, `\midrule`, `\bottomrule`.

## Code Listings

```latex
\usepackage{listings}
\usepackage{xcolor}
\lstset{
  language=Python,
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue}\bfseries,
  commentstyle=\color{gray}\itshape,
  numbers=left, numberstyle=\tiny\color{gray},
  frame=single, breaklines=true
}

\begin{lstlisting}[caption=Example]
def train(model, data):
    for batch in data:
        loss = model(batch)
        loss.backward()
\end{lstlisting}
```

## Subfigures

```latex
\usepackage{subcaption}

\begin{figure}[t]
\centering
\begin{subfigure}[b]{0.48\textwidth}
  \includegraphics[width=\textwidth]{fig_a.pdf}
  \caption{Training loss}\label{fig:loss}
\end{subfigure}
\hfill
\begin{subfigure}[b]{0.48\textwidth}
  \includegraphics[width=\textwidth]{fig_b.pdf}
  \caption{Accuracy}\label{fig:acc}
\end{subfigure}
\caption{Experimental results}\label{fig:results}
\end{figure}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Loading `algorithm2e` + `algorithmicx` together | Choose ONE. They redefine the same float. |
| `\newtheorem{theorem}` in `acmart` | `acmart` pre-defines it. Just use `\begin{theorem}`. |
| `\usepackage[utf-8]{inputenc}` | Use `utf8` (no hyphen): `[utf8]` |
| `</end{CCSXML}>` in acmart | LaTeX syntax: `\end{CCSXML}` (backslash, not angle bracket) |
| `\hline` with booktabs | Use `\toprule`, `\midrule`, `\bottomrule` |
| `\ref` to undefined `\label` | Every `\ref{X}` needs a matching `\label{X}` in the document |
| `hyperref` loaded before other packages | Load `hyperref` LAST in preamble |
| Missing `\;` at end of algorithm2e lines | Each line in algorithm2e needs `\;` for line-ending |

## Rendering to SVG

Use `render-latex-to-svg.js` (in this skill directory) to render LaTeX math to SVG:

```bash
node render-latex-to-svg.js <input.tex> [output.svg] [--dpi=N]
```

- Uses the latex.codecogs.com API (no local LaTeX install needed)
- Extracts math blocks (`$...$`, `\begin{align}`, etc.) from `.tex` files
- Raw LaTeX math files render as-is
- Multiple blocks are combined into a stacked SVG
- Default DPI is 200

## Validation Checklist

Before outputting LaTeX, verify:
- [ ] Only ONE algorithm package family loaded
- [ ] No `\newtheorem` for environments the document class already defines
- [ ] `inputenc` uses `utf8` (no hyphen)
- [ ] Every `\ref{}` has a matching `\label{}`
- [ ] `booktabs` commands not mixed with `\hline`
- [ ] `hyperref` loaded last (if used)
- [ ] All `\end{...}` use backslash syntax (not `</end{...}>`)
