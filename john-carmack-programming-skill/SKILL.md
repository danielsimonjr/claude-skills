---
name: carmack-programming
description: Program with John Carmack's philosophy of first-principles thinking, performance optimization, and pragmatic engineering excellence. Use when writing performance-critical code, optimizing systems, doing low-level programming, or when the user wants Carmack-style engineering rigor with emphasis on simplicity, measurement, and deep technical understanding.
---

# Carmack Programming Methodology

## Overview

This skill enables Claude Code to program with the philosophy, rigor, and technical excellence exemplified by John Carmack - legendary programmer behind Doom, Quake, and pioneering work in 3D graphics, VR, and aerospace. This methodology emphasizes first-principles thinking, performance optimization, deep technical understanding, and pragmatic engineering excellence.

## Core Philosophy

### First Principles Engineering

John Carmack's approach begins with fundamental understanding rather than accumulated abstractions. When implementing solutions:

1. **Understand the Hardware**: Know what's actually happening at the silicon level. Cache behavior, instruction pipelines, memory hierarchies - these aren't abstract concepts but concrete realities that determine performance.

2. **Question Assumptions**: Don't accept conventional wisdom without verification. If everyone says X is slow, measure it yourself. The industry is full of outdated assumptions and cargo cult practices.

3. **Simplify Relentlessly**: The best code is code that doesn't exist. Every line is a liability. Before adding complexity, exhaust simpler solutions.

4. **Measure, Don't Guess**: Performance intuition is valuable, but profilers don't lie. Measure actual bottlenecks, not theoretical ones.

### The Carmack Programming Mindset

```
"The cost of adding a feature isn't just the time it takes to code it. 
The cost also includes the addition of an obstacle to future expansion. 
The trick is to pick the features that don't fight each other."
- John Carmack
```

When writing code in this style:

- **Favor clarity over cleverness**: Code is read more than written. A straightforward solution that a junior programmer can understand beats an elegant hack that requires deep expertise to maintain.

- **Optimize hot paths ruthlessly**: 90% of execution time is in 10% of code. Find that 10% and make it perfect. The other 90% can be readable and maintainable.

- **Embrace controlled coupling**: Loose coupling everywhere creates indirection that kills performance and comprehension. Strategic coupling in performance-critical code is acceptable.

- **Write self-contained systems**: Minimize dependencies. Each system should be understandable in isolation.

## Technical Principles

### 1. Performance-Oriented Design

#### Cache Consciousness

Modern CPUs are memory-bound, not compute-bound. Design data structures for cache efficiency:

```c
// BAD: Array of structures (AoS) - cache inefficient
struct Particle {
    float x, y, z;      // Position
    float vx, vy, vz;   // Velocity
    float r, g, b, a;   // Color
    float life;
};
Particle particles[10000];

// Update loop brings in unnecessary data
for (int i = 0; i < count; i++) {
    particles[i].x += particles[i].vx * dt;
    particles[i].y += particles[i].vy * dt;
    particles[i].z += particles[i].vz * dt;
    // Cache line contains color and life data we don't need
}

// GOOD: Structure of arrays (SoA) - cache friendly
struct ParticleSystem {
    float* x;           // Contiguous positions
    float* y;
    float* z;
    float* vx;          // Contiguous velocities
    float* vy;
    float* vz;
    float* colors;      // Separate, not loaded during physics
    float* life;
};

// Update loop only touches position and velocity arrays
for (int i = 0; i < count; i++) {
    x[i] += vx[i] * dt;
    y[i] += vy[i] * dt;
    z[i] += vz[i] * dt;
    // Perfect cache utilization, SIMD-friendly
}
```

#### Minimize Branching in Hot Loops

Branch prediction misses are expensive. Branchless code often wins:

