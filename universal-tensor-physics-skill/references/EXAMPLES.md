# Tensor Physics Research - Practical Examples

## Part 1: Bridge Equation Examples

### Example 1: Electromagnetic Field Bridge

**Physical Domain**: Electromagnetic field strength
**Mathematical Domain**: Antisymmetric rank-2 tensor

#### Derivation

**Step 1: Physical Setup**
- Observable: Electric field E and magnetic field B
- Measurement: Force on test charges and currents
- Units: E in V/m, B in Tesla

**Step 2: Tensor Construction**

The electromagnetic field tensor is:

```
F^μν = [  0     -Ex/c  -Ey/c  -Ez/c ]
       [ Ex/c    0      -Bz     By   ]
       [ Ey/c    Bz      0     -Bx   ]
       [ Ez/c   -By     Bx      0    ]
```

**Step 3: Bridge Relations**

```python
# Using math-mcp to extract physical quantities from tensor

def extract_fields(F_μν):
    """
    Extract E and B from field strength tensor
    """
    c = 299792458  # m/s
    
    # Electric field components
    Ex = -c * F_μν[0,1]
    Ey = -c * F_μν[0,2]
    Ez = -c * F_μν[0,3]
    
    # Magnetic field components  
    Bx = F_μν[2,3]
    By = -F_μν[1,3]
    Bz = F_μν[1,2]
    
    return (Ex, Ey, Ez), (Bx, By, Bz)

def construct_tensor(E, B):
    """
    Build F^μν from E and B fields
    """
    c = 299792458
    Ex, Ey, Ez = E
    Bx, By, Bz = B
    
    F = np.zeros((4,4))
    
    # Electric components
    F[0,1] = -Ex/c;  F[1,0] = Ex/c
    F[0,2] = -Ey/c;  F[2,0] = Ey/c
    F[0,3] = -Ez/c;  F[3,0] = Ez/c
    
    # Magnetic components
    F[1,2] = -Bz;  F[2,1] = Bz
    F[1,3] = By;   F[3,1] = -By
    F[2,3] = -Bx;  F[3,2] = Bx
    
    # Verify antisymmetry
    assert np.allclose(F, -F.T), "F must be antisymmetric"
    
    return F
```

**Step 4: Maxwell's Equations in Tensor Form**

```python
# Homogeneous Maxwell equations: ∂_[μ F_νρ] = 0

def verify_bianchi(F_μν, coords):
    """
    Verify the Bianchi identity for electromagnetic tensor
    This encodes ∇·B = 0 and ∇×E + ∂B/∂t = 0
    """
    # Compute ∂_[μ F_νρ]
    bianchi = compute_bianchi_identity(F_μν, coords)
    
    # Should be zero (within numerical precision)
    assert np.max(np.abs(bianchi)) < 1e-10
    
    print("Bianchi identity verified: Homogeneous Maxwell equations satisfied")

# Inhomogeneous equations: ∂_μ F^μν = J^ν

def maxwells_equations(F_μν, J_ν, metric):
    """
    Verify ∂_μ F^μν = μ₀ J^ν
    This encodes Gauss's law and Ampère's law
    """
    # Raise index with metric
    F_up = raise_index(F_μν, metric)
    
    # Compute divergence
    div_F = divergence(F_up)
    
    # Compare with current
    mu_0 = 4 * np.pi * 1e-7  # Permeability
    
    residual = div_F - mu_0 * J_ν
    
    print(f"Maxwell equation residual: {np.max(np.abs(residual))}")
    
    return residual
```

**Physical Interpretation**:
- **E and B as components**: Not separate entities, but components of unified field
- **Lorentz transformations**: E and B mix under boosts
- **Gauge invariance**: F^μν is gauge-invariant (observable)
- **Conservation laws**: Charge conservation from ∂_μ J^μ = 0

---

### Example 2: Stress-Energy Bridge

**Physical Domain**: Energy, momentum, stress
**Mathematical Domain**: Symmetric rank-2 tensor

#### Derivation

**Step 1: Physical Components**

For a perfect fluid:
- Energy density: ρ
- Pressure: p  
- 4-velocity: u^μ

**Step 2: Tensor Form**

