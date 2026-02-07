# Carmack Programming - Rendering, Profiling & Complete Examples

## 5. Rendering System (OpenGL - Carmack Style)

```c
// renderer.c - Modern OpenGL renderer with Carmack principles

#include <GL/gl.h>
#include <GL/glext.h>

// ===== Render State Management =====

// Minimize state changes by batching draw calls
typedef struct {
    uint32_t shaderID;
    uint32_t textureID;
    uint32_t vao;
    uint32_t indexCount;
    Mat4 transform;
} DrawCommand;

typedef struct {
    DrawCommand* commands;
    int count;
    int capacity;
    
    // Current bound state (to avoid redundant state changes)
    uint32_t boundShader;
    uint32_t boundTexture;
    uint32_t boundVAO;
} RenderQueue;

static RenderQueue g_renderQueue;

void renderQueueInit(int capacity) {
    g_renderQueue.commands = malloc(sizeof(DrawCommand) * capacity);
    g_renderQueue.capacity = capacity;
    g_renderQueue.count = 0;
    g_renderQueue.boundShader = 0;
    g_renderQueue.boundTexture = 0;
    g_renderQueue.boundVAO = 0;
}

void renderQueueSubmit(DrawCommand cmd) {
    assert(g_renderQueue.count < g_renderQueue.capacity);
    g_renderQueue.commands[g_renderQueue.count++] = cmd;
}

// Sort key: Pack state into 64-bit key for radix sort
static uint64_t makeRenderKey(DrawCommand* cmd) {
    // Priority: shader (most expensive) > texture > VAO
    return ((uint64_t)cmd->shaderID << 40) | 
           ((uint64_t)cmd->textureID << 20) | 
           (uint64_t)cmd->vao;
}

// Radix sort for render commands (stable, O(n), cache-friendly)
static void radixSortCommands(DrawCommand* commands, int count) {
    const int BITS = 8;
    const int BUCKETS = 256;
    
    DrawCommand* temp = malloc(sizeof(DrawCommand) * count);
    uint64_t* keys = malloc(sizeof(uint64_t) * count);
    
    // Generate keys
    for (int i = 0; i < count; i++) {
        keys[i] = makeRenderKey(&commands[i]);
    }
    
    // Sort by each byte (8 passes for 64-bit keys)
    for (int pass = 0; pass < 8; pass++) {
        int hist[BUCKETS] = {0};
        int shift = pass * BITS;
        
        // Count
        for (int i = 0; i < count; i++) {
            int bucket = (keys[i] >> shift) & 0xFF;
            hist[bucket]++;
        }
        
        // Prefix sum
        int sum = 0;
        for (int i = 0; i < BUCKETS; i++) {
            int tmp = hist[i];
            hist[i] = sum;
            sum += tmp;
        }
        
        // Distribute
        for (int i = 0; i < count; i++) {
            int bucket = (keys[i] >> shift) & 0xFF;
            temp[hist[bucket]] = commands[i];
            keys[hist[bucket]] = keys[i];
            hist[bucket]++;
        }
        
        // Swap buffers
        DrawCommand* tmpCmd = commands;
        commands = temp;
        temp = tmpCmd;
    }
    
    free(temp);
    free(keys);
}

void renderQueueFlush(void) {
    if (g_renderQueue.count == 0) return;
    
    // Sort by state to minimize changes
    radixSortCommands(g_renderQueue.commands, g_renderQueue.count);
    
    // Execute sorted commands
    for (int i = 0; i < g_renderQueue.count; i++) {
        DrawCommand* cmd = &g_renderQueue.commands[i];
        
        // Only change state when necessary
        if (cmd->shaderID != g_renderQueue.boundShader) {
            glUseProgram(cmd->shaderID);
            g_renderQueue.boundShader = cmd->shaderID;
        }
        
        if (cmd->textureID != g_renderQueue.boundTexture) {
            glBindTexture(GL_TEXTURE_2D, cmd->textureID);
            g_renderQueue.boundTexture = cmd->textureID;
        }
        
        if (cmd->vao != g_renderQueue.boundVAO) {
            glBindVertexArray(cmd->vao);
            g_renderQueue.boundVAO = cmd->vao;
        }
        
        // Upload transform uniform
        GLint loc = glGetUniformLocation(cmd->shaderID, "u_transform");
        glUniformMatrix4fv(loc, 1, GL_FALSE, cmd->transform.m);
        
        // Draw
        glDrawElements(GL_TRIANGLES, cmd->indexCount, GL_UNSIGNED_INT, 0);
    }
    
    // Reset queue
    g_renderQueue.count = 0;
}

// ===== Mesh Management =====

typedef struct {
    uint32_t vao;
    uint32_t vbo;
    uint32_t ibo;
    int indexCount;
} Mesh;

Mesh createMesh(float* vertices, int vertexCount, 
                uint32_t* indices, int indexCount) {
    Mesh mesh;
    mesh.indexCount = indexCount;
    
    glGenVertexArrays(1, &mesh.vao);
    glGenBuffers(1, &mesh.vbo);
    glGenBuffers(1, &mesh.ibo);
    
    glBindVertexArray(mesh.vao);
    
    // Upload vertices
    glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo);
    glBufferData(GL_ARRAY_BUFFER, 
                 vertexCount * sizeof(float), 
                 vertices, 
                 GL_STATIC_DRAW);
    
    // Position attribute (3 floats)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 
                         8 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    
    // Normal attribute (3 floats)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 
                         8 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);
    
    // Texcoord attribute (2 floats)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 
                         8 * sizeof(float), (void*)(6 * sizeof(float)));
    glEnableVertexAttribArray(2);
    
    // Upload indices
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ibo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 
                 indexCount * sizeof(uint32_t), 
                 indices, 
                 GL_STATIC_DRAW);
    
    glBindVertexArray(0);
    
    return mesh;
}

// ===== Shader Management =====

uint32_t compileShader(const char* source, GLenum type) {
    uint32_t shader = glCreateShader(type);
    glShaderSource(shader, 1, &source, NULL);
    glCompileShader(shader);
    
    // Check for errors
    int success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        char log[512];
        glGetShaderInfoLog(shader, 512, NULL, log);
        fprintf(stderr, "Shader compilation failed: %s\n", log);
        return 0;
    }
    
    return shader;
}

uint32_t createShaderProgram(const char* vertSource, const char* fragSource) {
    uint32_t vert = compileShader(vertSource, GL_VERTEX_SHADER);
    uint32_t frag = compileShader(fragSource, GL_FRAGMENT_SHADER);
    
    if (!vert || !frag) return 0;
    
    uint32_t program = glCreateProgram();
    glAttachShader(program, vert);
    glAttachShader(program, frag);
    glLinkProgram(program);
    
    // Check for linking errors
    int success;
    glGetProgramiv(program, GL_LINK_STATUS, &success);
    if (!success) {
        char log[512];
        glGetProgramInfoLog(program, 512, NULL, log);
        fprintf(stderr, "Shader linking failed: %s\n", log);
        return 0;
    }
    
    glDeleteShader(vert);
    glDeleteShader(frag);
    
    return program;
}

// ===== Simple Shaders =====

const char* basicVertexShader = 
    "#version 330 core\n"
    "layout (location = 0) in vec3 a_position;\n"
    "layout (location = 1) in vec3 a_normal;\n"
    "layout (location = 2) in vec2 a_texcoord;\n"
    "uniform mat4 u_transform;\n"
    "uniform mat4 u_view;\n"
    "uniform mat4 u_projection;\n"
    "out vec3 v_normal;\n"
    "out vec2 v_texcoord;\n"
    "void main() {\n"
    "    gl_Position = u_projection * u_view * u_transform * vec4(a_position, 1.0);\n"
    "    v_normal = a_normal;\n"
    "    v_texcoord = a_texcoord;\n"
    "}\n";

const char* basicFragmentShader = 
    "#version 330 core\n"
    "in vec3 v_normal;\n"
    "in vec2 v_texcoord;\n"
    "uniform sampler2D u_texture;\n"
    "uniform vec4 u_color;\n"
    "out vec4 fragColor;\n"
    "void main() {\n"
    "    vec3 light = normalize(vec3(1, 1, 1));\n"
    "    float diff = max(dot(v_normal, light), 0.0);\n"
    "    vec4 texColor = texture(u_texture, v_texcoord);\n"
    "    fragColor = texColor * u_color * (0.3 + 0.7 * diff);\n"
    "}\n";
```