```c
// Conditional with branches - prediction misses hurt
if (value > threshold) {
    result = computeExpensive(value);
} else {
    result = computeCheap(value);
}

// Branchless alternative (when appropriate)
int mask = -(value > threshold);  // -1 if true, 0 if false
result = (mask & computeExpensive(value)) | (~mask & computeCheap(value));

// Or use SIMD-friendly select operations
result = select(value > threshold, computeExpensive(value), computeCheap(value));
```

#### Memory Allocation Strategy

```c
// BAD: Allocations in inner loops
for (int i = 0; i < 1000000; i++) {
    Entity* e = malloc(sizeof(Entity));  // Slow, fragmenting
    processEntity(e);
    free(e);
}

// GOOD: Pool allocator, linear allocator, or arena
typedef struct {
    void* memory;
    size_t used;
    size_t capacity;
} Arena;

Arena frame_arena = createArena(MEGABYTES(16));
for (int i = 0; i < 1000000; i++) {
    Entity* e = arenaAlloc(&frame_arena, sizeof(Entity));
    processEntity(e);
    // Don't free individual items
}
arenaReset(&frame_arena);  // Reset entire arena at frame end
```

### 2. Code Organization

#### Single Compilation Unit (Unity Build)

Carmack popularized unity builds where multiple source files are included into one translation unit:

```c
// build.c - single compilation unit
#include "math.c"
#include "renderer.c"
#include "physics.c"
#include "game.c"

// Compile: gcc -O3 build.c -o game
// Benefits:
// - Maximum LTO opportunities
// - Faster full rebuilds
// - Better inlining across "modules"
// - Simpler build system
```

#### Header File Philosophy

Minimize header dependencies. Headers should be minimal, self-contained:

```c
// GOOD: Minimal header
#ifndef RENDERER_H
#define RENDERER_H

typedef struct Renderer Renderer;  // Opaque pointer

Renderer* rendererCreate(void);
void rendererDestroy(Renderer* r);
void rendererDrawFrame(Renderer* r);

#endif

// Implementation has full struct definition
// renderer.c
struct Renderer {
    // Implementation details hidden
};
```

### 3. Algorithm Selection

#### Favor Linear Scans Over Fancy Data Structures

For small to medium datasets, linear scans beat "optimal" data structures:

```c
// For N < ~1000, this is often faster than hash table or tree:
Entity* findEntityByID(Entity* entities, int count, int id) {
    for (int i = 0; i < count; i++) {
        if (entities[i].id == id) {
            return &entities[i];
        }
    }
    return NULL;
    // Simple, cache-friendly, branch-predictor-friendly
    // Beats hash table overhead for small N
}
```

#### Approximate Solutions

Perfect accuracy isn't always necessary:

```c
// Fast inverse square root (Quake III)
float fastInvSqrt(float x) {
    float xhalf = 0.5f * x;
    int i = *(int*)&x;              // Evil floating point bit hack
    i = 0x5f3759df - (i >> 1);      // Initial guess with magic constant
    x = *(float*)&i;
    x = x * (1.5f - xhalf * x * x); // Newton iteration
    return x;
}

// Modern: Use hardware reciprocal square root
float fastInvSqrt_SSE(float x) {
    __m128 temp = _mm_set_ss(x);
    temp = _mm_rsqrt_ss(temp);  // Hardware approximation
    return _mm_cvtss_f32(temp);
}
```

### 4. Debugging and Verification

#### Assertions Everywhere

```c
#define ASSERT(expr) if (!(expr)) { \
    fprintf(stderr, "Assertion failed: %s\n  File: %s\n  Line: %d\n", \
            #expr, __FILE__, __LINE__); \
    abort(); \
}

void updateEntity(Entity* e, float dt) {
    ASSERT(e != NULL);
    ASSERT(dt > 0.0f && dt < 1.0f);  // Sanity check
    ASSERT(e->health >= 0.0f);       // Invariant check
    
    // Implementation
    
    ASSERT(e->health >= 0.0f);       // Post-condition
}
```

#### Built-in Profiling

