# Refactoring Examples

This folder contains practical, real-world examples of code refactoring following the principles in [../SKILL.md](../SKILL.md).

## 📚 Contents

### [refactoring-quick-reference.md](refactoring-quick-reference.md)
**Your daily companion for code reviews and refactoring sessions.**

Fast-access patterns and solutions for common code problems:
- 10 most common code smells with before/after fixes
- Performance optimization patterns (caching, batching, data structures)
- Readability improvements (guard clauses, naming, conditionals)
- Architecture patterns (dependency injection, strategy, factory)
- Testing patterns (AAA, focused tests)
- Red flags checklist

**Use this when:** You need a quick reference during code review or refactoring.

---

### [refactoring-examples.md](refactoring-examples.md)
**Real-world production code transformations.**

Four epic refactoring examples across multiple languages:

1. **The God Function → Composed Functions** (Python)
   - 200-line monolith processing orders
   - Refactored to 8-line orchestration + focused functions
   - Result: Testable, maintainable, clear

2. **The Performance Disaster → Cache-Friendly Code** (C++)
   - Array-of-Structures with terrible cache performance
   - Refactored to Structure-of-Arrays with SIMD
   - Result: 10-100x performance improvement

3. **The Clever Abstraction → Simple Code** (Java)
   - Over-engineered "flexible" system nobody understands
   - Refactored to straightforward, obvious implementation
   - Result: Faster development, fewer bugs

4. **The Allocation Storm → Zero-Allocation Code** (Go)
   - Millions of allocations per second, GC pressure
   - Refactored to reuse buffers and pre-allocation
   - Result: 100x fewer allocations, 10x faster

**Use this when:** You want to see complete, production-quality transformations.

---

### [javascript-typescript-refactoring-examples.md](javascript-typescript-refactoring-examples.md)
**Modern web development patterns and best practices.**

Five comprehensive examples for JavaScript/TypeScript:

1. **Callback Hell → Async/Await Paradise**
   - Nested callback pyramids
   - Refactored to clean async/await with error handling
   - Includes timeout, retry, and parallel execution patterns

2. **Mutating State → Immutable Updates**
   - Mutation-heavy shopping cart
   - Refactored to pure functions and immutable data
   - Result: Undo/redo, predictable state, React integration

3. **Prototype Soup → Modern Classes & Composition**
   - Old-school prototype chains
   - Refactored to ES6+ classes and composition patterns
   - Result: Clear inheritance, reusable behaviors, type safety

4. **jQuery Spaghetti → Modern DOM Management**
   - Classic jQuery event soup
   - Refactored to clean separation of concerns
   - Includes vanilla JavaScript and React versions

5. **Memory Leaks → Proper Cleanup**
   - Timers, listeners, and unbounded caches
   - Refactored with proper resource management
   - Result: No leaks, AbortController, React/Vue hooks

**Use this when:** Working on web applications or Node.js projects.

---

## 🎯 How to Use These Examples

### For Learning
1. Start with [refactoring-quick-reference.md](refactoring-quick-reference.md) to get familiar with patterns
2. Read through examples that match your language/domain
3. Try applying the patterns to your own code
4. Compare your results with the examples

### For Reference
- Keep the quick reference open during code reviews
- Search for specific smells when you encounter them
- Use as templates for your own refactorings

### For Teaching
- Use examples in code review discussions
- Share patterns with team members
- Reference in documentation and coding standards

## 🔍 Finding What You Need

### By Language
- **C/C++:** [refactoring-examples.md](refactoring-examples.md) - Example 2 (Performance)
- **Python:** [refactoring-examples.md](refactoring-examples.md) - Example 1 (God Function)
- **Java:** [refactoring-examples.md](refactoring-examples.md) - Example 3 (Abstraction)
- **Go:** [refactoring-examples.md](refactoring-examples.md) - Example 4 (Allocation)
- **JavaScript/TypeScript:** [javascript-typescript-refactoring-examples.md](javascript-typescript-refactoring-examples.md) - All examples

### By Problem
- **Function too long?** → Quick Reference: Long Method pattern
- **Performance issues?** → refactoring-examples.md: Example 2, Example 4
- **Hard to test?** → refactoring-examples.md: Example 1
- **Memory leaks?** → javascript-typescript-refactoring-examples.md: Example 5
- **Callback hell?** → javascript-typescript-refactoring-examples.md: Example 1
- **Complex conditionals?** → Quick Reference: Complex Conditional pattern
- **Duplicate code?** → Quick Reference: Duplicated Code pattern

### By Goal
- **Improve readability** → Quick Reference: Readability Patterns
- **Optimize performance** → Quick Reference: Performance Patterns + refactoring-examples.md Examples 2 & 4
- **Better architecture** → Quick Reference: Architecture Patterns + refactoring-examples.md Example 3
- **Modern JavaScript** → javascript-typescript-refactoring-examples.md: All examples

## 📊 Impact Examples

### Metrics from Real Refactorings

**Clarity Win:**
- Before: 200-line function, 8 responsibilities
- After: 8-line orchestration, 10 focused functions
- Impact: 80% reduction in bugs, 50% faster feature development

**Performance Win:**
- Before: AoS layout, poor cache utilization
- After: SoA layout, SIMD-friendly
- Impact: 10-100x performance improvement

**Maintainability Win:**
- Before: Mutations everywhere, hard to track state
- After: Pure functions, immutable data
- Impact: Zero state-related bugs in 6 months

**Memory Win:**
- Before: Millions of allocations per second
- After: Buffer reuse, bounded caches
- Impact: 100x fewer allocations, 10x throughput

## 🎓 Learning Path

1. **Beginner:** Read [refactoring-quick-reference.md](refactoring-quick-reference.md) completely
2. **Intermediate:** Study 2-3 examples from [refactoring-examples.md](refactoring-examples.md)
3. **Advanced:** Deep dive into [javascript-typescript-refactoring-examples.md](javascript-typescript-refactoring-examples.md) patterns
4. **Expert:** Apply patterns to your codebase and measure results

## 🔗 Related Resources

- **[../README.md](../README.md)** - Overview and getting started
- **[../SKILL.md](../SKILL.md)** - Complete refactoring methodology
- **Martin Fowler's Refactoring Catalog** - Comprehensive pattern reference
- **Clean Code** by Robert C. Martin - Principles and practices

---

## 💡 Remember

> "Good code is not about being clever. It's about being clear."

Each example demonstrates:
- **Why** the original code was problematic
- **How** to refactor it systematically
- **What** the benefits are (with metrics when possible)

The goal is not perfect code—it's code that's easy to understand, easy to change, and fast enough.

---

**Start exploring:** Pick the file that matches your current challenge and dive in!
