# Carmack Programming Methodology - Implementation Guide

## Quick Reference: The Carmack Checklist

Before writing any code, ask yourself:

```
□ Do I understand this problem at the hardware level?
□ Have I chosen the simplest possible solution?
□ Can I measure this before optimizing it?
□ Is this code readable by someone with less expertise than me?
□ Have I minimized dependencies and coupling?
□ Are my hot paths identified and cache-friendly?
□ Can I delete any of this code?
```

## Project Structure (Carmack Style)

### Directory Layout

```
project/
├── build.c              # Unity build file (includes all .c files)
├── src/
│   ├── platform/
│   │   ├── platform.h   # Platform abstraction interface
│   │   ├── win32.c      # Windows implementation
│   │   └── linux.c      # Linux implementation
│   ├── core/
│   │   ├── math.c       # Vector, matrix, quaternion math
│   │   ├── memory.c     # Arena allocators, pools
│   │   └── utility.c    # String manipulation, hash functions
│   ├── engine/
│   │   ├── renderer.c   # Graphics rendering
│   │   ├── physics.c    # Physics simulation
│   │   └── audio.c      # Audio system
│   └── game/
│       ├── game.c       # Game logic
│       ├── entities.c   # Entity management
│       └── ai.c         # AI behaviors
├── assets/              # Data files
└── tools/               # Build tools, asset processors
```

### Build System (Simple Make or Shell Script)

```makefile
# Makefile - Carmack style

CC = gcc
CFLAGS = -O3 -Wall -Werror -march=native -ffast-math
LDFLAGS = -lm -lGL -lSDL2

# Debug build
debug: CFLAGS = -O0 -g -Wall -Werror -DDEBUG
debug: game

# Release build with maximum optimization
release: CFLAGS = -O3 -Wall -Werror -march=native -ffast-math -DNDEBUG -flto
release: game

game: build.c src/**/*.c src/**/*.h
	$(CC) $(CFLAGS) build.c -o game $(LDFLAGS)

clean:
	rm -f game

.PHONY: debug release clean
```

Or a simple shell script:

```bash
#!/bin/bash
# build.sh - Ultra-simple build script

set -e  # Exit on error

CFLAGS="-O3 -Wall -Werror -march=native -ffast-math"
LIBS="-lm -lGL -lSDL2"

if [ "$1" == "debug" ]; then
    CFLAGS="-O0 -g -Wall -Werror -DDEBUG"
fi

echo "Compiling..."
gcc $CFLAGS build.c -o game $LIBS

echo "Build complete: ./game"
```

## Core Components Implementation

### 1. Platform Layer

```c
// platform.h - Minimal platform abstraction
#ifndef PLATFORM_H
#define PLATFORM_H

#include <stdint.h>
#include <stdbool.h>

// Time
uint64_t platformGetTicks(void);        // Microseconds since startup
void     platformSleep(uint32_t ms);

// File I/O
typedef struct {
    void* data;
    size_t size;
} FileData;

FileData platformReadFile(const char* path);
bool     platformWriteFile(const char* path, void* data, size_t size);
void     platformFreeFileData(FileData* fd);

// Window
typedef struct PlatformWindow PlatformWindow;

PlatformWindow* platformCreateWindow(const char* title, int width, int height);
void            platformDestroyWindow(PlatformWindow* window);
void            platformPollEvents(void);
bool            platformShouldClose(void);
void            platformSwapBuffers(PlatformWindow* window);

// Input (simple immediate-mode input)
bool platformKeyDown(int key);
bool platformKeyPressed(int key);  // Just pressed this frame
bool platformMouseButton(int button);
void platformGetMousePos(int* x, int* y);

#endif // PLATFORM_H
```

