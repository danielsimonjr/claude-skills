# John Carmack Programming Methodology - Claude Code Skill

> "Focused, hard work is the real key to success. Keep your eyes on the goal, and just keep taking the next step towards completing it."  
> — John Carmack

## What Is This?

This is a comprehensive Claude Code skill that teaches and implements the programming philosophy and technical methodology of **John Carmack** — the legendary programmer behind Doom, Quake, pioneering 3D graphics technology, and advances in VR and aerospace software.

Carmack's approach represents decades of learned wisdom in systems programming, performance optimization, and pragmatic software engineering. This skill embodies his philosophy of first-principles thinking, performance-conscious design, and elegant simplicity.

## Why Carmack's Methodology?

John Carmack is renowned for:

- **Revolutionary 3D Graphics**: Created the technology behind Doom, Quake, and modern 3D gaming
- **Performance Mastery**: Legendary ability to squeeze maximum performance from hardware
- **First-Principles Thinking**: Understanding systems from the ground up, not just using abstractions
- **Pragmatic Engineering**: Choosing simple, working solutions over theoretical perfection
- **Continuous Learning**: Constantly evolving techniques based on measured results
- **Technical Leadership**: Influential work at id Software, Oculus VR, and Armadillo Aerospace

His code powers everything from classic games to modern VR systems, and his approach to programming emphasizes understanding over abstraction, measurement over intuition, and simplicity over cleverness.

## Core Philosophy

### The Carmack Programming Principles

**1. Understand the Machine**
```c
"The more you understand about what the hardware is actually doing,
the better programmer you will be."
```

Know what happens at the silicon level. Cache hierarchies, instruction pipelines, memory bandwidth — these determine real performance.

**2. Simplicity Is Paramount**
```c
"The cost of adding a feature isn't just the time it takes to code it.
The cost also includes the addition of an obstacle to future expansion."
```

The best code is code that doesn't need to exist. Solve problems with the minimum necessary complexity.

**3. Measure, Don't Guess**
```c
"It's important to measure what you're optimizing. 
Otherwise you're just guessing, and that's a waste of time."
```

Use profilers. Let data drive decisions. Intuition is valuable, but measurement is truth.

**4. Optimize What Matters**
```c
"Premature optimization is the root of all evil. But late optimization
is the root of all performance problems."
```

90% of time is spent in 10% of code. Find that 10% and make it perfect. Keep everything else clean.

**5. Pragmatism Over Dogma**
```c
"I'm not a fan of software engineering's typical abstraction approach. 
It's often not the right solution."
```

Use globals when appropriate. Skip dependency injection if it adds complexity. Question "best practices."

## What's Included

### 📚 Documentation

1. **SKILL.md** — Complete methodology guide
   - First principles engineering approach
   - Cache-conscious programming
   - SIMD optimization techniques
   - Memory management strategies
   - Algorithm selection criteria
   - Code organization patterns
   - Anti-patterns to avoid
   - Testing philosophy

2. **IMPLEMENTATION_GUIDE.md** — Practical examples
   - Project structure
   - Platform abstraction layer
   - SIMD-optimized math library
   - Custom memory allocators
   - Entity component system
   - Complete working examples

3. **RENDERING_PROFILING.md** — Advanced topics
   - OpenGL rendering system
   - State-change minimization
   - Render queue sorting
   - Built-in profiler
   - Complete game loop
   - Optimization techniques
   - Debugging tools

4. **README.md** (this file) — Overview and philosophy

### 🎯 Key Topics Covered

**Performance Programming**
- Cache-friendly data structures (SoA vs AoS)
- SIMD vectorization (SSE/AVX)
- Branch elimination techniques
- Memory bandwidth optimization
- Lock-free programming

**Memory Management**
- Arena allocators
- Pool allocators
- Stack allocators
- Frame-based allocation
- Minimal heap usage

**Systems Architecture**
- Unity builds
- Minimal dependencies
- Data-driven design
- Component-based entities
- State machines over inheritance

**Graphics Programming**
- Render queue optimization
- State change minimization
- Shader management
- Mesh batching
- GPU programming principles