```c
typedef struct {
    const char* name;
    uint64_t start;
    uint64_t total;
    int count;
} ProfileZone;

#define PROFILE_SCOPE(name) \
    ProfileZone zone = {name, readCPUTimer(), 0, 0}; \
    defer(profileEnd(&zone));

void updatePhysics(void) {
    PROFILE_SCOPE("Physics");
    // Physics code
}

void renderFrame(void) {
    PROFILE_SCOPE("Render");
    // Render code
}
```

## Programming Patterns

### State Machines Over Object Hierarchies

```c
// AVOID: Deep inheritance hierarchies
class Entity { virtual void update(); };
class MovingEntity : public Entity { };
class AIEntity : public MovingEntity { };
class Enemy : public AIEntity { };
// Brittle, hard to reason about, vtable overhead

// PREFER: Explicit state machines
typedef enum {
    ENTITY_IDLE,
    ENTITY_MOVING,
    ENTITY_ATTACKING,
    ENTITY_DEAD
} EntityState;

typedef struct {
    EntityState state;
    float stateTime;
    // Data for all states together
    Vector3 position;
    Vector3 velocity;
    float health;
} Entity;

void updateEntity(Entity* e, float dt) {
    e->stateTime += dt;
    
    switch (e->state) {
        case ENTITY_IDLE:
            // Handle idle
            if (shouldAttack(e)) {
                e->state = ENTITY_ATTACKING;
                e->stateTime = 0;
            }
            break;
        case ENTITY_MOVING:
            // Handle movement
            break;
        // etc.
    }
}
```

### Data-Driven Design

```c
// Configuration in data, not code
typedef struct {
    const char* name;
    float speed;
    float health;
    float damage;
    int modelID;
} EnemyTemplate;

EnemyTemplate templates[] = {
    {"Imp",     3.0f, 60.0f,  5.0f, MODEL_IMP},
    {"Demon",   5.0f, 150.0f, 15.0f, MODEL_DEMON},
    {"Baron",   4.0f, 1000.0f, 40.0f, MODEL_BARON},
};

Entity* spawnEnemy(const char* type) {
    EnemyTemplate* tmpl = findTemplate(type);
    Entity* e = allocEntity();
    e->speed = tmpl->speed;
    e->health = tmpl->health;
    e->damage = tmpl->damage;
    return e;
}
```

### System-Based Architecture

```c
// Systems operate on all entities with specific components
void physicsSystem(Entity* entities, int count, float dt) {
    for (int i = 0; i < count; i++) {
        if (entities[i].flags & HAS_PHYSICS) {
            entities[i].position += entities[i].velocity * dt;
            entities[i].velocity += GRAVITY * dt;
        }
    }
}

void renderSystem(Entity* entities, int count) {
    for (int i = 0; i < count; i++) {
        if (entities[i].flags & HAS_RENDER) {
            drawModel(entities[i].modelID, entities[i].position);
        }
    }
}
```

## Optimization Workflow

### The Carmack Optimization Process

1. **Make it work**: Get the algorithm correct first
2. **Make it right**: Clean up the code, ensure correctness
3. **Profile**: Find actual bottlenecks with real data
4. **Optimize hot paths**: Focus on the 10% that matters
5. **Verify**: Ensure optimization didn't break correctness
6. **Measure again**: Confirm the optimization helped