```c
// win32.c - Windows implementation
#ifdef _WIN32

#include "platform.h"
#include <windows.h>

static LARGE_INTEGER g_frequency;
static LARGE_INTEGER g_startTime;
static bool g_initialized = false;

static void initTimer(void) {
    if (!g_initialized) {
        QueryPerformanceFrequency(&g_frequency);
        QueryPerformanceCounter(&g_startTime);
        g_initialized = true;
    }
}

uint64_t platformGetTicks(void) {
    initTimer();
    LARGE_INTEGER now;
    QueryPerformanceCounter(&now);
    
    // Convert to microseconds
    uint64_t elapsed = now.QuadPart - g_startTime.QuadPart;
    return (elapsed * 1000000) / g_frequency.QuadPart;
}

void platformSleep(uint32_t ms) {
    Sleep(ms);
}

FileData platformReadFile(const char* path) {
    FileData result = {0};
    
    HANDLE file = CreateFileA(path, GENERIC_READ, FILE_SHARE_READ, 
                              NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE) {
        return result;
    }
    
    LARGE_INTEGER size;
    if (!GetFileSizeEx(file, &size)) {
        CloseHandle(file);
        return result;
    }
    
    result.data = malloc((size_t)size.QuadPart);
    result.size = (size_t)size.QuadPart;
    
    DWORD bytesRead;
    ReadFile(file, result.data, (DWORD)result.size, &bytesRead, NULL);
    
    CloseHandle(file);
    return result;
}

bool platformWriteFile(const char* path, void* data, size_t size) {
    HANDLE file = CreateFileA(path, GENERIC_WRITE, 0, NULL, 
                              CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE) {
        return false;
    }
    
    DWORD bytesWritten;
    bool success = WriteFile(file, data, (DWORD)size, &bytesWritten, NULL);
    
    CloseHandle(file);
    return success && (bytesWritten == size);
}

void platformFreeFileData(FileData* fd) {
    if (fd->data) {
        free(fd->data);
        fd->data = NULL;
        fd->size = 0;
    }
}

#endif // _WIN32
```

### 2. Math Library (SIMD-Optimized)