**Development Practice**
- Built-in profiling
- Visual debugging
- Assertion-driven development
- Iterative optimization
- Measurement-based improvement

## Quick Start

### Using This Skill with Claude Code

When you ask Claude Code to help with programming tasks, reference this methodology:

```
"Using the Carmack programming methodology, help me optimize this physics system"
"Create a memory allocator following Carmack's approach"
"Refactor this code to be more cache-friendly per the Carmack skill"
```

### Key Commands to Claude Code

**Starting a New Project**
```
"Set up a new C project using Carmack's project structure with unity build"
```

**Performance Work**
```
"Profile this code and suggest optimizations based on Carmack's principles"
"Convert this to use arena allocation instead of malloc"
"Make this loop cache-friendly with SIMD"
```

**Code Review**
```
"Review this code using Carmack's checklist"
"Simplify this following first-principles thinking"
```

## The Carmack Approach in Action

### Example 1: Cache-Friendly Particle System

**Before (Bad)**
```c
struct Particle {
    Vec3 position;
    Vec3 velocity;
    Color color;
    float life;
};
Particle particles[10000];

// Updates touch all particle data, even what we don't need
for (int i = 0; i < count; i++) {
    particles[i].position += particles[i].velocity * dt;
}
```

**After (Carmack Style)**
```c
struct ParticleSystem {
    float* px, *py, *pz;     // Positions
    float* vx, *vy, *vz;     // Velocities
    uint32_t* colors;        // Separate, not loaded
    float* life;
};

// Only touch position and velocity - perfect cache utilization
for (int i = 0; i < count; i += 4) {
    __m128 x = _mm_load_ps(&px[i]);
    __m128 vx = _mm_load_ps(&vx[i]);
    x = _mm_add_ps(x, _mm_mul_ps(vx, dt_vec));
    _mm_store_ps(&px[i], x);
}
```

**Result**: 3-5x faster due to cache efficiency and SIMD

### Example 2: Simple Over Complex

**Before (Over-Engineered)**
```c
class IRenderer {
    virtual void drawMesh(Mesh* m) = 0;
};

class OpenGLRenderer : public IRenderer {
    void drawMesh(Mesh* m) override { /* ... */ }
};

class VulkanRenderer : public IRenderer {
    void drawMesh(Mesh* m) override { /* ... */ }
};

// You don't have two renderers. You won't have two renderers.
```

**After (Carmack Style)**
```c
void drawMesh(Mesh* m) {
    glBindVertexArray(m->vao);
    glDrawElements(GL_TRIANGLES, m->indexCount, GL_UNSIGNED_INT, 0);
}

// If you need a second backend later, write it then.
// Don't predict the future.
```

**Result**: Simpler, faster, more maintainable

### Example 3: Profile-Driven Optimization

**The Process**
```c
// 1. Make it work
void checkCollisions_v1(Entity* entities, int count) {
    for (int i = 0; i < count; i++) {
        for (int j = i + 1; j < count; j++) {
            if (collides(entities[i], entities[j])) {
                resolve(entities[i], entities[j]);
            }
        }
    }
}

// 2. Profile: "80% of frame time here"

// 3. Optimize based on measurement
void checkCollisions_v2(Entity* entities, int count) {
    SpatialGrid* grid = buildGrid(entities, count);
    for (int i = 0; i < count; i++) {
        Entity** nearby = gridQuery(grid, entities[i]);
        for (int j = 0; nearby[j]; j++) {
            if (collides(entities[i], *nearby[j])) {
                resolve(entities[i], *nearby[j]);
            }
        }
    }
}

// 4. Measure: "Now 5% of frame time - SUCCESS"
```

## Famous Carmack Wisdom

### On Code Quality

> "In the information age, the barriers just aren't there. The barriers are self imposed. If you want to set off and go develop some grand new thing, you don't need millions of dollars of capitalization. You need enough pizza and Diet Coke to stick in your refrigerator, a cheap PC to work on, and the dedication to go through with it."

> "Because of the nature of Moore's law, anything that an extremely clever graphics programmer can do at one point can be replicated by a merely competent programmer some number of years later."

