#!/usr/bin/env node
// Render a Mermaid diagram file to SVG using the mermaid.ink API.
// Usage: node render-to-svg.js <input.mmd> [output.svg]
//   If output is omitted, writes to <input>.svg

const https = require('https');
const fs = require('fs');
const path = require('path');
const { deflateSync } = require('zlib');

const inputPath = process.argv[2];
if (!inputPath) {
  console.error('Usage: node render-to-svg.js <input.mmd> [output.svg]');
  process.exit(1);
}

const outputPath = process.argv[3] || inputPath.replace(/\.[^.]+$/, '.svg');
const mermaidCode = fs.readFileSync(inputPath, 'utf-8');

console.log(`Input:  ${inputPath} (${mermaidCode.length} chars)`);
console.log(`Output: ${outputPath}`);

// Mermaid.ink expects pako-deflated base64url-encoded JSON
const jsonStr = JSON.stringify({ code: mermaidCode, mermaid: { theme: 'default' } });
const compressed = deflateSync(jsonStr);
const encoded = compressed.toString('base64url');
const url = `https://mermaid.ink/svg/pako:${encoded}`;

console.log('Fetching SVG from mermaid.ink...');

https.get(url, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200 && data.includes('<svg')) {
      fs.writeFileSync(outputPath, data, 'utf-8');
      console.log(`SVG saved: ${outputPath} (${data.length} bytes)`);
    } else {
      console.error(`Failed (HTTP ${res.statusCode}):`);
      console.error(data.substring(0, 500));
      process.exit(1);
    }
  });
}).on('error', (err) => {
  console.error(`Request failed: ${err.message}`);
  process.exit(1);
});