```c
// Example: Optimizing collision detection

// Step 1: Naive but correct
void checkCollisions_v1(Entity* entities, int count) {
    for (int i = 0; i < count; i++) {
        for (int j = i + 1; j < count; j++) {
            if (circleCollision(&entities[i], &entities[j])) {
                handleCollision(&entities[i], &entities[j]);
            }
        }
    }
}
// Works but O(n²)

// Step 2: Profile shows this is 80% of frame time

// Step 3: Spatial partitioning
void checkCollisions_v2(Entity* entities, int count) {
    // Broad phase: spatial hash grid
    Grid* grid = buildGrid(entities, count);
    
    for (int i = 0; i < count; i++) {
        // Only check nearby entities
        Entity** nearby = gridGetNearby(grid, &entities[i]);
        for (int j = 0; nearby[j]; j++) {
            if (circleCollision(&entities[i], nearby[j])) {
                handleCollision(&entities[i], nearby[j]);
            }
        }
    }
}
// Now O(n) for well-distributed entities

// Step 4: SIMD narrow phase (if profiler shows collision test is hot)
bool circleCollision_SIMD(Entity* a, Entity* b) {
    __m128 posA = _mm_load_ps(&a->position);
    __m128 posB = _mm_load_ps(&b->position);
    __m128 diff = _mm_sub_ps(posA, posB);
    __m128 squared = _mm_mul_ps(diff, diff);
    
    float distSq = squared.m128_f32[0] + squared.m128_f32[1];
    float radiusSum = a->radius + b->radius;
    
    return distSq < radiusSum * radiusSum;
}
```

## Modern Adaptations

### When to Use Modern C++ Features

Carmack has evolved to use C++ pragmatically. Use modern features when they improve code without sacrificing performance:

```cpp
// Good uses of C++:

// 1. RAII for resource management
class ScopedTimer {
    const char* name;
    uint64_t start;
public:
    ScopedTimer(const char* n) : name(n), start(readCPUTimer()) {}
    ~ScopedTimer() {
        uint64_t elapsed = readCPUTimer() - start;
        logTime(name, elapsed);
    }
};

// 2. Templates for type-safe generics (not excessive metaprogramming)
template<typename T>
struct Array {
    T* data;
    int count;
    int capacity;
    
    T& operator[](int i) { 
        ASSERT(i >= 0 && i < count);
        return data[i]; 
    }
};

// 3. Lambdas for callbacks
std::sort(entities, entities + count, 
    [](const Entity& a, const Entity& b) {
        return a.distance < b.distance;
    }
);

// AVOID: Complex template metaprogramming, deep inheritance,
// virtual functions in hot paths, exceptions
```

### GPU Programming

Carmack pioneered GPU optimization. Modern graphics programming principles:

```glsl
// Vertex shader: Minimal work, batch transforms
#version 450

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texcoord;

layout(binding = 0) uniform Transforms {
    mat4 viewProj;
    mat4 model;
} transforms;

layout(location = 0) out vec3 fragNormal;
layout(location = 1) out vec2 fragTexcoord;

void main() {
    gl_Position = transforms.viewProj * transforms.model * vec4(position, 1.0);
    fragNormal = mat3(transforms.model) * normal;
    fragTexcoord = texcoord;
}

// Fragment shader: Do heavy lifting here
// GPU has thousands of cores for parallel fragment processing
```

## Communication and Documentation

### Code Should Be Self-Documenting

```c
// BAD: Comments explaining what code does
// Increment the counter
counter++;

// Add velocity to position
pos.x += vel.x;

// GOOD: Code that doesn't need comments
position += velocity * deltaTime;
entity->framesSinceLastAttack++;

// GOOD: Comments explaining WHY
// We update physics before rendering to avoid one-frame lag
// in player response to input
updatePhysics(dt);
updateRenderer();

// Cache coherency: Process all positions, then all velocities
// This is 3x faster than interleaved access
for (int i = 0; i < count; i++) positions[i] += velocities[i] * dt;
```

### Technical Design Documents

When writing design docs in Carmack style:

```markdown
## Renderer Refactor Proposal

### Problem
Current renderer does redundant state changes (300+ per frame).
Profiler shows 15% of frame time in OpenGL driver.

### Solution
Sort draw calls by (shader, texture, mesh) before submission.

### Implementation
1. Build RenderKey from state: `key = (shaderID << 40) | (textureID << 20) | meshID`
2. Radix sort commands by key (O(n), cache-friendly)
3. Submit in sorted order

### Expected Gains
- Measured on test scene: 300 → 45 state changes
- Estimated: 2.5ms → 0.8ms driver overhead
- Risk: Low, changes isolated to submission loop

### Alternatives Considered
- Command buffer API: Too complex for marginal gain
- Manual batching: Too brittle, already sort-based approach is general

### Timeline
2 days implementation, 1 day testing
```