> "It's done when it ships."

### On Optimization

> "The situation isn't that people are writing slow code and making it fast. People are writing ridiculously slow code and making it mediocre."

> "Everybody's saturated with programming information. We all know about objects and inheritance and polymorphism and exception handling. We're all on the same page there. Where we differentiate ourselves is in our familiarity with particular domains."

### On Simplicity

> "Sometimes the elegant implementation is just a function. Not a method. Not a class. Not a framework. Just a function."

> "The fundamental problem with program development is that the complexity of the systems we build is limited primarily by our ability to comprehend them. Code structure, modularity, design patterns, all these things exist to help manage that complexity."

### On Learning

> "I think the most important thing is to have a passion for what you're doing. If you're doing it because it's cool, or because you want to make money, you're probably not going to have the stamina to go through the tough times."

> "Make something you want to exist in the world."

> "The best person to build something is someone who actually wants to use it."

## The Carmack Development Workflow

```
┌─────────────────────────────────────────────────┐
│ 1. UNDERSTAND THE PROBLEM                       │
│    • What are we actually trying to achieve?    │
│    • What does the hardware need to do?         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 2. IMPLEMENT THE SIMPLE SOLUTION                │
│    • Write the obvious code first               │
│    • Make it correct, not fast                  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 3. MEASURE ACTUAL PERFORMANCE                   │
│    • Profile with real data                     │
│    • Identify actual bottlenecks                │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 4. OPTIMIZE HOT PATHS                           │
│    • Focus on measured bottlenecks              │
│    • Apply appropriate techniques               │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 5. VERIFY CORRECTNESS                           │
│    • Test thoroughly                            │
│    • Ensure optimization didn't break code      │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 6. MEASURE IMPROVEMENT                          │
│    • Confirm optimization helped                │
│    • Document results                           │
└─────────────────────────────────────────────────┘
                      ↓
              ITERATE OR DONE
```

## Checklist: Writing Carmack-Style Code

Use this checklist when writing or reviewing code:

### Before Writing Code

- [ ] Do I understand this problem at the hardware level?
- [ ] What is the simplest solution that could work?
- [ ] Can I solve this without adding new abstractions?
- [ ] Have I checked if similar code already exists?

### While Writing Code

- [ ] Is this the minimum code needed to solve the problem?
- [ ] Can a less experienced programmer understand this?
- [ ] Are my assumptions documented and asserted?
- [ ] Am I avoiding premature optimization?
- [ ] Would data be better than code here?

### Performance-Critical Code

- [ ] Have I profiled to confirm this is a hot path?
- [ ] Is this data structure cache-friendly?
- [ ] Can I eliminate branches in the inner loop?
- [ ] Could SIMD help here?
- [ ] Am I minimizing memory allocations?

### Before Committing

- [ ] Does this compile with -Wall -Werror and zero warnings?
- [ ] Have I tested edge cases?
- [ ] Can I delete any of this code?
- [ ] Is this simpler than what it replaces?
- [ ] Will I understand this in 6 months?

## Common Anti-Patterns (What NOT to Do)

### ❌ Excessive Abstraction

```c
// DON'T: Abstract for hypothetical future needs
class AbstractEntityFactoryBuilder {
    virtual Entity* createEntity() = 0;
};

// DO: Write what you need today
Entity* createEntity(EntityType type) {
    Entity* e = malloc(sizeof(Entity));
    initEntity(e, type);
    return e;
}
```

### ❌ Premature Optimization

```c
// DON'T: Optimize before measuring
// *spends 3 days optimizing matrix multiplication*
// *profiler shows it's 0.1% of frame time*

// DO: Profile first, optimize hot paths
// *profiler shows collision detection is 60% of frame time*
// *optimize that instead*
```

### ❌ Dependency Injection Everywhere

```c
// DON'T: Inject everything
class Game {
    IRenderer* renderer;
    IPhysics* physics;
    IAudio* audio;
    IInput* input;
    INetwork* network;
    // Constructor from hell...
};

// DO: Use globals for engine services
extern Renderer* g_renderer;
extern Physics* g_physics;

void gameUpdate(void) {
    updatePhysics(g_physics);
    drawFrame(g_renderer);
}
```