## 6. Profiling System (Built-in Performance Measurement)

```c
// profiler.c - Lightweight profiling system

#include <stdio.h>
#include <string.h>

#define MAX_PROFILE_ZONES 256

typedef struct {
    const char* name;
    uint64_t startTime;
    uint64_t totalTime;
    uint32_t hitCount;
    uint32_t parentIndex;
} ProfileZone;

typedef struct {
    ProfileZone zones[MAX_PROFILE_ZONES];
    int zoneCount;
    int currentZone;
    bool enabled;
} Profiler;

static Profiler g_profiler = {0};

void profilerEnable(bool enable) {
    g_profiler.enabled = enable;
}

void profilerReset(void) {
    for (int i = 0; i < g_profiler.zoneCount; i++) {
        g_profiler.zones[i].totalTime = 0;
        g_profiler.zones[i].hitCount = 0;
    }
}

int profilerBeginZone(const char* name) {
    if (!g_profiler.enabled) return -1;
    
    // Find or create zone
    int index = -1;
    for (int i = 0; i < g_profiler.zoneCount; i++) {
        if (strcmp(g_profiler.zones[i].name, name) == 0) {
            index = i;
            break;
        }
    }
    
    if (index == -1) {
        assert(g_profiler.zoneCount < MAX_PROFILE_ZONES);
        index = g_profiler.zoneCount++;
        g_profiler.zones[index].name = name;
        g_profiler.zones[index].totalTime = 0;
        g_profiler.zones[index].hitCount = 0;
    }
    
    g_profiler.zones[index].startTime = platformGetTicks();
    g_profiler.zones[index].parentIndex = g_profiler.currentZone;
    g_profiler.currentZone = index;
    
    return index;
}

void profilerEndZone(int index) {
    if (!g_profiler.enabled || index == -1) return;
    
    uint64_t endTime = platformGetTicks();
    uint64_t elapsed = endTime - g_profiler.zones[index].startTime;
    
    g_profiler.zones[index].totalTime += elapsed;
    g_profiler.zones[index].hitCount++;
    g_profiler.currentZone = g_profiler.zones[index].parentIndex;
}

void profilerPrint(void) {
    if (!g_profiler.enabled) return;
    
    printf("\n=== Profile Results ===\n");
    printf("%-30s %10s %10s %10s\n", "Zone", "Total (ms)", "Calls", "Avg (us)");
    printf("------------------------------------------------------------\n");
    
    for (int i = 0; i < g_profiler.zoneCount; i++) {
        ProfileZone* zone = &g_profiler.zones[i];
        if (zone->hitCount == 0) continue;
        
        double totalMs = zone->totalTime / 1000.0;
        double avgUs = (zone->totalTime / (double)zone->hitCount) / 1.0;
        
        printf("%-30s %10.2f %10u %10.2f\n", 
               zone->name, totalMs, zone->hitCount, avgUs);
    }
    
    printf("\n");
}

// Macro for convenient scoped profiling
#define PROFILE_SCOPE(name) \
    int __profile_##__LINE__ = profilerBeginZone(name); \
    defer(profilerEndZone(__profile_##__LINE__))

// defer macro (requires cleanup attribute - GCC/Clang)
#define defer(code) \
    __attribute__((cleanup(defer_##__LINE__))) int __defer_##__LINE__ = 0; \
    static void defer_##__LINE__(int* _) { code; }
```