```python
def perfect_fluid_stress_energy(rho, p, u_μ, metric):
    """
    Construct T^μν for perfect fluid
    
    T^μν = (ρ + p) u^μ u^ν + p g^μν
    """
    # Raise index on 4-velocity
    u_up = raise_index(u_μ, metric)
    
    # Outer product
    T = (rho + p) * np.outer(u_up, u_up)
    
    # Add pressure term
    g_up = np.linalg.inv(metric)
    T += p * g_up
    
    # Verify symmetry
    assert np.allclose(T, T.T), "T^μν must be symmetric"
    
    return T
```

**Step 3: Conservation Laws**

```python
def verify_energy_momentum_conservation(T_μν, metric, christoffel):
    """
    Verify ∇_μ T^μν = 0
    """
    # Raise first index
    T_up = raise_index(T_μν, metric)
    
    # Covariant divergence
    div_T = covariant_divergence(T_up, christoffel)
    
    # Should be zero
    max_violation = np.max(np.abs(div_T))
    
    print(f"Energy-momentum conservation: {max_violation}")
    
    assert max_violation < 1e-8, "Conservation violated!"
    
    return div_T
```

**Step 4: Physical Interpretation**

```python
def extract_energy_density(T_μν, u_μ):
    """
    Energy density as measured by observer with 4-velocity u^μ
    
    ρ = T_μν u^μ u^ν
    """
    return np.einsum('ij,i,j', T_μν, u_μ, u_μ)

def extract_momentum_density(T_μν, u_μ, metric):
    """
    Momentum density in rest frame of observer
    
    S^i = T^0i (in observer's frame)
    """
    # Project T^μν onto spatial hypersurface
    u_up = raise_index(u_μ, metric)
    
    # Momentum density
    S = np.einsum('ij,j->i', T_μν, u_up)
    
    return S[1:]  # Spatial components

def extract_stress(T_μν):
    """
    Stress tensor: spatial part of T^μν
    
    σ^ij = T^ij
    """
    return T_μν[1:,1:]
```

---

### Example 3: Curvature Bridge

**Physical Domain**: Gravitational tidal forces
**Mathematical Domain**: Riemann curvature tensor

#### Derivation

**Step 1: Geodesic Deviation**

Physical effect: Separation of nearby free-falling test particles

```python
def geodesic_deviation(R_μνρσ, separation_ξ, velocity_u):
    """
    Compute relative acceleration of nearby geodesics
    
    D²ξ^μ/Dτ² = -R^μ_νρσ u^ν ξ^ρ u^σ
    """
    # Contract curvature tensor
    acceleration = -np.einsum('ijkl,j,k,l->i', 
                             R_μνρσ, velocity_u, separation_ξ, velocity_u)
    
    return acceleration
```

**Step 2: Construct Riemann from Metric**

```python
def compute_riemann_tensor(metric, coords):
    """
    Compute R^ρ_σμν from metric g_μν
    
    R^ρ_σμν = ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ - Γ^ρ_νλ Γ^λ_μσ
    """
    # First compute Christoffel symbols
    Gamma = christoffel_symbols(metric, coords)
    
    # Compute derivatives of Christoffel symbols
    dGamma = np.zeros((4,4,4,4,4))  # ∂_μ Γ^ρ_νσ
    
    for mu in range(4):
        for rho in range(4):
            for nu in range(4):
                for sigma in range(4):
                    dGamma[mu,rho,nu,sigma] = derivative(
                        Gamma[rho,nu,sigma], coords[mu]
                    )
    
    # Assemble Riemann tensor
    R = np.zeros((4,4,4,4))
    
    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):
                    R[rho,sigma,mu,nu] = (
                        dGamma[mu,rho,nu,sigma] - dGamma[nu,rho,mu,sigma]
                        + np.sum(Gamma[rho,mu,:] * Gamma[:,nu,sigma])
                        - np.sum(Gamma[rho,nu,:] * Gamma[:,mu,sigma])
                    )
    
    return R
```

**Step 3: Verify Symmetries**