## Anti-Patterns to Avoid

### Premature Abstraction

```c
// BAD: Abstract too early
class IRenderer {
    virtual void drawMesh(Mesh* m) = 0;
    virtual void setShader(Shader* s) = 0;
};

class OpenGLRenderer : public IRenderer { /* ... */ };
class VulkanRenderer : public IRenderer { /* ... */ };

// You don't have multiple renderers. You won't have multiple renderers.
// This is wasted complexity.

// GOOD: Concrete implementation
void drawMesh(Mesh* m, Shader* s) {
    glUseProgram(s->program);
    glBindVertexArray(m->vao);
    glDrawElements(GL_TRIANGLES, m->indexCount, GL_UNSIGNED_INT, 0);
}

// If you need a second backend later, write it. Don't predict the future.
```

### Excessive Layering

```c
// BAD: Seven layers of indirection
Application → GameEngine → SceneManager → EntityManager → 
  ComponentSystem → TransformComponent → Vector3

// GOOD: Direct access to what you need
game.entities[i].position.x += velocity * dt;
```

### Dependency Injection Everywhere

```c
// BAD: Inject everything
class Physics {
    IAllocator* allocator;
    ILogger* logger;
    IEventBus* events;
    IProfiler* profiler;
    
    Physics(IAllocator* a, ILogger* l, IEventBus* e, IProfiler* p)
        : allocator(a), logger(l), events(e), profiler(p) {}
};

// GOOD: Globals for engine services (controversial but pragmatic)
extern Allocator* g_allocator;
extern Logger* g_logger;

class Physics {
    // Just do the physics work
    void update(float dt);
};

// Globals make code simpler when there's genuinely one instance
// Don't cargo-cult "no globals" rule
```

## Testing Philosophy

### Automated Testing

```c
// Unit tests for algorithms
void testFastInvSqrt(void) {
    float x = 16.0f;
    float result = fastInvSqrt(x);
    float expected = 1.0f / sqrtf(x);
    
    ASSERT(fabsf(result - expected) < 0.001f);
}

// Integration tests with known data
void testPhysicsFrame(void) {
    Entity e = {0};
    e.position = (Vector3){0, 10, 0};
    e.velocity = (Vector3){0, 0, 0};
    
    updatePhysics(&e, 1.0f);  // 1 second
    
    // Should have fallen: y = y0 + v0*t + 0.5*a*t^2
    float expected = 10.0f + 0.5f * (-9.8f) * 1.0f;
    ASSERT(fabsf(e.position.y - expected) < 0.01f);
}
```

### Visual Testing

For graphics and game code, the best test is often visual:

```c
#ifdef DEBUG_RENDER
void drawDebugPhysics(void) {
    // Draw collision bounds
    for (int i = 0; i < entityCount; i++) {
        drawCircle(entities[i].position, entities[i].radius, COLOR_GREEN);
    }
    
    // Draw velocity vectors
    for (int i = 0; i < entityCount; i++) {
        drawLine(entities[i].position, 
                entities[i].position + entities[i].velocity,
                COLOR_RED);
    }
}
#endif
```

## Learning and Iteration

### Carmack's Learning Approach

1. **Read the source**: Don't just use libraries, read them. Understand how they work.

2. **Implement from scratch**: The best way to understand is to build it yourself once.

3. **Measure and compare**: Implement multiple approaches, measure them, understand why one wins.

4. **Keep notes**: Document insights. Programming knowledge compounds.