## 7. Complete Game Loop

```c
// game.c - Main game loop integrating all systems

#include "platform.h"
#include "renderer.h"
#include "entities.h"
#include "profiler.h"

typedef struct {
    PlatformWindow* window;
    bool running;
    
    // Arenas for different lifetimes
    Arena permanentArena;  // Never freed
    Arena levelArena;      // Freed on level change
    Arena frameArena;      // Reset every frame
    
    // Camera
    Vec3 cameraPos;
    Vec3 cameraTarget;
    Mat4 viewMatrix;
    Mat4 projMatrix;
    
    // Resources
    uint32_t shaderProgram;
    Mesh cubeMesh;
    
    // Timing
    uint64_t lastFrameTime;
    float deltaTime;
    float accumulator;  // For fixed timestep
} GameState;

static GameState g_game;

// ===== Initialization =====

void gameInit(void) {
    // Create window
    g_game.window = platformCreateWindow("Carmack-Style Game", 1280, 720);
    g_game.running = true;
    
    // Initialize memory arenas
    g_game.permanentArena = arenaCreate(MEGABYTES(64));
    g_game.levelArena = arenaCreate(MEGABYTES(256));
    g_game.frameArena = arenaCreate(MEGABYTES(16));
    
    // Initialize systems
    entitiesInit();
    renderQueueInit(1000);
    profilerEnable(true);
    
    // Setup camera
    g_game.cameraPos = vec3(0, 5, 10);
    g_game.cameraTarget = vec3(0, 0, 0);
    g_game.viewMatrix = mat4LookAt(g_game.cameraPos, 
                                    g_game.cameraTarget, 
                                    vec3(0, 1, 0));
    g_game.projMatrix = mat4Perspective(1.047f, 1280.0f/720.0f, 0.1f, 1000.0f);
    
    // Create resources
    g_game.shaderProgram = createShaderProgram(basicVertexShader, 
                                               basicFragmentShader);
    
    // Create simple cube mesh
    float cubeVertices[] = {
        // positions        normals         texcoords
        -1,-1,-1,  0, 0,-1,  0, 0,
         1,-1,-1,  0, 0,-1,  1, 0,
         1, 1,-1,  0, 0,-1,  1, 1,
        -1, 1,-1,  0, 0,-1,  0, 1,
        // ... (other faces)
    };
    
    uint32_t cubeIndices[] = {
        0, 1, 2,  2, 3, 0,  // Front face
        // ... (other faces)
    };
    
    g_game.cubeMesh = createMesh(cubeVertices, 
                                sizeof(cubeVertices)/sizeof(float),
                                cubeIndices, 
                                sizeof(cubeIndices)/sizeof(uint32_t));
    
    // Spawn some test entities
    for (int i = 0; i < 100; i++) {
        EntityID id = entityCreate();
        int index = entityFindIndex(id);
        
        g_entities.position[index] = vec3(
            (rand() % 20) - 10.0f,
            (rand() % 10) + 2.0f,
            (rand() % 20) - 10.0f
        );
        g_entities.velocity[index] = vec3(
            ((rand() % 200) - 100) / 100.0f,
            0,
            ((rand() % 200) - 100) / 100.0f
        );
        g_entities.flags[index] |= ENTITY_HAS_PHYSICS | ENTITY_HAS_RENDER;
        g_entities.modelID[index] = 0;  // Cube
    }
    
    g_game.lastFrameTime = platformGetTicks();
    g_game.accumulator = 0.0f;
}

// ===== Update =====

void gameUpdate(float dt) {
    PROFILE_SCOPE("Game Update");
    
    // Camera rotation
    static float angle = 0.0f;
    angle += dt * 0.5f;
    
    g_game.cameraPos = vec3(
        sinf(angle) * 15.0f,
        5.0f,
        cosf(angle) * 15.0f
    );
    
    g_game.viewMatrix = mat4LookAt(g_game.cameraPos, 
                                    g_game.cameraTarget, 
                                    vec3(0, 1, 0));
    
    // Input handling
    if (platformKeyPressed(KEY_ESCAPE)) {
        g_game.running = false;
    }
}

void gameFixedUpdate(float dt) {
    PROFILE_SCOPE("Fixed Update");
    
    // Physics runs at fixed timestep
    physicsSystem(dt);
    collisionSystem();
    healthSystem(dt);
}

// ===== Rendering =====

void gameRender(void) {
    PROFILE_SCOPE("Render");
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glClearColor(0.1f, 0.1f, 0.15f, 1.0f);
    
    // Set view/projection uniforms (shared across all draws)
    glUseProgram(g_game.shaderProgram);
    GLint viewLoc = glGetUniformLocation(g_game.shaderProgram, "u_view");
    GLint projLoc = glGetUniformLocation(g_game.shaderProgram, "u_projection");
    glUniformMatrix4fv(viewLoc, 1, GL_FALSE, g_game.viewMatrix.m);
    glUniformMatrix4fv(projLoc, 1, GL_FALSE, g_game.projMatrix.m);
    
    // Submit draw commands for all entities
    {
        PROFILE_SCOPE("Submit Commands");
        
        for (int i = 0; i < g_entities.count; i++) {
            if (!(g_entities.flags[i] & ENTITY_HAS_RENDER)) continue;
            
            // Build transform matrix
            Mat4 transform = mat4Identity();
            // TODO: Apply position, rotation, scale
            
            DrawCommand cmd;
            cmd.shaderID = g_game.shaderProgram;
            cmd.textureID = 0;  // White texture
            cmd.vao = g_game.cubeMesh.vao;
            cmd.indexCount = g_game.cubeMesh.indexCount;
            cmd.transform = transform;
            
            renderQueueSubmit(cmd);
        }
    }
    
    // Flush render queue (sorted submission)
    {
        PROFILE_SCOPE("Flush Queue");
        renderQueueFlush();
    }
    
    platformSwapBuffers(g_game.window);
}

// ===== Main Loop =====

int main(void) {
    gameInit();
    
    const float FIXED_DT = 1.0f / 60.0f;  // 60 FPS physics
    const float TARGET_FRAME_TIME = 1.0f / 60.0f;  // Target 60 FPS rendering
    
    uint64_t frameCount = 0;
    uint64_t profilePrintTimer = 0;
    
    while (g_game.running) {
        PROFILE_SCOPE("Frame");
        
        // Calculate delta time
        uint64_t currentTime = platformGetTicks();
        uint64_t elapsed = currentTime - g_game.lastFrameTime;
        g_game.deltaTime = elapsed / 1000000.0f;  // Convert to seconds
        g_game.lastFrameTime = currentTime;
        
        // Cap delta time to prevent spiral of death
        if (g_game.deltaTime > 0.25f) {
            g_game.deltaTime = 0.25f;
        }
        
        // Process input
        platformPollEvents();
        if (platformShouldClose()) {
            g_game.running = false;
        }
        
        // Fixed timestep update (physics)
        g_game.accumulator += g_game.deltaTime;
        while (g_game.accumulator >= FIXED_DT) {
            gameFixedUpdate(FIXED_DT);
            g_game.accumulator -= FIXED_DT;
        }
        
        // Variable timestep update (gameplay)
        gameUpdate(g_game.deltaTime);
        
        // Render
        gameRender();
        
        // Reset frame arena
        arenaReset(&g_game.frameArena);
        
        // Frame pacing
        uint64_t frameEnd = platformGetTicks();
        uint64_t frameTime = frameEnd - currentTime;
        float frameSeconds = frameTime / 1000000.0f;
        
        if (frameSeconds < TARGET_FRAME_TIME) {
            uint32_t sleepMs = (uint32_t)((TARGET_FRAME_TIME - frameSeconds) * 1000.0f);
            platformSleep(sleepMs);
        }
        
        frameCount++;
        
        // Print profile every second
        if (currentTime - profilePrintTimer > 1000000) {
            profilerPrint();
            profilerReset();
            profilePrintTimer = currentTime;
            
            printf("FPS: %.1f\n", 1.0f / g_game.deltaTime);
        }
    }
    
    // Cleanup
    arenaDestroy(&g_game.frameArena);
    arenaDestroy(&g_game.levelArena);
    arenaDestroy(&g_game.permanentArena);
    platformDestroyWindow(g_game.window);
    
    return 0;
}
```