```c
// math.c - Core math library

#include <math.h>
#include <xmmintrin.h>  // SSE
#include <smmintrin.h>  // SSE4.1

// ===== Basic Types =====

typedef struct { float x, y; } Vec2;
typedef struct { float x, y, z; } Vec3;
typedef struct { float x, y, z, w; } Vec4;

typedef struct {
    float m[16];  // Column-major for OpenGL
} Mat4;

typedef struct { float x, y, z, w; } Quat;

// ===== Vector Operations (Scalar) =====

static inline Vec3 vec3(float x, float y, float z) {
    return (Vec3){x, y, z};
}

static inline Vec3 vec3Add(Vec3 a, Vec3 b) {
    return vec3(a.x + b.x, a.y + b.y, a.z + b.z);
}

static inline Vec3 vec3Sub(Vec3 a, Vec3 b) {
    return vec3(a.x - b.x, a.y - b.y, a.z - b.z);
}

static inline Vec3 vec3Scale(Vec3 v, float s) {
    return vec3(v.x * s, v.y * s, v.z * s);
}

static inline float vec3Dot(Vec3 a, Vec3 b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

static inline Vec3 vec3Cross(Vec3 a, Vec3 b) {
    return vec3(
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x
    );
}

static inline float vec3Length(Vec3 v) {
    return sqrtf(vec3Dot(v, v));
}

static inline Vec3 vec3Normalize(Vec3 v) {
    float len = vec3Length(v);
    return len > 0.0f ? vec3Scale(v, 1.0f / len) : vec3(0, 0, 0);
}

// ===== SIMD Vector Operations =====

// Process 4 Vec3s simultaneously using SSE
typedef struct {
    __m128 x, y, z;  // 4 x values, 4 y values, 4 z values
} Vec3x4;

static inline Vec3x4 vec3x4Load(Vec3* vectors) {
    Vec3x4 result;
    // Transpose from AoS to SoA
    result.x = _mm_set_ps(vectors[3].x, vectors[2].x, vectors[1].x, vectors[0].x);
    result.y = _mm_set_ps(vectors[3].y, vectors[2].y, vectors[1].y, vectors[0].y);
    result.z = _mm_set_ps(vectors[3].z, vectors[2].z, vectors[1].z, vectors[0].z);
    return result;
}

static inline void vec3x4Store(Vec3x4 v, Vec3* out) {
    float x[4], y[4], z[4];
    _mm_store_ps(x, v.x);
    _mm_store_ps(y, v.y);
    _mm_store_ps(z, v.z);
    
    for (int i = 0; i < 4; i++) {
        out[i] = vec3(x[i], y[i], z[i]);
    }
}

static inline Vec3x4 vec3x4Add(Vec3x4 a, Vec3x4 b) {
    Vec3x4 result;
    result.x = _mm_add_ps(a.x, b.x);
    result.y = _mm_add_ps(a.y, b.y);
    result.z = _mm_add_ps(a.z, b.z);
    return result;
}

static inline Vec3x4 vec3x4Scale(Vec3x4 v, __m128 s) {
    Vec3x4 result;
    result.x = _mm_mul_ps(v.x, s);
    result.y = _mm_mul_ps(v.y, s);
    result.z = _mm_mul_ps(v.z, s);
    return result;
}

// ===== Matrix Operations =====

Mat4 mat4Identity(void) {
    Mat4 m = {0};
    m.m[0] = m.m[5] = m.m[10] = m.m[15] = 1.0f;
    return m;
}

Mat4 mat4Perspective(float fovy, float aspect, float near, float far) {
    Mat4 m = {0};
    float f = 1.0f / tanf(fovy * 0.5f);
    
    m.m[0] = f / aspect;
    m.m[5] = f;
    m.m[10] = (far + near) / (near - far);
    m.m[11] = -1.0f;
    m.m[14] = (2.0f * far * near) / (near - far);
    
    return m;
}

Mat4 mat4LookAt(Vec3 eye, Vec3 center, Vec3 up) {
    Vec3 f = vec3Normalize(vec3Sub(center, eye));
    Vec3 s = vec3Normalize(vec3Cross(f, up));
    Vec3 u = vec3Cross(s, f);
    
    Mat4 m = {0};
    m.m[0] = s.x;
    m.m[4] = s.y;
    m.m[8] = s.z;
    m.m[1] = u.x;
    m.m[5] = u.y;
    m.m[9] = u.z;
    m.m[2] = -f.x;
    m.m[6] = -f.y;
    m.m[10] = -f.z;
    m.m[12] = -vec3Dot(s, eye);
    m.m[13] = -vec3Dot(u, eye);
    m.m[14] = vec3Dot(f, eye);
    m.m[15] = 1.0f;
    
    return m;
}

Mat4 mat4Multiply(Mat4 a, Mat4 b) {
    Mat4 result = {0};
    
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            result.m[i * 4 + j] = 
                a.m[i * 4 + 0] * b.m[0 * 4 + j] +
                a.m[i * 4 + 1] * b.m[1 * 4 + j] +
                a.m[i * 4 + 2] * b.m[2 * 4 + j] +
                a.m[i * 4 + 3] * b.m[3 * 4 + j];
        }
    }
    
    return result;
}

// ===== Fast Approximations =====

// Fast inverse square root (modernized from Quake III)
static inline float fastInvSqrt(float x) {
    // Use hardware instruction on modern CPUs
    __m128 temp = _mm_set_ss(x);
    temp = _mm_rsqrt_ss(temp);
    return _mm_cvtss_f32(temp);
}

// Fast sine approximation (good for game logic, not scientific)
static inline float fastSin(float x) {
    // Normalize to [-π, π]
    const float PI = 3.14159265359f;
    while (x > PI) x -= 2.0f * PI;
    while (x < -PI) x += 2.0f * PI;
    
    // 5th order polynomial approximation
    float x2 = x * x;
    return x * (1.0f - x2 * (0.16666f - x2 * 0.00833f));
}

static inline float fastCos(float x) {
    return fastSin(x + 3.14159265359f * 0.5f);
}
```

