#!/usr/bin/env node
// Render LaTeX math/equations to SVG using the latex.codecogs.com API.
// Usage: node render-to-svg.js <input.tex> [output.svg] [--dpi=N]
//
// Modes:
//   - If input is a .tex file, extracts all $...$ and \begin{...} blocks
//     and renders them as a combined SVG.
//   - Reads raw LaTeX math if the file contains no document structure.
//
// Requires: Node.js (no local LaTeX install needed)

const https = require('https');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2).filter(a => !a.startsWith('--'));
const flags = process.argv.slice(2).filter(a => a.startsWith('--'));

const inputPath = args[0];
if (!inputPath) {
  console.error('Usage: node render-to-svg.js <input.tex> [output.svg] [--dpi=N]');
  console.error('');
  console.error('Renders LaTeX equations to native SVG via latex.codecogs.com.');
  console.error('Input can be a .tex file (extracts math blocks) or raw LaTeX math.');
  process.exit(1);
}

const outputPath = args[1] || inputPath.replace(/\.[^.]+$/, '.svg');
const dpiFlag = flags.find(f => f.startsWith('--dpi='));
const dpi = dpiFlag ? parseInt(dpiFlag.split('=')[1]) : 200;

const texSource = fs.readFileSync(inputPath, 'utf-8');

console.log(`Input:  ${inputPath} (${texSource.length} chars)`);
console.log(`Output: ${outputPath}`);
console.log(`DPI:    ${dpi}`);

// Determine if this is a full document or raw math
const isDocument = texSource.includes('\\documentclass') || texSource.includes('\\begin{document}');

let mathBlocks = [];

if (isDocument) {
  // Extract math environments from the document
  console.log('Extracting math blocks from LaTeX document...');

  // Extract display math: \begin{align}, \begin{equation}, \[...\], $$...$$
  const envRegex = /\\begin\{(align|equation|gather|multline|array|cases)\*?\}[\s\S]*?\\end\{\1\*?\}/g;
  let match;
  while ((match = envRegex.exec(texSource)) !== null) {
    mathBlocks.push({ label: match[1], tex: match[0] });
  }

  // Extract boxed/standalone display math
  const displayRegex = /\\\[[\s\S]*?\\\]/g;
  while ((match = displayRegex.exec(texSource)) !== null) {
    mathBlocks.push({ label: 'display', tex: match[0].slice(2, -2).trim() });
  }

  // Extract custom commands for context
  const preamble = texSource.split('\\begin{document}')[0] || '';
  const newcmds = preamble.match(/\\(newcommand|DeclareMathOperator)\*?{[^}]+}(\[[^\]]*\])?{[^}]+}/g) || [];
  const cmdPrefix = newcmds.join('\n');

  // Prepend custom commands to each block
  if (cmdPrefix) {
    mathBlocks = mathBlocks.map(b => ({
      ...b,
      tex: cmdPrefix + '\n' + b.tex
    }));
  }

  if (mathBlocks.length === 0) {
    console.log('No math blocks found. Rendering entire file as LaTeX...');
    mathBlocks.push({ label: 'document', tex: texSource });
  }
} else {
  // Raw LaTeX math -- render as-is
  mathBlocks.push({ label: 'math', tex: texSource.trim() });
}

console.log(`Found ${mathBlocks.length} block(s) to render.`);

// Fetch each block as SVG
const results = new Array(mathBlocks.length).fill(null);
let completed = 0;

function fetchBlock(idx) {
  const block = mathBlocks[idx];
  const encodedTex = encodeURIComponent(block.tex);
  const urlPath = `/svg.image?\\dpi{${dpi}}${encodedTex}`;

  function doFetch(hostname, fetchPath) {
    https.get({ hostname, path: fetchPath, headers: { 'User-Agent': 'Node.js' } }, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        const loc = new URL(res.headers.location);
        doFetch(loc.hostname, loc.pathname + loc.search);
        return;
      }
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const data = Buffer.concat(chunks).toString('utf-8');
        if (data.includes('<svg')) {
          results[idx] = data;
          console.log(`  [${idx + 1}/${mathBlocks.length}] ${block.label}: OK (${data.length} bytes)`);
        } else {
          console.log(`  [${idx + 1}/${mathBlocks.length}] ${block.label}: failed (no SVG)`);
        }
        completed++;
        if (completed === mathBlocks.length) finalize();
      });
    }).on('error', (e) => {
      console.error(`  [${idx + 1}/${mathBlocks.length}] ${block.label}: error (${e.message})`);
      completed++;
      if (completed === mathBlocks.length) finalize();
    });
  }

  doFetch('latex.codecogs.com', urlPath);
}

function finalize() {
  const valid = results.filter(r => r !== null);

  if (valid.length === 1) {
    // Single block -- save directly
    fs.writeFileSync(outputPath, valid[0], 'utf-8');
    console.log(`\nSVG saved: ${outputPath} (${valid[0].length} bytes)`);
    return;
  }

  // Multiple blocks -- combine into a stacked SVG
  let totalHeight = 20; // top padding
  const blockInfo = [];

  for (const svg of valid) {
    const hMatch = svg.match(/height='([^']+?)(?:pt|px)?'/);
    const wMatch = svg.match(/width='([^']+?)(?:pt|px)?'/);
    const h = hMatch ? parseFloat(hMatch[1]) : 50;
    const w = wMatch ? parseFloat(wMatch[1]) : 400;
    blockInfo.push({ svg, w, h, y: totalHeight });
    totalHeight += h + 20; // 20px gap between blocks
  }

  const maxW = Math.max(...blockInfo.map(b => b.w)) + 40;
  const parts = [];
  parts.push(`<?xml version="1.0" encoding="UTF-8"?>`);
  parts.push(`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${maxW}pt" height="${totalHeight}pt" viewBox="0 0 ${maxW} ${totalHeight}">`);
  parts.push(`<rect width="${maxW}" height="${totalHeight}" fill="white"/>`);

  for (const info of blockInfo) {
    const inner = info.svg
      .replace(/<\?xml[^?]*\?>\s*/, '')
      .replace(/<!DOCTYPE[^>]*>\s*/, '')
      .replace(/<svg([^>]*)>/, `<svg$1 x="20" y="${info.y}">`);
    parts.push(inner);
  }

  parts.push('</svg>');
  const combined = parts.join('\n');
  fs.writeFileSync(outputPath, combined, 'utf-8');
  console.log(`\nCombined SVG saved: ${outputPath} (${combined.length} bytes, ${valid.length} blocks)`);
}

// Launch all fetches
mathBlocks.forEach((_, i) => fetchBlock(i));
