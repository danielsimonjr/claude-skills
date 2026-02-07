# Complete RLM Example: Single Script REPL Session

This is a standalone Python script implementing the full RLM pipeline.

```python
#!/usr/bin/env python3
"""
RLM Processing Session
Content loaded into memory, examined, processed, aggregated.
"""

import os
import json
import subprocess
import re
from pathlib import Path

# ============================================================
# SETUP
# ============================================================

def get_api_key():
    key = os.environ.get('ANTHROPIC_API_KEY')
    if key: return key.strip()
    key_file = Path.home() / '.claude' / 'api_key.txt'
    if key_file.exists(): return key_file.read_text().strip()
    raise ValueError("API key not found")

API_KEY = get_api_key()

def llm_query(prompt, fast=True):
    model = "claude-haiku-4-5-20251001" if fast else "claude-sonnet-4-5-20250929"
    payload = json.dumps({
        "model": model, "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    })
    result = subprocess.run([
        'curl', '-s', 'https://api.anthropic.com/v1/messages',
        '-H', 'Content-Type: application/json',
        '-H', f'x-api-key: {API_KEY}',
        '-H', 'anthropic-version: 2023-06-01',
        '-d', payload
    ], capture_output=True, text=True)
    return json.loads(result.stdout)['content'][0]['text']

# ============================================================
# 1. LOAD INTO REPL
# ============================================================

FILE_PATH = "/path/to/large_file.txt"  # <-- Change this
USER_QUERY = "Summarize the main findings"  # <-- Change this

context = open(FILE_PATH).read()
print(f"Loaded {len(context):,} characters into memory")

# ============================================================
# 2. EXAMINE IN MEMORY
# ============================================================

print("\n=== EXAMINING ===")
print(f"Lines: {context.count(chr(10)):,}")
print(f"Est. tokens: ~{len(context)//4:,}")

# Sample
print("\n--- First 500 chars ---")
print(context[:500])

# Detect structure
md_headers = len(re.findall(r'^#{1,3} ', context, re.MULTILINE))
functions = len(re.findall(r'^def |^class ', context, re.MULTILINE))
print(f"\nMarkdown headers: {md_headers}")
print(f"Function/class defs: {functions}")

# ============================================================
# 3. DECIDE STRATEGY
# ============================================================

print("\n=== DECIDING STRATEGY ===")

if md_headers > 3:
    chunks = re.split(r'\n(?=## )', context)
    strategy = "markdown"
elif functions > 3:
    chunks = re.split(r'\n(?=def |class )', context)
    strategy = "code"
else:
    # Fixed size with overlap
    chunks = [context[i:i+20000] for i in range(0, len(context), 19000)]
    strategy = "fixed"

print(f"Strategy: {strategy}")
print(f"Chunks: {len(chunks)}")

# ============================================================
# 4. PROCESS CHUNKS
# ============================================================

print("\n=== PROCESSING ===")
results = []

for i, chunk in enumerate(chunks):
    if len(chunk) < 100:
        continue

    print(f"[{i+1}/{len(chunks)}] {len(chunk):,} chars...", end=" ")

    prompt = f"""Analyze this section:

{chunk[:15000]}

Query: {USER_QUERY}

Respond in JSON: {{"summary": "...", "key_points": [...]}}"""

    try:
        resp = llm_query(prompt, fast=True)
        result = json.loads(resp)
        results.append(result)
        print(f"OK - {len(result.get('key_points', []))} points")
    except Exception as e:
        print(f"Error: {e}")

# ============================================================
# 5. AGGREGATE
# ============================================================

print("\n=== AGGREGATING ===")

all_points = []
for r in results:
    all_points.extend(r.get('key_points', []))

# Final synthesis with stronger model
final_prompt = f"""Synthesize these findings into a coherent response:

Summaries:
{json.dumps([r.get('summary') for r in results], indent=2)}

Key Points:
{json.dumps(all_points, indent=2)}

Original Query: {USER_QUERY}

Provide a comprehensive response."""

final = llm_query(final_prompt, fast=False)

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)
print(final)

# Optionally save
Path("result.txt").write_text(final)
print("\nSaved to result.txt")
```

## Usage

```bash
# Edit FILE_PATH and USER_QUERY in the script, then:
python rlm_session.py
```

## Customization Points

| Variable | Purpose |
|----------|---------|
| `FILE_PATH` | Path to file to process |
| `USER_QUERY` | What you want to learn from the file |
| `chunk_size` | Characters per chunk (default: 20000) |
| `fast=True/False` | Haiku (cheap) vs Sonnet (quality) |