### 3. Memory Management

```c
// memory.c - Custom allocators

#include <stdlib.h>
#include <string.h>
#include <assert.h>

// ===== Arena Allocator =====

typedef struct {
    uint8_t* base;
    size_t size;
    size_t used;
    size_t commitPosition;  // For virtual memory
} Arena;

Arena arenaCreate(size_t size) {
    Arena arena;
    arena.base = malloc(size);
    arena.size = size;
    arena.used = 0;
    arena.commitPosition = 0;
    
    assert(arena.base != NULL);
    memset(arena.base, 0, size);
    
    return arena;
}

void* arenaPush(Arena* arena, size_t size) {
    assert(arena->used + size <= arena->size);
    
    void* result = arena->base + arena->used;
    arena->used += size;
    
    return result;
}

void* arenaPushZero(Arena* arena, size_t size) {
    void* result = arenaPush(arena, size);
    memset(result, 0, size);
    return result;
}

void arenaReset(Arena* arena) {
    arena->used = 0;
}

void arenaDestroy(Arena* arena) {
    free(arena->base);
    arena->base = NULL;
    arena->size = 0;
    arena->used = 0;
}

// Temporary arena marker for nested scoping
typedef struct {
    Arena* arena;
    size_t savedUsed;
} ArenaTemp;

ArenaTemp arenaTempBegin(Arena* arena) {
    ArenaTemp temp;
    temp.arena = arena;
    temp.savedUsed = arena->used;
    return temp;
}

void arenaTempEnd(ArenaTemp temp) {
    temp.arena->used = temp.savedUsed;
}

// ===== Pool Allocator =====

typedef struct PoolFreeNode {
    struct PoolFreeNode* next;
} PoolFreeNode;

typedef struct {
    void* memory;
    PoolFreeNode* freeList;
    size_t objectSize;
    size_t capacity;
    size_t used;
} Pool;

Pool poolCreate(size_t objectSize, size_t capacity) {
    Pool pool;
    pool.objectSize = objectSize >= sizeof(PoolFreeNode) ? 
                      objectSize : sizeof(PoolFreeNode);
    pool.capacity = capacity;
    pool.used = 0;
    pool.memory = malloc(pool.objectSize * capacity);
    
    assert(pool.memory != NULL);
    
    // Build free list
    pool.freeList = pool.memory;
    uint8_t* ptr = pool.memory;
    
    for (size_t i = 0; i < capacity - 1; i++) {
        PoolFreeNode* node = (PoolFreeNode*)ptr;
        node->next = (PoolFreeNode*)(ptr + pool.objectSize);
        ptr += pool.objectSize;
    }
    
    PoolFreeNode* lastNode = (PoolFreeNode*)ptr;
    lastNode->next = NULL;
    
    return pool;
}

void* poolAlloc(Pool* pool) {
    if (pool->freeList == NULL) {
        return NULL;  // Pool exhausted
    }
    
    void* result = pool->freeList;
    pool->freeList = pool->freeList->next;
    pool->used++;
    
    return result;
}

void poolFree(Pool* pool, void* ptr) {
    assert(ptr != NULL);
    
    PoolFreeNode* node = (PoolFreeNode*)ptr;
    node->next = pool->freeList;
    pool->freeList = node;
    pool->used--;
}

void poolReset(Pool* pool) {
    // Rebuild free list
    pool.freeList = pool.memory;
    uint8_t* ptr = pool.memory;
    
    for (size_t i = 0; i < pool.capacity - 1; i++) {
        PoolFreeNode* node = (PoolFreeNode*)ptr;
        node->next = (PoolFreeNode*)(ptr + pool.objectSize);
        ptr += pool.objectSize;
    }
    
    PoolFreeNode* lastNode = (PoolFreeNode*)ptr;
    lastNode->next = NULL;
    pool.used = 0;
}

void poolDestroy(Pool* pool) {
    free(pool.memory);
    pool->memory = NULL;
    pool->freeList = NULL;
    pool->capacity = 0;
    pool->used = 0;
}

// ===== Stack Allocator (for temporary frame data) =====

typedef struct {
    Arena arena;
    size_t* markers;
    int markerCount;
    int markerCapacity;
} Stack;

Stack stackCreate(size_t size) {
    Stack stack;
    stack.arena = arenaCreate(size);
    stack.markerCapacity = 128;
    stack.markers = malloc(sizeof(size_t) * stack.markerCapacity);
    stack.markerCount = 0;
    
    return stack;
}

void stackPush(Stack* stack) {
    if (stack->markerCount >= stack->markerCapacity) {
        stack->markerCapacity *= 2;
        stack->markers = realloc(stack->markers, 
                                sizeof(size_t) * stack->markerCapacity);
    }
    
    stack->markers[stack->markerCount++] = stack->arena.used;
}

void stackPop(Stack* stack) {
    assert(stack->markerCount > 0);
    stack->arena.used = stack->markers[--stack->markerCount];
}

void* stackAlloc(Stack* stack, size_t size) {
    return arenaPush(&stack->arena, size);
}

void stackDestroy(Stack* stack) {
    arenaDestroy(&stack->arena);
    free(stack->markers);
}
```