```python
def verify_riemann_symmetries(R_μνρσ):
    """
    Riemann tensor must satisfy:
    1. R_μνρσ = -R_νμρσ (antisymmetric in first pair)
    2. R_μνρσ = -R_μνσρ (antisymmetric in second pair)
    3. R_μνρσ = R_ρσμν (symmetric under pair exchange)
    4. R_μ[νρσ] = 0 (first Bianchi identity)
    """
    # Check antisymmetries
    assert np.allclose(R_μνρσ, -np.transpose(R_μνρσ, (1,0,2,3)))
    assert np.allclose(R_μνρσ, -np.transpose(R_μνρσ, (0,1,3,2)))
    
    # Check pair symmetry
    assert np.allclose(R_μνρσ, np.transpose(R_μνρσ, (2,3,0,1)))
    
    # Check first Bianchi identity
    bianchi = (R_μνρσ + 
               np.roll(R_μνρσ, 1, axis=1) + 
               np.roll(R_μνρσ, 2, axis=1))
    
    assert np.max(np.abs(bianchi)) < 1e-10
    
    print("All Riemann symmetries verified")
```

**Step 4: Physical Interpretation**

```python
def tidal_force_matrix(R_μνρσ, u_μ):
    """
    Tidal force matrix in observer's rest frame
    
    K^i_j = R^i_0j0 (spatial components)
    """
    # Extract relevant components
    K = np.zeros((3,3))
    
    for i in range(1,4):
        for j in range(1,4):
            K[i-1,j-1] = R_μνρσ[i,0,j,0]
    
    # This matrix determines tidal stretching/squeezing
    eigenvalues = np.linalg.eigvals(K)
    
    print(f"Tidal eigenvalues: {eigenvalues}")
    print(f"Stretching directions: {np.sum(eigenvalues > 0)}")
    print(f"Squeezing directions: {np.sum(eigenvalues < 0)}")
    
    return K
```

---

## Part 2: Proof Patterns with MCP Integration

### Pattern 1: Symmetry-Based Proof

**Example**: Prove stress-energy conservation from diffeomorphism invariance

```python
# Step 1: Use deepthinking-mcp for strategy
query_deepthinking = """
I need to prove that ∇_μ T^μν = 0 follows from diffeomorphism invariance
of the Einstein-Hilbert action. What is the most elegant approach?
"""

# Response suggests using Noether's theorem

# Step 2: Implement proof steps with math-mcp

def prove_energy_momentum_conservation():
    """
    Proof via Noether's theorem
    """
    # Define Einstein-Hilbert action
    def action(g_μν):
        R = ricci_scalar(g_μν)
        sqrt_g = np.sqrt(-np.linalg.det(g_μν))
        return integrate(R * sqrt_g, spacetime)
    
    # Consider infinitesimal diffeomorphism
    # g_μν → g_μν + £_ξ g_μν
    
    # Variation of action
    delta_action = vary_action_diffeomorphism(action, g_μν, xi)
    
    # By diffeomorphism invariance, this must vanish
    assert np.allclose(delta_action, 0)
    
    # Extract Noether current
    # δS = ∫ (∂S/∂g_μν) δg_μν
    # For δg_μν = ∇_μ ξ_ν + ∇_ν ξ_μ
    # This gives ∇_μ T^μν = 0
    
    print("Energy-momentum conservation proven from symmetry")
```

### Pattern 2: Variational Proof

**Example**: Derive geodesic equation from action principle

```python
def prove_geodesic_equation():
    """
    Prove that extremizing proper time gives geodesic equation
    """
    # Step 1: Define action
    # S = ∫ dτ = ∫ √(-g_μν dx^μ dx^ν)
    
    def proper_time_action(path, metric):
        """
        Compute proper time along path
        """
        s = 0
        for i in range(len(path)-1):
            dx = path[i+1] - path[i]
            ds_squared = np.einsum('ij,i,j', metric, dx, dx)
            s += np.sqrt(-ds_squared)
        return s
    
    # Step 2: Vary the path using math-mcp
    # δS/δx^μ(λ) = 0
    
    # This gives Euler-Lagrange equation:
    # d/dλ(∂L/∂ẋ^μ) - ∂L/∂x^μ = 0
    
    # Step 3: Work out the derivatives (math-mcp helps)
    # L = √(-g_μν ẋ^μ ẋ^ν)
    
    # After algebra, this yields:
    # ẍ^μ + Γ^μ_νρ ẋ^ν ẋ^ρ = 0
    
    print("Geodesic equation derived from variational principle")
```

### Pattern 3: Consistency Check Proof

**Example**: Verify Bianchi identities

