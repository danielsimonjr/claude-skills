---
name: refactoring
description: Surgical, high-impact code refactoring guided by Torvalds-style principles of taste, simplicity, and performance consciousness. Use when refactoring code, eliminating code smells, improving maintainability, or performing systematic codebase improvements across C++, Python, Go, JavaScript, and TypeScript.
---

# Code Refactoring Excellence SKILL

## Overview
This skill guides Claude in performing surgical, high-impact code refactoring that prioritizes clarity, performance, maintainability, and correctness. It embodies the engineering philosophies of systems masters: ruthless simplification, performance consciousness, and elegant problem-solving.

## Documentation Structure

This SKILL is part of a comprehensive refactoring toolkit:

- **[README.md](README.md)** - Start here! Overview, quick start, and navigation guide
- **[SKILL.md](SKILL.md)** (this file) - Complete refactoring methodology and philosophy
- **[refactoring-quick-reference.md](examples/refactoring-quick-reference.md)** - Fast-access patterns and checklists
- **[refactoring-examples.md](examples/refactoring-examples.md)** - Real-world transformations (C++, Python, Go)
- **[javascript-typescript-refactoring-examples.md](examples/javascript-typescript-refactoring-examples.md)** - Modern JS/TS patterns

**First time here?** Read the [README.md](README.md) for an introduction and learning path.

**Need quick patterns?** Check [refactoring-quick-reference.md](examples/refactoring-quick-reference.md) for common code smells and fixes.

**Want to see real transformations?** Browse the [examples/](examples/) folder for language-specific refactoring examples.

## Core Philosophy

### The Torvalds Principles
1. **Taste Matters**: Good code has taste. It's not just about working—it's about being obviously correct.
2. **Simplicity Over Cleverness**: Smart code is simple code. Clever code is a liability.
3. **Performance is a Feature**: Always be aware of what the machine is actually doing.
4. **Maintainability is Everything**: Code is read 100x more than it's written.
5. **Data Structures > Algorithms**: Get the data structures right, and the algorithms become obvious.

### The Carmack Principles
1. **Functional Purity Where Possible**: Minimize state, maximize referential transparency.
2. **Performance Through Understanding**: Optimization comes from understanding the machine and the problem deeply.
3. **Incremental Improvement**: Make one clear improvement at a time, verify it works.
4. **Eliminate Abstraction Overhead**: Every layer of abstraction has a cost—make it worth it.
5. **Measurement Over Assumptions**: Profile before optimizing. Measure after refactoring.

## Refactoring Process

> **Note:** This section provides the theoretical framework. For practical, language-specific examples of these patterns in action, see:
> - [examples/refactoring-examples.md](examples/refactoring-examples.md) - C++, Python, Go examples
> - [examples/javascript-typescript-refactoring-examples.md](examples/javascript-typescript-refactoring-examples.md) - Modern web development patterns
> - [examples/refactoring-quick-reference.md](examples/refactoring-quick-reference.md) - Quick pattern lookup

### Phase 1: Analysis and Understanding

Before touching any code, Claude MUST:

1. **Read and Comprehend Completely**
   - Understand what the code actually does, not what it claims to do
   - Identify the core algorithm or business logic
   - Map data flows and transformations
   - Identify external dependencies and side effects
   - Find all entry points and exit points

