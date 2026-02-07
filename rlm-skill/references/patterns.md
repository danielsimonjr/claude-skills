# RLM Patterns Reference

Based on observations from the paper "Recursive Language Models" (arXiv:2512.24601).

## Emergent Patterns in RLM Trajectories

### Pattern 1: Filtering with Model Priors

**When to use**: When context is large but query targets specific information.

**How it works**: 
- Extract keywords from query
- Use regex/string matching to filter chunks BEFORE expensive LLM calls
- Reduces API costs significantly

```python
# Example implementation
import re

def filter_by_priors(chunks, query):
    # Extract meaningful keywords (skip stopwords)
    keywords = re.findall(r'\b[A-Z][a-z]+\b|\b\w{6,}\b', query)
    
    # Build pattern
    pattern = '|'.join(keywords)
    
    # Filter chunks
    relevant = []
    for i, chunk in enumerate(chunks):
        if re.search(pattern, chunk, re.IGNORECASE):
            relevant.append((i, chunk))
    
    return relevant
```

**Paper finding**: This pattern significantly reduces costs while maintaining quality.

---

### Pattern 2: Hierarchical Decomposition

**When to use**: For very large contexts (>1M tokens) or deep analysis.

**How it works**:
- Recursively break context into smaller pieces
- Process leaves first, then aggregate up the tree
- Final synthesis at root

```
Level 0 (Root):     [Final Answer]
                         ↑
Level 1:        [Summary A]  [Summary B]
                   ↑            ↑
Level 2:     [S1] [S2] [S3]  [S4] [S5] [S6]
                ↑     ↑           ↑     ↑
Level 3:    Chunk processing (leaf nodes)
```

```python
def process_hierarchically(chunks, query, depth=0, max_depth=3):
    if len(chunks) <= 2 or depth >= max_depth:
        # Base case: process directly
        combined = "\n---\n".join(chunks)
        return llm_query(f"Analyze for '{query}':\n{combined}")
    
    # Recursive case: split and recurse
    mid = len(chunks) // 2
    left = process_hierarchically(chunks[:mid], query, depth+1)
    right = process_hierarchically(chunks[mid:], query, depth+1)
    
    # Combine
    return llm_query(f"Combine these analyses:\n{left}\n---\n{right}")
```

**Paper finding**: Enables processing of essentially unlimited context lengths.

---

### Pattern 3: Answer Verification

**When to use**: For high-stakes queries where accuracy is critical.

**How it works**:
- After finding a potential answer, verify it
- Use sub-LLM call with focused context (relevant chunks only)
- Avoids context rot by keeping verification context small

```python
def verify_answer(answer, evidence_chunks, query):
    verification_prompt = f"""
    PROPOSED ANSWER: {answer}
    
    ORIGINAL QUERY: {query}
    
    EVIDENCE (subset of document):
    {chr(10).join(evidence_chunks[:3])}
    
    TASK: Verify if the proposed answer is correct based on the evidence.
    If incorrect, provide the correct answer.
    If partially correct, explain what's missing.
    """
    
    return llm_query(verification_prompt)
```

**Paper finding**: Improves accuracy, especially for complex queries.

---

### Pattern 4: Variable-Based Output Construction

**When to use**: For tasks requiring long outputs (e.g., listing all pairs, full summaries).

**How it works**:
- Store intermediate results in Python variables
- Build up the final answer programmatically
- Return variable contents at the end (not model generation)

```python
# Store results as variables
results = []

for chunk in chunks:
    chunk_result = llm_query(f"Extract all X from: {chunk}")
    results.append(chunk_result)

# Combine programmatically
final_output = "\n".join(results)  # No hallucination risk

# Or aggregate with LLM
final_answer = llm_query(f"Synthesize: {final_output}")
```

**Paper finding**: Critical for tasks with long output requirements (OOLONG-Pairs).

---

### Pattern 5: Semantic Transformation per Entry

**When to use**: When processing structured data with semantic labels.

**How it works**:
- Process each entry individually with sub-LLM call
- Particularly useful for classification tasks
- Can be parallelized for speed

```python
def classify_entries(entries, categories):
    classifications = {}
    
    for entry_id, entry_text in entries:
        result = llm_query(f"""
        Classify this entry into one of: {categories}
        
        Entry: {entry_text}
        
        Category:""")
        
        classifications[entry_id] = result.strip()
    
    return classifications
```

**Paper finding**: Essential for OOLONG-style tasks where every entry matters.

---

## Cost Optimization Strategies

### 1. Model Tiering

Use different models for different tasks:

| Task | Recommended Model | Reason |
|------|-------------------|--------|
| Chunk processing | claude-haiku | Fast, cheap |
| Final aggregation | claude-sonnet | Higher quality |
| Complex reasoning | claude-opus | Best accuracy |

### 2. Early Termination

If answer is found with high confidence, stop processing remaining chunks.

### 3. Adaptive Chunking

Adjust chunk size based on information density:
- Code: smaller chunks (more structure per line)
- Prose: larger chunks (context helps understanding)

### 4. Caching

Save intermediate results to files:
```python
cache_file = f"/tmp/rlm_cache_{hash(chunk)}.json"
if os.path.exists(cache_file):
    result = json.load(open(cache_file))
else:
    result = llm_query(...)
    json.dump(result, open(cache_file, 'w'))
```

---

## Negative Results (What Doesn't Work)

From paper Appendix A:

1. **Same prompt across all models**: Different models need different prompting
2. **Models without coding ability**: Struggle with RLM (need Python proficiency)
3. **Thinking models without enough output tokens**: Run out of budget
4. **Synchronous sub-calls**: Slow (async would help but harder to implement)
5. **Brittle final answer detection**: FINAL() tags can be misused

---

## Performance Benchmarks

From the paper's experiments:

| Task | Base Model | RLM | Improvement |
|------|------------|-----|-------------|
| OOLONG (GPT-5) | 44% | 56.5% | +28% |
| OOLONG-Pairs (GPT-5) | <0.1% | 58% | >500x |
| BrowseComp+ 1K (GPT-5) | 0%* | 91.3% | ∞ |
| CodeQA (GPT-5) | 24%* | 62% | +158% |

*Base model cannot fit context
