# Implementing RLM in Claude Code

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Mapping](#architecture-mapping)
3. [Implementation Approaches](#implementation-approaches)
4. [Windows Setup](#windows-setup)
5. [Feasibility Assessment](#feasibility-assessment)

---

## Executive Summary

Claude Code can implement RLM because it already has the core infrastructure:
- File-based context storage (`/home/claude/` or local workspace)
- Python/bash code execution
- Iterative multi-turn reasoning

**The key insight:** Claude Code IS the RLM agent. It examines content, decides strategies, writes processing code, and adapts based on observations.

### What RLM Enables

| Metric | Improvement |
|--------|-------------|
| Context handling | 100x beyond model context windows (10M+ tokens) |
| Quality on OOLONG | +28-33% over base models |
| BrowseComp+ (1K docs) | 91% accuracy vs 0% for base models |

---

## Architecture Mapping

### RLM Components → Claude Code

| RLM Component | Claude Code Equivalent |
|---------------|----------------------|
| REPL Environment | Bash tool + Python runtime |
| Context Storage | File system |
| Code Execution | Multi-turn bash execution |
| Sub-LM Calls | API calls via `rlm_query.py` |
| Final Answer | Response formatting |

### The Sub-LLM Pattern

```python
# What RLM needs
result = llm_query(f"Analyze chunk: {chunk}", model="claude-haiku-4-5-20251001")
```

This is implemented in `scripts/rlm_query.py` using curl to call the Anthropic API.

---

## Implementation Approaches

### Approach 1: Python Scripts (Current)

Use `rlm_processor.py` and `rlm_query.py` directly:

```bash
python scripts/rlm_processor.py document.pdf "Summarize key points"
```

**Pros:** Works today, no additional setup
**Cons:** Requires API key, sequential processing

### Approach 2: MCP Server (Future)

Create an MCP server providing `llm_query` as a tool:

```typescript
server.tool("llm_query", {
  description: "Invoke a sub-LLM call",
  inputSchema: {
    properties: {
      prompt: { type: "string" },
      model: { type: "string", default: "claude-haiku-4-5-20251001" }
    }
  }
}, async (args) => {
  const response = await anthropic.messages.create({...});
  return { content: response.content[0].text };
});
```

**Pros:** Clean integration, reusable
**Cons:** Requires MCP server setup

### Approach 3: Native Sub-Agent (Ideal)

If Anthropic adds native sub-agent capability to Claude Code:

```python
result = claude_sub_query(prompt=f"Analyze: {chunk}", max_tokens=1000)
```

---

## Windows Setup

### API Key Storage

The scripts check these locations in order:
1. `ANTHROPIC_API_KEY` environment variable
2. `%USERPROFILE%\.claude\api_key.txt`
3. `%USERPROFILE%\.claude\config.json`

**PowerShell setup:**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude"
"sk-ant-api03-your-key-here" | Out-File "$env:USERPROFILE\.claude\api_key.txt" -NoNewline -Encoding utf8

# Verify
python scripts\rlm_query.py --check-key
```

---

## Feasibility Assessment

### Ready Today

| Capability | Status |
|------------|--------|
| File-based context storage | Ready |
| Python code execution | Ready |
| Iterative reasoning | Ready |
| Result aggregation | Ready |
| Context chunking | Ready |

### Needs Work

| Capability | Implementation Path |
|------------|---------------------|
| Sub-LM calls | API calls via curl/Python (done) |
| API key management | Environment variable or .claude folder (done) |
| Async processing | Python asyncio (optional) |

### Current Limitations

| Limitation | Mitigation |
|------------|------------|
| No native sub-agent | Use API calls directly |
| Sequential processing | Implement async patterns |
| API key required | Store in .claude folder |

---

## Conclusion

Claude Code provides ~80% of RLM infrastructure. The remaining 20% is implemented via:

1. **Current:** Bash/Python scripts calling Anthropic API
2. **Future:** MCP server for cleaner integration
3. **Ideal:** Native sub-agent capability in Claude Code

Reference: Zhang, Kraska, Khattab - "Recursive Language Models" (MIT CSAIL, arXiv:2512.24601)