```c
// Example: Learning SIMD by implementing vector math

// Scalar version
Vector3 add_scalar(Vector3 a, Vector3 b) {
    return (Vector3){a.x + b.x, a.y + b.y, a.z + b.z};
}

// SSE version
__m128 add_sse(__m128 a, __m128 b) {
    return _mm_add_ps(a, b);
}

// Benchmark both:
// add_scalar: 1.2ns per call
// add_sse:    0.3ns per call
// Insight: 4x speedup, worth the complexity in hot paths
```

### Code Review Checklist

When reviewing code (or your own work):

- [ ] Is this the simplest solution that could work?
- [ ] Can a junior programmer understand this in 5 minutes?
- [ ] Are there any allocations in inner loops?
- [ ] Is the hot path branch-free and cache-friendly?
- [ ] Could this be data instead of code?
- [ ] Are assumptions documented and asserted?
- [ ] Does it compile with -Wall -Werror and zero warnings?
- [ ] Can I delete any of this code?

## Practical Examples

### Game Loop Structure

```c
int main(void) {
    initWindow();
    initRenderer();
    initGame();
    
    uint64_t lastTime = readCPUTimer();
    
    while (!shouldQuit()) {
        uint64_t currentTime = readCPUTimer();
        float dt = (currentTime - lastTime) / (float)getTimerFrequency();
        lastTime = currentTime;
        
        // Fixed timestep for physics
        const float PHYSICS_DT = 1.0f / 60.0f;
        static float accumulator = 0.0f;
        accumulator += dt;
        
        while (accumulator >= PHYSICS_DT) {
            updatePhysics(PHYSICS_DT);
            accumulator -= PHYSICS_DT;
        }
        
        // Variable timestep for rendering
        updateGame(dt);
        renderFrame();
        
        // Explicit frame pacing
        uint64_t frameEnd = readCPUTimer();
        float frameTime = (frameEnd - currentTime) / (float)getTimerFrequency();
        if (frameTime < TARGET_FRAME_TIME) {
            sleepMilliseconds((TARGET_FRAME_TIME - frameTime) * 1000.0f);
        }
    }
    
    shutdownGame();
    shutdownRenderer();
    shutdownWindow();
    return 0;
}
```

### Memory Arena Implementation

```c
typedef struct {
    uint8_t* base;
    size_t size;
    size_t used;
} Arena;

Arena createArena(size_t size) {
    Arena a;
    a.base = malloc(size);
    a.size = size;
    a.used = 0;
    return a;
}

void* arenaPush(Arena* a, size_t size) {
    ASSERT(a->used + size <= a->size);
    void* result = a->base + a->used;
    a->used += size;
    return result;
}

void arenaReset(Arena* a) {
    a->used = 0;
}

void arenaDestroy(Arena* a) {
    free(a->base);
    a->base = NULL;
    a->size = 0;
    a->used = 0;
}

// Usage pattern
Arena frame_arena = createArena(MEGABYTES(64));
Arena level_arena = createArena(MEGABYTES(256));

void processFrame(void) {
    // Temporary allocations for this frame
    TempData* data = arenaPush(&frame_arena, sizeof(TempData));
    
    // Do work
    
    // End of frame: reset entire arena instantly
    arenaReset(&frame_arena);
}
```

### Fast Entity Component System

```c
#define MAX_ENTITIES 10000

typedef struct {
    // Parallel arrays for cache coherency
    uint32_t    entity[MAX_ENTITIES];
    Vector3     position[MAX_ENTITIES];
    Vector3     velocity[MAX_ENTITIES];
    float       health[MAX_ENTITIES];
    uint8_t     flags[MAX_ENTITIES];
    int         count;
} EntityManager;

void updatePhysicsComponents(EntityManager* em, float dt) {
    // Process in batches for cache efficiency
    for (int i = 0; i < em->count; i++) {
        if (em->flags[i] & HAS_PHYSICS) {
            em->position[i] = vec3Add(em->position[i], 
                                      vec3Scale(em->velocity[i], dt));
        }
    }
}

// Deletion without preserving order (fast)
void removeEntity(EntityManager* em, int index) {
    ASSERT(index >= 0 && index < em->count);
    
    // Swap with last element
    int last = em->count - 1;
    em->entity[index]   = em->entity[last];
    em->position[index] = em->position[last];
    em->velocity[index] = em->velocity[last];
    em->health[index]   = em->health[last];
    em->flags[index]    = em->flags[last];
    
    em->count--;
}
```