## When to Use This Methodology

### Perfect For:

- ✅ Game engines and graphics programming
- ✅ Real-time systems (physics, audio, rendering)
- ✅ Performance-critical applications
- ✅ Systems programming (OS, drivers, embedded)
- ✅ Scientific computing and simulations
- ✅ When you need to understand and control everything

### Less Suitable For:

- ❌ Web applications with changing requirements
- ❌ Projects with many external dependencies
- ❌ Applications where developer productivity >> runtime performance
- ❌ When you're prototyping and exploring the problem space
- ❌ Large teams with varying skill levels

## Integration with Claude Code

Claude Code can help you apply these principles by:

1. **Analyzing Code**: "Review this code using Carmack's methodology"
2. **Optimizing**: "Make this cache-friendly with SoA layout"
3. **Simplifying**: "Simplify this using first-principles thinking"
4. **Profiling**: "Add profiling instrumentation to find bottlenecks"
5. **Refactoring**: "Convert this to use arena allocation"

### Example Session

```
You: "I have a particle system that's running slow. Help me optimize it."

Claude Code: *reads the Carmack skill*
"Let me profile this first. I'll add timing instrumentation..."
*adds profiling code*
"The bottleneck is in the update loop - 80% of frame time. 
Let me convert this to use SoA layout for cache efficiency..."
*refactors to structure-of-arrays*
*adds SIMD vectorization*
"This should be 3-4x faster. Let's measure to confirm..."
```

## Learning Path

### Beginner

1. Read SKILL.md sections:
   - Core Philosophy
   - First Principles Engineering
   - Code Organization
   
2. Study examples in IMPLEMENTATION_GUIDE.md:
   - Memory arenas
   - Simple entity system
   - Basic profiling

### Intermediate

1. Deep dive into performance topics:
   - Cache-conscious programming
   - SIMD optimization
   - Memory allocation strategies
   
2. Implement examples:
   - Convert project to unity build
   - Add custom allocators
   - Profile and optimize hot paths

### Advanced

1. Master advanced techniques:
   - Lock-free programming
   - GPU optimization
   - Custom build systems
   
2. Apply to real projects:
   - Game engine components
   - Physics simulations
   - Rendering systems

## Resources for Further Learning

### John Carmack's Own Words

- **Blog**: [John Carmack's .plan files](http://www.altdev.co/2011/09/15/john-carmacks-plan-files/) (historical development notes)
- **Interviews**: Search for Carmack interviews on YouTube
- **Twitter**: [@ID_AA_Carmack](https://twitter.com/ID_AA_Carmack)

### Books Aligned with This Philosophy

- *Game Engine Architecture* by Jason Gregory
- *Real-Time Rendering* by Akenine-Möller et al.
- *Computer Systems: A Programmer's Perspective* by Bryant & O'Hallaron
- *Physically Based Rendering* by Pharr, Jakob, & Humphreys

### Technical Resources

- Intel Architecture Optimization Manuals
- Agner Fog's optimization guides
- GPU architecture white papers
- SIMD intrinsics guides

## Contributing

This skill is designed to evolve. If you find improvements or want to add examples:

1. Test the code thoroughly
2. Follow the Carmack principles outlined here
3. Measure performance impact
4. Document your reasoning

Remember: "The best code is code that doesn't need to exist."

## Final Thoughts

> "Focus on the fundamentals. Everything else is just details."  
> — John Carmack

This skill isn't about blindly copying Carmack's code. It's about adopting his mindset:

- **Understand deeply** rather than accepting abstractions
- **Measure rigorously** rather than guessing
- **Simplify relentlessly** rather than adding complexity
- **Optimize intelligently** where it matters
- **Stay pragmatic** over dogmatic

The goal is to write code that is fast, clear, and maintainable. Code that you'll be proud of six months from now. Code that solves real problems efficiently.

Now go write something amazing. 🚀

---

*"The best person to build something is someone who actually wants to use it."*  
*— John Carmack*