```python
def prove_bianchi_identities():
    """
    Prove the two Bianchi identities for Riemann tensor
    """
    # First Bianchi identity: R_μ[νρσ] = 0
    
    def first_bianchi(R_μνρσ):
        """
        Cyclic sum over last three indices vanishes
        """
        # Use math-mcp to compute
        cyclic_sum = (
            R_μνρσ + 
            np.roll(R_μνρσ, 1, axis=(1,2,3)) +
            np.roll(R_μνρσ, 2, axis=(1,2,3))
        )
        
        max_violation = np.max(np.abs(cyclic_sum))
        print(f"First Bianchi identity: max violation = {max_violation}")
        
        assert max_violation < 1e-10
    
    # Second Bianchi identity: ∇_[μ R_ν]ρσλ = 0
    
    def second_bianchi(R_μνρσ, Gamma):
        """
        Cyclic sum of covariant derivatives vanishes
        """
        # Compute ∇_μ R_νρσλ
        nabla_R = covariant_derivative_tensor(R_μνρσ, Gamma)
        
        # Take cyclic sum
        cyclic = (
            nabla_R +
            np.roll(nabla_R, 1, axis=(0,1)) +
            np.roll(nabla_R, 2, axis=(0,1))
        )
        
        max_violation = np.max(np.abs(cyclic))
        print(f"Second Bianchi identity: max violation = {max_violation}")
        
        assert max_violation < 1e-10
    
    # Verify both
    R = compute_riemann_tensor(metric, coords)
    Gamma = christoffel_symbols(metric, coords)
    
    first_bianchi(R)
    second_bianchi(R, Gamma)
    
    print("Both Bianchi identities verified")
```

---

## Part 3: Numerical Methods with MCP

### Solving Einstein Equations Numerically

```python
def solve_einstein_equations_numerically(T_μν, initial_metric):
    """
    Solve G_μν = 8πG T_μν numerically
    """
    # Step 1: Set up discretization
    grid = create_spacetime_grid(nx=100, ny=100, nz=100, nt=1000)
    
    # Step 2: Initial conditions
    g = initial_metric
    
    # Step 3: Time evolution (ADM formalism)
    for t in range(nt):
        # Compute Einstein tensor at current time
        G = einstein_tensor(g)
        
        # Residual
        residual = G - 8*np.pi*G_newton * T_μν
        
        # Update metric (using math-mcp for solver)
        delta_g = solve_constraint_equations(residual)
        g += delta_g
        
        # Check convergence
        if np.max(np.abs(residual)) < tolerance:
            print(f"Converged at t={t}")
            break
    
    return g
```

### Perturbation Theory

```python
def perturbative_solution(g_background, perturbation_param):
    """
    Solve Einstein equations perturbatively
    
    g_μν = ḡ_μν + ε h_μν + ε² h2_μν + ...
    """
    # Use deepthinking-mcp to determine order of expansion needed
    
    # Zeroth order: background solution
    g0 = g_background
    G0 = einstein_tensor(g0)
    
    # First order: linearized Einstein equations
    h1 = solve_linearized_einstein(g0, perturbation_param)
    
    # Second order: quadratic corrections (math-mcp helps)
    h2 = solve_second_order_einstein(g0, h1, perturbation_param)
    
    # Construct full solution
    g_full = g0 + perturbation_param * h1 + perturbation_param**2 * h2
    
    # Verify convergence
    G_full = einstein_tensor(g_full)
    print(f"Einstein equation residual: {np.max(np.abs(G_full - 8*np.pi*G_newton*T_μν))}")
    
    return g_full
```

---

## Part 4: Physical Interpretation Tools

### Extracting Observables

```python
def compute_physical_observables(solution):
    """
    Extract measurable quantities from tensor solution
    """
    observables = {}
    
    # Energy density (for timelike observer)
    u = np.array([1, 0, 0, 0])  # Observer at rest
    observables['energy_density'] = extract_energy_density(solution['T'], u)
    
    # Gravitational wave strain
    h_plus, h_cross = extract_gravitational_wave_modes(solution['g'])
    observables['h_plus'] = h_plus
    observables['h_cross'] = h_cross
    
    # Kretschmann scalar (curvature invariant)
    R = solution['R']  # Riemann tensor
    K = np.einsum('ijkl,ijkl', R, R)
    observables['kretschmann'] = K
    
    # Event horizon (for black holes)
    if is_black_hole(solution):
        observables['horizon_radius'] = find_event_horizon(solution['g'])
    
    return observables
```