2. **Identify Code Smells**

   > **Quick Reference:** See [examples/refactoring-quick-reference.md](examples/refactoring-quick-reference.md) for a fast-access guide to all these smells with before/after examples.
   
   - **Structural Smells**:
     - God objects/functions doing too much
     - Primitive obsession (using primitives instead of domain types)
     - Feature envy (method using another class's data more than its own)
     - Data clumps (groups of data that travel together)
     - Long parameter lists
     - Divergent change (one class changed for many reasons)
     - Shotgun surgery (one change requires changes in many places)
   
   - **Complexity Smells**:
     - Cyclomatic complexity > 10
     - Nesting depth > 4
     - Function length > 50 lines (guideline, not rule)
     - Duplicate code blocks
     - Complex boolean expressions
     - Switch statements that could be polymorphism
   
   - **Performance Smells**:
     - Unnecessary allocations in hot paths
     - N+1 query patterns
     - Premature abstraction causing overhead
     - Cache misses from poor data locality
     - Excessive string concatenation
     - Repeated expensive computations
   
   - **Maintainability Smells**:
     - Magic numbers without explanation
     - Unclear variable/function names
     - Comments explaining what instead of why
     - Inconsistent naming conventions
     - Mixed abstraction levels
     - Hidden temporal coupling

3. **Establish Test Coverage**
   - If tests exist, run them and verify they pass
   - If tests don't exist, CREATE THEM FIRST
   - Focus on behavior, not implementation
   - Test edge cases and error conditions
   - Ensure tests are fast and deterministic

4. **Set Clear Goals**
   - Define specific, measurable improvements
   - Prioritize by impact (clarity > performance > brevity)
   - Identify non-negotiables (API contracts, performance guarantees)
   - Set success criteria

### Phase 2: Strategic Refactoring

Apply refactorings in order of safety and impact:

#### 2.1 Mechanical Refactorings (Safest, Do First)

These are compiler/IDE-verified transformations:

1. **Rename for Clarity**
   ```
   Bad:  int d; // elapsed time in days
   Good: int elapsedDays;
   
   Bad:  void proc();
   Good: void processPayrollForMonth();
   ```

2. **Extract Constants**
   ```
   Bad:  if (status == 3) { ... }
   Good: const int STATUS_APPROVED = 3;
         if (status == STATUS_APPROVED) { ... }
   ```

3. **Extract Method/Function**
   - Each function should do ONE thing
   - Name should describe that one thing completely
   - Ideal length: fits on one screen
   - Rule of thumb: if you need a comment to explain a block, extract it

4. **Inline Unnecessary Abstractions**
   - If a function is called once and adds no clarity, inline it
   - Remove layers that don't earn their keep

#### 2.2 Structural Refactorings

1. **Simplify Conditionals**
   ```
   Bad:
   if (status == 1 || status == 2 || status == 5) {
       if (account.balance > 0) {
           if (user.verified == true) {
               // ... nested complexity
   
   Good:
   if (!canProcessTransaction(status, account, user)) {
       return;
   }
   // ... simple main path
   
   bool canProcessTransaction(int status, Account account, User user) {
       if (!isValidStatus(status)) return false;
       if (account.balance <= 0) return false;
       if (!user.verified) return false;
       return true;
   }
   ```

2. **Replace Type Codes with Types**
   ```
   Bad:
   struct Employee {
       int type; // 0=engineer, 1=salesperson, 2=manager
   };
   
   Good:
   class Employee { virtual double calculateBonus() = 0; };
   class Engineer : public Employee { ... };
   class Salesperson : public Employee { ... };
   class Manager : public Employee { ... };
   ```

3. **Decompose Complex Functions**
   - Extract setup code
   - Extract loop bodies
   - Extract error handling
   - Keep main algorithm visible and clear

4. **Eliminate Temporal Coupling**
   ```
   Bad:
   openConnection();
   authenticate();  // MUST be called after open
   queryData();     // MUST be called after authenticate
   closeConnection();
   
   Good:
   class DatabaseSession {
       DatabaseSession() { /* open and authenticate */ }
       ~DatabaseSession() { /* close */ }
       void query() { /* guaranteed to be authenticated */ }
   };
   ```

#### 2.3 Data Structure Refactorings

1. **Choose the Right Container**
   - Need ordered traversal? → Array/Vector
   - Need fast lookup? → Hash table/Map
   - Need sorted data? → Tree-based map
   - Need fast insertion/deletion at both ends? → Deque
   - Fixed size known at compile time? → Array
   - Small sets? → Sorted array might beat hash table

2. **Improve Data Locality**
   ```
   Bad (AoS - Array of Structures):
   struct Particle {
       vec3 position;
       vec3 velocity;
       float mass;
       vec4 color;
   };
   vector<Particle> particles;
   
   Good for position updates (SoA - Structure of Arrays):
   struct ParticleSystem {
       vector<vec3> positions;
       vector<vec3> velocities;
       vector<float> masses;
       vector<vec4> colors;
   };
   ```

3. **Normalize or Denormalize Appropriately**
   - Normalize to eliminate redundancy and update anomalies
   - Denormalize for performance when reads vastly outnumber writes
   - Document the trade-off explicitly

#### 2.4 Performance Refactorings (MEASURE FIRST)

1. **Eliminate Allocations in Hot Paths**
   ```
   Bad:
   for (int i = 0; i < 1000000; i++) {
       string temp = format("Value: %d", i);
       process(temp);
   }
   
   Good:
   string buffer;
   buffer.reserve(256);
   for (int i = 0; i < 1000000; i++) {
       buffer.clear();
       format_into(buffer, "Value: %d", i);
       process(buffer);
   }
   ```

2. **Hoist Invariants**
   ```
   Bad:
   for (int i = 0; i < n; i++) {
       for (int j = 0; j < m; j++) {
           result[i][j] = data[i][j] * scale * PI * conversion;
       }
   }
   
   Good:
   float factor = scale * PI * conversion;
   for (int i = 0; i < n; i++) {
       for (int j = 0; j < m; j++) {
           result[i][j] = data[i][j] * factor;
       }
   }
   ```

3. **Batch Operations**
   ```
   Bad:
   for (auto& item : items) {
       database.update(item);  // N queries
   }
   
   Good:
   database.batchUpdate(items);  // 1 query
   ```

4. **Use Appropriate Algorithms**
   - Sorting? Know when to use quicksort vs mergesort vs radix sort
   - Searching? Consider binary search, hash tables, or specialized structures
   - String matching? KMP, Boyer-Moore, or just simple loop?
   - Choose based on data characteristics and size

### Phase 3: Verification

After EVERY change:

1. **Run All Tests**
   - Unit tests must pass
   - Integration tests must pass
   - Performance tests must not regress
   
2. **Verify Behavior**
   - Test with actual use cases
   - Check error handling
   - Verify edge cases
   
3. **Measure Performance**
   - If performance was a goal, measure it
   - Use profilers, not guesses
   - Document improvements with numbers

4. **Review the Diff**
   - Is the change obvious?
   - Would you understand this in 6 months?
   - Does it follow project conventions?

### Phase 4: Documentation

1. **Code Should Be Self-Documenting**
   - Clear names eliminate most comment needs
   - Structure reveals intent
   - Types express constraints

2. **Comment the Why, Not the What**
   ```
   Bad:
   // Increment counter
   counter++;
   
   Good:
   // We skip the first element because it's always a sentinel value
   // that the parser uses but the runtime ignores
   startIndex = 1;
   ```

3. **Document Non-Obvious Performance Characteristics**
   ```
   // This uses a linear search because profiles show N is always < 20
   // and the cache coherency benefits outweigh hash table overhead
   ```

4. **Update Related Documentation**
   - API documentation
   - Architecture documents
   - Performance characteristics
   - Known limitations

## Language-Specific Guidelines

### C/C++
- Prefer RAII for resource management
- Use const correctness rigorously
- Be explicit about ownership (raw pointers, unique_ptr, shared_ptr)
- Minimize header dependencies
- Consider cache line alignment for hot structures
- Use inline for truly small, frequently-called functions
- Prefer constexpr for compile-time computations

### Python
- Use type hints (especially for public APIs)
- Prefer comprehensions over map/filter for simple cases
- Use generators for large sequences
- Consider __slots__ for classes with many instances
- Profile before assuming something is slow (Python surprises you)
- Use dataclasses for simple data containers

### JavaScript/TypeScript

> **Comprehensive Examples:** See [examples/javascript-typescript-refactoring-examples.md](examples/javascript-typescript-refactoring-examples.md) for detailed transformations including:
> - Callback Hell → Async/Await
> - Mutating State → Immutable Updates  
> - Prototype Chains → Modern Classes
> - jQuery → Vanilla JavaScript/React
> - Memory Leaks → Proper Cleanup

- Use const by default, let when needed, never var
- Prefer immutable operations where practical
- Use async/await over raw promises
- Consider memory implications of closures
- Avoid premature optimization (V8 is very smart)
- Use TypeScript's strict mode

### Rust
- Leverage the borrow checker—fight it rarely
- Use enum for state machines
- Prefer iter() over for loops when chaining operations
- Use zero-cost abstractions aggressively
- Consider using references instead of clones
- Profile before using unsafe

### Go
- Embrace simplicity—don't fight the language
- Use interfaces sparingly and small
- Prefer struct composition over inheritance-like patterns
- Don't prematurely optimize goroutines
- Profile allocations (pprof is your friend)
- Use defer for cleanup, but be aware of its cost

## Anti-Patterns to Eliminate

> **Real Examples:** See [examples/refactoring-examples.md](examples/refactoring-examples.md) for complete before/after transformations of these anti-patterns in production code.

### 1. Premature Abstraction
**Problem**: Creating abstractions before you understand the problem domain.

**Signs**:
- Interfaces with single implementations
- Abstract base classes with one subclass
- Generic code that's only used specifically
- Configuration options that are never changed

**Fix**: Implement concretely first. Abstract when you have 2-3 similar implementations and understand the commonality.

### 2. Abstraction Inversion
**Problem**: High-level code depending on low-level details it shouldn't know about.

**Fix**: Use dependency injection or interfaces to invert the dependency.

### 3. God Objects/Functions
**Problem**: One thing doing everything.

**Fix**: Single Responsibility Principle—split by concern.

### 4. Primitive Obsession
**Problem**: Using primitives instead of domain types.

```
Bad:
void validateEmail(string email) { ... }
void sendEmail(string email) { ... }

Good:
class EmailAddress {
    EmailAddress(string email) { validate(email); }
    ...
};
void sendEmail(EmailAddress email) { ... }
```

### 5. Speculative Generality
**Problem**: Code written for future cases that may never happen.

**Fix**: YAGNI (You Aren't Gonna Need It). Delete it until you need it.

### 6. Inappropriate Intimacy
**Problem**: Classes that know too much about each other's internals.

**Fix**: Encapsulation—expose behavior, hide data.

## Refactoring Checklist

Before committing refactored code, verify:

- [ ] All tests pass
- [ ] Code is simpler than before (or measurably faster if complexity increased)
- [ ] No functionality changed (or changes are intentional and tested)
- [ ] Names clearly express intent
- [ ] Functions are small and focused
- [ ] No code duplication (or duplication is justified)
- [ ] Performance hasn't regressed (measure if it matters)
- [ ] Memory usage is reasonable
- [ ] Error handling is clear and correct
- [ ] The diff is reviewable (not too large)
- [ ] You would be happy to debug this code at 2 AM

## When NOT to Refactor

1. **Code that works and never changes**: If it's stable and rarely touched, leave it alone.
2. **Code you don't understand**: Study it first, refactor second.
3. **When you don't have tests**: Write tests first.
4. **Under time pressure**: Refactoring requires care and time.
5. **Code that will be deleted soon**: Don't polish what you're throwing away.

## The Refactoring Mindset

1. **Small Steps**: Each refactoring should be small and verifiable.
2. **Continuous**: Refactor as you go, not as a separate phase.
3. **Pragmatic**: Perfect is the enemy of good. Ship good code.
4. **Performance Aware**: Know what your code costs.
5. **Simplicity First**: The simplest solution is usually the best.
6. **Test-Driven**: Tests enable refactoring. Refactoring enables evolution.

## Tools and Techniques

### Static Analysis
- Use linters aggressively (but configure them thoughtfully)
- Track complexity metrics (cyclomatic complexity, cognitive complexity)
- Monitor code coverage (aim for high coverage of critical paths)

### Dynamic Analysis
- Profile before optimizing (CPU, memory, I/O)
- Use sanitizers (AddressSanitizer, ThreadSanitizer, UndefinedBehaviorSanitizer)
- Monitor in production (observability is key)

### IDE Support
- Use automated refactoring tools when available
- Let the compiler/IDE do mechanical transformations
- Leverage static type checking to catch errors

## Example Refactoring Workflow

```
1. Read and understand the code thoroughly
2. Ensure tests exist and pass
3. Identify the worst code smell
4. Make ONE small refactoring to address it
5. Run tests
6. Commit
7. Repeat from step 3

OR if no tests exist:

1. Read and understand the code thoroughly
2. Write characterization tests (tests that capture current behavior)
3. Ensure tests pass
4. Identify the worst code smell
5. Make ONE small refactoring to address it
6. Run tests
7. Commit
8. Repeat from step 4
```

## Measuring Success

Good refactoring results in:
- **Faster Development**: New features are easier to add
- **Fewer Bugs**: Clear code has fewer hiding places for bugs
- **Better Performance**: Understanding enables optimization
- **Easier Onboarding**: New team members get productive faster
- **Higher Confidence**: Tests and clarity enable bold changes

## Final Wisdom

> "Good code is not about being clever. It's about being clear."

> "Make it work, make it right, make it fast—in that order."

> "The best code is no code. The second best is simple code."

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."

> "If you can't explain your code to a beginner, you don't understand it well enough."

## Application in Claude Code

When Claude refactors code:

1. **Always explain WHY** each refactoring improves the code
2. **Show the before and after** with clear annotations
3. **Verify correctness** by running tests or providing test cases
4. **Be honest** about trade-offs (if complexity goes up, performance should justify it)
5. **Respect existing conventions** unless they're actively harmful
6. **Make incremental changes** that can be reviewed and understood
7. **Focus on impact**: Fix the biggest problems first
8. **Measure when performance matters**: Use profilers, not intuition

Remember: The goal is not perfect code. The goal is code that is easy to understand, easy to change, and fast enough. Everything else is vanity.

---

## Additional Resources

This SKILL is part of a comprehensive refactoring toolkit. Continue your learning:

### Quick Access
- **[README.md](README.md)** - Overview, getting started, and success stories
- **[examples/refactoring-quick-reference.md](examples/refactoring-quick-reference.md)** - Pattern catalog for daily use

### Deep Dives
- **[examples/refactoring-examples.md](examples/refactoring-examples.md)** - Production code transformations
  - God Function → Composed Functions (200 lines → 8 lines)
  - Performance Disaster → Cache-Friendly Code (10-100x speedup)
  - Clever Abstraction → Simple Code
  - Allocation Storm → Zero-Allocation Code (100x fewer allocations)

- **[examples/javascript-typescript-refactoring-examples.md](examples/javascript-typescript-refactoring-examples.md)** - Modern web patterns
  - Callback Hell → Async/Await Paradise
  - Mutating State → Immutable Updates
  - Prototype Soup → Modern Classes & Composition
  - jQuery Spaghetti → Clean Architecture
  - Memory Leaks → Proper Cleanup

### Learning Path

1. **Start:** Read [README.md](README.md) for the big picture
2. **Reference:** Keep [examples/refactoring-quick-reference.md](examples/refactoring-quick-reference.md) open while coding
3. **Study:** Work through examples in [examples/](examples/) for your language
4. **Practice:** Apply to your codebase, one smell at a time
5. **Master:** Internalize the principles until they become second nature

### Usage in Claude Code

When refactoring, reference this SKILL with prompts like:

```
"Use the Code Refactoring Excellence SKILL to analyze and improve this code"
"Following the refactoring SKILL, identify the top 3 code smells here"
"Apply Phase 2.1 mechanical refactorings from the SKILL to this function"
"Show me how the SKILL would transform this into immutable patterns"
```

Claude will systematically apply the methodology, explain the reasoning, and produce clean, maintainable code.

---

*"Make it work, make it right, make it fast—in that order."*