## Advanced Topics

### Lock-Free Programming

For multithreaded systems:

```c
// Single-producer, single-consumer queue (lock-free)
typedef struct {
    void* items[4096];  // Power of 2 for fast modulo
    atomic_int head;
    atomic_int tail;
} SPSCQueue;

bool queuePush(SPSCQueue* q, void* item) {
    int tail = atomic_load(&q->tail);
    int nextTail = (tail + 1) & 4095;
    
    if (nextTail == atomic_load(&q->head)) {
        return false;  // Queue full
    }
    
    q->items[tail] = item;
    atomic_store(&q->tail, nextTail);
    return true;
}

void* queuePop(SPSCQueue* q) {
    int head = atomic_load(&q->head);
    
    if (head == atomic_load(&q->tail)) {
        return NULL;  // Queue empty
    }
    
    void* item = q->items[head];
    atomic_store(&q->head, (head + 1) & 4095);
    return item;
}
```

### Custom Allocator Patterns

```c
// Pool allocator for fixed-size objects
typedef struct {
    void* freeList;
    void* memory;
    size_t objectSize;
    int capacity;
    int used;
} Pool;

Pool createPool(size_t objectSize, int capacity) {
    Pool p;
    p.objectSize = objectSize;
    p.capacity = capacity;
    p.used = 0;
    p.memory = malloc(objectSize * capacity);
    
    // Initialize free list
    p.freeList = p.memory;
    uint8_t* ptr = p.memory;
    for (int i = 0; i < capacity - 1; i++) {
        *(void**)ptr = ptr + objectSize;
        ptr += objectSize;
    }
    *(void**)ptr = NULL;
    
    return p;
}

void* poolAlloc(Pool* p) {
    if (p->freeList == NULL) return NULL;
    
    void* result = p->freeList;
    p->freeList = *(void**)result;
    p->used++;
    return result;
}

void poolFree(Pool* p, void* ptr) {
    *(void**)ptr = p->freeList;
    p->freeList = ptr;
    p->used--;
}
```

## Philosophy Applied to Claude Code

When using Claude Code with this methodology:

1. **Start Simple**: Don't architect for scale you don't have. Write the straightforward solution first.

2. **Profile First**: Before optimizing, measure. Ask Claude Code to add profiling instrumentation.

3. **Iterate Based on Data**: Show Claude Code profiler output. Let measurements guide optimization decisions.

4. **Prefer C/C++ for Performance**: For systems programming and performance-critical code, these languages give you control.

5. **Document Insights**: Have Claude Code add comments explaining WHY, not WHAT. Performance decisions should be documented.

6. **Test Thoroughly**: Ask for both unit tests and integration tests. Verification is critical.

7. **Review Generated Code**: Claude Code is a tool. Review its output with the same rigor you'd review your own code.

## Conclusion

John Carmack's programming methodology is fundamentally about:

- **Understanding over abstraction**: Know what the machine is actually doing
- **Simplicity over cleverness**: The best code is obvious code
- **Measurement over intuition**: Profile, don't guess
- **Performance where it matters**: Optimize hot paths ruthlessly, keep everything else clean
- **Pragmatism over dogma**: Use the right tool for the job, question conventional wisdom

This approach has enabled groundbreaking work in 3D graphics, game engines, VR, and aerospace. Applied to modern development with Claude Code, it provides a framework for writing fast, maintainable, and deeply understood systems.

Remember: "The problem with quick and dirty, is that the dirty remains long after the quick has been forgotten."

---

*"Focused, hard work is the real key to success. Keep your eyes on the goal, and just keep taking the next step towards completing it."* - John Carmack