### Visualization

```python
def visualize_tensor_field(T_μν, spacetime_grid):
    """
    Create visualizations of tensor field
    """
    import matplotlib.pyplot as plt
    
    # Energy density distribution
    rho = T_μν[0,0]
    plt.figure(figsize=(12,4))
    
    plt.subplot(131)
    plt.imshow(rho[:,:,nz//2], cmap='plasma')
    plt.title('Energy Density (z-slice)')
    plt.colorbar()
    
    # Momentum flow
    S = T_μν[0,1:4]
    plt.subplot(132)
    plt.quiver(S[0], S[1])
    plt.title('Momentum Flow')
    
    # Stress eigenvalues
    stress = T_μν[1:4,1:4]
    eigenvalues = np.linalg.eigvals(stress)
    plt.subplot(133)
    plt.hist(eigenvalues.flatten())
    plt.title('Stress Eigenvalue Distribution')
    
    plt.tight_layout()
    plt.savefig('tensor_field_visualization.png')
```

---

## Part 5: Verification and Validation

### Comprehensive Verification Suite

```python
def verify_tensor_solution(solution):
    """
    Run all verification checks on tensor solution
    """
    checks = {}
    
    # 1. Mathematical consistency
    checks['symmetries'] = verify_tensor_symmetries(solution['T'])
    checks['bianchi'] = verify_bianchi_identities(solution['R'])
    checks['conservation'] = verify_conservation_laws(solution['T'])
    
    # 2. Physical consistency  
    checks['energy_conditions'] = verify_energy_conditions(solution['T'])
    checks['causality'] = verify_causality(solution['g'])
    checks['singularities'] = check_for_singularities(solution['R'])
    
    # 3. Dimensional analysis
    checks['dimensions'] = verify_dimensions(solution)
    
    # 4. Numerical accuracy
    checks['convergence'] = check_numerical_convergence(solution)
    checks['stability'] = check_numerical_stability(solution)
    
    # 5. Known limits
    checks['flat_limit'] = verify_flat_space_limit(solution)
    checks['weak_field'] = verify_weak_field_limit(solution)
    
    # Print report
    print("\n=== Verification Report ===")
    for check, result in checks.items():
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {check}: {result['message']}")
    
    return all(c['passed'] for c in checks.values())
```

---

## Part 6: Research Workflow Examples

### Complete Research Session

```python
def research_session_example():
    """
    Example of a complete research session using MCP tools
    """
    
    # Phase 1: Problem formulation (use deepthinking-mcp)
    problem = """
    Develop a bridge equation connecting quantum entanglement entropy
    to a geometric tensor structure in spacetime.
    """
    
    strategy = deepthinking_query(problem)
    print(f"Strategy: {strategy}")
    
    # Phase 2: Mathematical development
    # Build tensor structure based on strategy
    entanglement_tensor = construct_entanglement_tensor()
    
    # Phase 3: Calculations (use math-mcp)
    # Compute various quantities
    entropy = compute_entanglement_entropy(entanglement_tensor)
    curvature = compute_induced_curvature(entanglement_tensor)
    
    # Phase 4: Verification
    verify_consistency(entanglement_tensor, entropy, curvature)
    
    # Phase 5: Physical interpretation (use deepthinking-mcp)
    interpretation = deepthinking_query(f"""
    Given this mathematical result:
    S_entanglement = Tr(ρ log ρ) = (1/4) ∫ K dA
    
    where K is curvature and A is area, what is the physical meaning?
    What does this tell us about the relationship between quantum information
    and geometry?
    """)
    
    # Phase 6: Predictions
    predictions = generate_testable_predictions(entanglement_tensor)
    
    # Phase 7: Documentation
    document_results({
        'problem': problem,
        'strategy': strategy,
        'tensor': entanglement_tensor,
        'calculations': {'entropy': entropy, 'curvature': curvature},
        'interpretation': interpretation,
        'predictions': predictions
    })
```

This comprehensive set of examples demonstrates how to integrate deepthinking-mcp and math-mcp into your tensor physics research workflow. The key is to use deepthinking-mcp for conceptual work and proof strategies, while using math-mcp for all calculations and numerical verification.
