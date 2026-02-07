#!/usr/bin/env node
// Render a Graphviz DOT file to SVG using the quickchart.io API.
// Usage: node render-to-svg.js <input.dot> [output.svg]
//   If output is omitted, writes to <input>.svg

const https = require('https');
const fs = require('fs');

const inputPath = process.argv[2];
if (!inputPath) {
  console.error('Usage: node render-to-svg.js <input.dot> [output.svg]');
  process.exit(1);
}

const outputPath = process.argv[3] || inputPath.replace(/\.[^.]+$/, '.svg');
const dotSource = fs.readFileSync(inputPath, 'utf-8');

console.log(`Input:  ${inputPath} (${dotSource.length} chars)`);
console.log(`Output: ${outputPath}`);

const postData = JSON.stringify({
  graph: dotSource,
  layout: 'dot',
  format: 'svg'
});

const options = {
  hostname: 'quickchart.io',
  port: 443,
  path: '/graphviz',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

console.log('Sending DOT to quickchart.io/graphviz...');

const req = https.request(options, (res) => {
  const chunks = [];
  res.on('data', (chunk) => chunks.push(chunk));
  res.on('end', () => {
    const content = Buffer.concat(chunks).toString('utf-8');
    if (res.statusCode === 200 && content.includes('<svg')) {
      fs.writeFileSync(outputPath, content, 'utf-8');
      console.log(`SVG saved: ${outputPath} (${content.length} bytes)`);
    } else {
      console.error(`Failed (HTTP ${res.statusCode}):`);
      console.error(content.substring(0, 500));
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error(`Request failed: ${e.message}`);
  process.exit(1);
});

req.write(postData);
req.end();