## 8. Optimization Techniques

### Cache Optimization Example

```c
// BAD: Random memory access pattern
void updateParticles_Bad(Particle* particles, int count) {
    for (int i = 0; i < count; i++) {
        // Each particle is scattered in memory
        particles[i].position.x += particles[i].velocity.x * dt;
        particles[i].position.y += particles[i].velocity.y * dt;
        particles[i].position.z += particles[i].velocity.z * dt;
    }
}

// GOOD: Linear memory access, SIMD-friendly
void updateParticles_Good(ParticleSystem* system, int count) {
    // Process X coordinates
    for (int i = 0; i < count; i += 4) {
        __m128 px = _mm_load_ps(&system->px[i]);
        __m128 vx = _mm_load_ps(&system->vx[i]);
        __m128 dt_vec = _mm_set1_ps(dt);
        px = _mm_add_ps(px, _mm_mul_ps(vx, dt_vec));
        _mm_store_ps(&system->px[i], px);
    }
    
    // Process Y coordinates
    for (int i = 0; i < count; i += 4) {
        __m128 py = _mm_load_ps(&system->py[i]);
        __m128 vy = _mm_load_ps(&system->vy[i]);
        __m128 dt_vec = _mm_set1_ps(dt);
        py = _mm_add_ps(py, _mm_mul_ps(vy, dt_vec));
        _mm_store_ps(&system->py[i], py);
    }
    
    // Process Z coordinates
    for (int i = 0; i < count; i += 4) {
        __m128 pz = _mm_load_ps(&system->pz[i]);
        __m128 vz = _mm_load_ps(&system->vz[i]);
        __m128 dt_vec = _mm_set1_ps(dt);
        pz = _mm_add_ps(pz, _mm_mul_ps(vz, dt_vec));
        _mm_store_ps(&system->pz[i], pz);
    }
}
```