### 4. Entity Component System

```c
// entities.c - Data-oriented entity system

#define MAX_ENTITIES 10000

typedef uint32_t EntityID;
typedef uint32_t EntityFlags;

enum {
    ENTITY_ACTIVE      = 1 << 0,
    ENTITY_HAS_PHYSICS = 1 << 1,
    ENTITY_HAS_RENDER  = 1 << 2,
    ENTITY_HAS_AI      = 1 << 3,
    ENTITY_HAS_HEALTH  = 1 << 4,
};

typedef struct {
    // Parallel arrays for cache efficiency
    EntityID    id[MAX_ENTITIES];
    EntityFlags flags[MAX_ENTITIES];
    
    // Transform
    Vec3        position[MAX_ENTITIES];
    Quat        rotation[MAX_ENTITIES];
    Vec3        scale[MAX_ENTITIES];
    
    // Physics
    Vec3        velocity[MAX_ENTITIES];
    Vec3        acceleration[MAX_ENTITIES];
    float       mass[MAX_ENTITIES];
    float       radius[MAX_ENTITIES];
    
    // Rendering
    uint32_t    modelID[MAX_ENTITIES];
    uint32_t    textureID[MAX_ENTITIES];
    Vec4        color[MAX_ENTITIES];
    
    // Gameplay
    float       health[MAX_ENTITIES];
    float       maxHealth[MAX_ENTITIES];
    int         aiState[MAX_ENTITIES];
    
    int count;
    int capacity;
} EntityManager;

EntityManager g_entities;  // Global (Carmack-approved for singletons)

void entitiesInit(void) {
    memset(&g_entities, 0, sizeof(g_entities));
    g_entities.capacity = MAX_ENTITIES;
}

EntityID entityCreate(void) {
    assert(g_entities.count < MAX_ENTITIES);
    
    int index = g_entities.count++;
    static EntityID nextID = 1;
    
    g_entities.id[index] = nextID++;
    g_entities.flags[index] = ENTITY_ACTIVE;
    
    // Initialize with defaults
    g_entities.position[index] = vec3(0, 0, 0);
    g_entities.rotation[index] = (Quat){0, 0, 0, 1};
    g_entities.scale[index] = vec3(1, 1, 1);
    g_entities.velocity[index] = vec3(0, 0, 0);
    g_entities.mass[index] = 1.0f;
    g_entities.radius[index] = 0.5f;
    g_entities.health[index] = 100.0f;
    g_entities.maxHealth[index] = 100.0f;
    g_entities.color[index] = (Vec4){1, 1, 1, 1};
    
    return g_entities.id[index];
}

void entityDestroy(int index) {
    assert(index >= 0 && index < g_entities.count);
    
    // Swap with last element (unordered removal)
    int last = g_entities.count - 1;
    if (index != last) {
        g_entities.id[index] = g_entities.id[last];
        g_entities.flags[index] = g_entities.flags[last];
        g_entities.position[index] = g_entities.position[last];
        g_entities.rotation[index] = g_entities.rotation[last];
        g_entities.scale[index] = g_entities.scale[last];
        g_entities.velocity[index] = g_entities.velocity[last];
        g_entities.mass[index] = g_entities.mass[last];
        g_entities.radius[index] = g_entities.radius[last];
        g_entities.modelID[index] = g_entities.modelID[last];
        g_entities.health[index] = g_entities.health[last];
        // ... copy all components
    }
    
    g_entities.count--;
}

int entityFindIndex(EntityID id) {
    for (int i = 0; i < g_entities.count; i++) {
        if (g_entities.id[i] == id) {
            return i;
        }
    }
    return -1;
}

// ===== Systems =====

void physicsSystem(float dt) {
    const Vec3 gravity = vec3(0, -9.8f, 0);
    
    for (int i = 0; i < g_entities.count; i++) {
        if (!(g_entities.flags[i] & ENTITY_HAS_PHYSICS)) {
            continue;
        }
        
        // Apply gravity
        g_entities.acceleration[i] = vec3Add(
            g_entities.acceleration[i],
            vec3Scale(gravity, 1.0f / g_entities.mass[i])
        );
        
        // Integrate velocity
        g_entities.velocity[i] = vec3Add(
            g_entities.velocity[i],
            vec3Scale(g_entities.acceleration[i], dt)
        );
        
        // Integrate position
        g_entities.position[i] = vec3Add(
            g_entities.position[i],
            vec3Scale(g_entities.velocity[i], dt)
        );
        
        // Reset acceleration
        g_entities.acceleration[i] = vec3(0, 0, 0);
    }
}

void collisionSystem(void) {
    // Broad phase: Simple spatial grid
    // (In real code, implement spatial hash or BVH)
    
    for (int i = 0; i < g_entities.count; i++) {
        if (!(g_entities.flags[i] & ENTITY_HAS_PHYSICS)) continue;
        
        for (int j = i + 1; j < g_entities.count; j++) {
            if (!(g_entities.flags[j] & ENTITY_HAS_PHYSICS)) continue;
            
            // Sphere-sphere collision
            Vec3 delta = vec3Sub(g_entities.position[i], 
                                g_entities.position[j]);
            float distSq = vec3Dot(delta, delta);
            float radiusSum = g_entities.radius[i] + g_entities.radius[j];
            
            if (distSq < radiusSum * radiusSum) {
                // Collision! Resolve with simple separation
                float dist = sqrtf(distSq);
                if (dist > 0.001f) {
                    Vec3 normal = vec3Scale(delta, 1.0f / dist);
                    float overlap = radiusSum - dist;
                    
                    g_entities.position[i] = vec3Add(
                        g_entities.position[i],
                        vec3Scale(normal, overlap * 0.5f)
                    );
                    g_entities.position[j] = vec3Add(
                        g_entities.position[j],
                        vec3Scale(normal, -overlap * 0.5f)
                    );
                }
            }
        }
    }
}

void healthSystem(float dt) {
    for (int i = g_entities.count - 1; i >= 0; i--) {
        if (!(g_entities.flags[i] & ENTITY_HAS_HEALTH)) continue;
        
        if (g_entities.health[i] <= 0.0f) {
            entityDestroy(i);
        }
    }
}
```

## Continued in next artifact for rendering, profiling, and complete game loop...

