# Universal Tensor Physics Skill

A specialized Claude Code skill for Universal Tensor Physics Framework (UPTF) research — theoretical physics proofs, tensor mathematics, and bridge equations between physical and mathematical domains.

## What It Does

| Capability | Description |
|---|---|
| **Bridge Equations** | Formal derivation connecting physical observables to mathematical structures with 6-step templates |
| **Tensor Formalism** | Rigorous index conventions, Einstein summation, covariant derivatives, Lie derivatives, curvature tensors |
| **Proof Development** | Step-by-step derivation and verification of theoretical results with consistency checks |
| **MCP Integration** | Leverages deepthinking-mcp for conceptual reasoning and math-mcp for rigorous calculations |
| **Research Methodology** | 4-phase workflow: Formulation, Mathematical Development, Physical Interpretation, Validation |
| **Worked Examples** | Electromagnetic field bridge, stress-energy tensor, conservation law verification |

## When to Use

- Working on theoretical physics proofs or derivations
- Tensor mathematics requiring rigorous notation and index conventions
- Bridge equations between physical and mathematical domains
- User mentions UPTF, tensor framework, physics unification
- Working through theoretical physics derivations requiring step-by-step verification
- Integrating physical observables with mathematical structures

## When NOT to Use

- Applied physics problems not requiring tensor formalism
- Standard numerical computation or data analysis
- Experimental physics (measurement, instrumentation)
- Problems that don't involve bridging physical and mathematical domains

## Directory Structure

```
universal-tensor-physics-skill/
├── SKILL.md                    # Skill definition with framework, methodology, and notation (19.1 KB)
└── examples/
    └── EXAMPLES.md             # Worked examples: EM field bridge, stress-energy tensor (19.0 KB)
```

## The UPTF Paradigm

The Universal Tensor Physics Framework distinguishes between:

- **The Physical** (atoms): Observable reality, experimental data, physical systems
- **The Virtual** (axioms): Mathematical structures, logical frameworks, theoretical constructs

**Central thesis:** A unified tensor framework bridges these domains, providing rigorous mathematical foundations for physical theories, predictive power from first principles, and unification of disparate physical phenomena.

## Framework Components

### Tensor Notation Standards

| Convention | Meaning |
|---|---|
| Greek indices (mu, nu, ...) | Spacetime components (0-3) |
| Latin indices (i, j, ...) | Spatial components (1-3) |
| Uppercase indices | Abstract/internal spaces |
| Lowercase indices | Coordinate representations |
| Einstein summation | Repeated upper/lower indices are summed |

### Key Operations

- **Contraction** — Trace over paired indices
- **Covariant derivative** — Connection-aware differentiation preserving tensor character
- **Lie derivative** — Measures change along a vector field flow
- **Christoffel symbols** — Connection coefficients for covariant derivatives
- **Riemann curvature** — Measures spacetime curvature via parallel transport failure
- **Bianchi identity** — Constraint on curvature tensor symmetries

### Bridge Equation Template

A bridge equation connects physical observables to mathematical structures. The 6-step derivation process:

1. **Physical Specification** — Define the physical domain and observables
2. **Mathematical Structure** — Identify the appropriate tensor/algebraic framework
3. **Bridge Relation** — Write the formal mapping between domains
4. **Derivation Steps** — Step-by-step mathematical development
5. **Verification** — Check mathematical consistency, dimensional correctness, symmetry preservation, physical interpretation, known limits
6. **Physical Predictions** — Extract testable predictions from the mathematical result

### Research Methodology

```
1. FORMULATION
   ├─ Define the problem in tensor notation
   ├─ Identify relevant symmetries and conservation laws
   └─ Establish boundary conditions and constraints

2. MATHEMATICAL DEVELOPMENT
   ├─ Use deepthinking-mcp for conceptual breakthroughs
   ├─ Use math-mcp for rigorous calculations
   └─ Develop formal proofs step-by-step

3. PHYSICAL INTERPRETATION
   ├─ Map mathematical results back to physical observables
   ├─ Verify consistency with known physics
   └─ Generate testable predictions

4. VALIDATION
   ├─ Check mathematical consistency
   ├─ Verify dimensional analysis
   ├─ Compare with experimental data where available
   └─ Document assumptions and limitations
```

### Common Research Patterns

| Pattern | Description |
|---|---|
| Symmetry-based derivation | Exploit symmetry groups to constrain tensor form |
| Variational derivation | Derive equations of motion from action principles |
| Perturbative expansion | Expand around known solutions for approximate results |
| Dimensional analysis | Verify physical consistency of tensor equations |

## Examples Reference

The `examples/EXAMPLES.md` file provides worked examples including:

### Electromagnetic Field Bridge
- Maps electromagnetic field observables to the Faraday tensor
- Demonstrates physical-to-mathematical domain mapping
- Includes tensor extraction and Maxwell's equations verification

### Stress-Energy Bridge
- Constructs the perfect fluid stress-energy tensor T^{mu nu}
- Demonstrates index raising/lowering operations
- Verifies conservation law (nabla_mu T^{mu nu} = 0)
- Shows physical interpretation and extraction methods

### Techniques Demonstrated
- Outer product tensor construction
- Index manipulation (raising, lowering, contraction)
- Conservation law verification via covariant divergence
- Physical observable extraction from tensor components

## Usage

The skill triggers in Claude Code when the user mentions UPTF, tensor framework, physics unification, or theoretical physics derivations. It integrates with:

- **deepthinking-mcp** — For conceptual breakthroughs, symmetry analysis, physical insight
- **math-mcp** — For rigorous calculations, tensor algebra, verification

Typical workflow:
1. User describes a physics problem or derivation goal
2. Skill provides tensor notation standards and methodology
3. Bridge equation template guides systematic derivation
4. Verification checklist ensures mathematical and physical consistency
5. Results documented with assumptions and limitations

## Documentation Standards

- All equations labeled with descriptive tags
- Notation declared before first use
- Assumptions explicitly tracked throughout derivations
- Research templates provided for documenting new results