### Branch Elimination

```c
// BAD: Branch in inner loop
for (int i = 0; i < count; i++) {
    if (entities[i].health > 0) {
        entities[i].position += entities[i].velocity * dt;
    }
}

// GOOD: Process only active entities (maintain active list)
// Swap dead entities to end, process only alive portion
int aliveCount = 0;
for (int i = 0; i < count; i++) {
    if (entities[i].health > 0) {
        if (i != aliveCount) {
            // Swap to alive section
            Entity temp = entities[aliveCount];
            entities[aliveCount] = entities[i];
            entities[i] = temp;
        }
        aliveCount++;
    }
}

// Now update without branches
for (int i = 0; i < aliveCount; i++) {
    entities[i].position += entities[i].velocity * dt;
}
```

## 9. Debugging Tools

```c
// debug.c - Debug visualization and assertions

#ifdef DEBUG

void debugDrawLine(Vec3 start, Vec3 end, Vec4 color) {
    // Immediate-mode debug rendering
    glBegin(GL_LINES);
    glColor4fv(&color.x);
    glVertex3fv(&start.x);
    glVertex3fv(&end.x);
    glEnd();
}

void debugDrawSphere(Vec3 center, float radius, Vec4 color) {
    const int segments = 16;
    
    for (int i = 0; i < segments; i++) {
        float angle1 = (i / (float)segments) * 2.0f * 3.14159f;
        float angle2 = ((i + 1) / (float)segments) * 2.0f * 3.14159f;
        
        Vec3 p1 = vec3(
            center.x + cosf(angle1) * radius,
            center.y,
            center.z + sinf(angle1) * radius
        );
        
        Vec3 p2 = vec3(
            center.x + cosf(angle2) * radius,
            center.y,
            center.z + sinf(angle2) * radius
        );
        
        debugDrawLine(p1, p2, color);
    }
}

void debugPrintEntityStats(void) {
    int physicsCount = 0;
    int renderCount = 0;
    int aiCount = 0;
    
    for (int i = 0; i < g_entities.count; i++) {
        if (g_entities.flags[i] & ENTITY_HAS_PHYSICS) physicsCount++;
        if (g_entities.flags[i] & ENTITY_HAS_RENDER) renderCount++;
        if (g_entities.flags[i] & ENTITY_HAS_AI) aiCount++;
    }
    
    printf("Entities: %d total, %d physics, %d render, %d AI\n",
           g_entities.count, physicsCount, renderCount, aiCount);
}

#else
// No-op in release builds
#define debugDrawLine(...)
#define debugDrawSphere(...)
#define debugPrintEntityStats()
#endif
```

## Summary: The Carmack Development Cycle

1. **Start Simple**: Write the obvious solution first
2. **Make It Work**: Get correctness before performance
3. **Profile**: Measure where time is actually spent
4. **Optimize Hot Paths**: Focus on the 10% that matters
5. **Maintain Clarity**: Keep code readable for future you
6. **Test Thoroughly**: Verify correctness at every step
7. **Iterate**: Repeat the cycle, never stop improving

The result is code that is:
- **Fast**: Optimized where it matters
- **Clear**: Understandable and maintainable
- **Robust**: Well-tested and debuggable
- **Scalable**: Simple enough to extend

This is the essence of Carmack-style programming.
