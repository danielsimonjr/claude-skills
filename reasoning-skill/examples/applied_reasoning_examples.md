# Applied Reasoning Examples by Domain

This file demonstrates how different reasoning types apply to specific domains and use cases.

## Software Engineering

### Code Review: Critical + Analytical + Evidential Reasoning

**Scenario**: Reviewing a pull request for a new authentication feature

**Critical Reasoning Application**:
```python
# Code under review:
def authenticate_user(username, password):
    user = db.query("SELECT * FROM users WHERE username = '" + username + "'")
    if user and user.password == password:
        return create_session(user)
    return None
```

**Critical Analysis**:
1. **Security vulnerability identified**: SQL injection risk
   - Evidence: String concatenation with user input
   - Reasoning: Attacker could input: `' OR '1'='1`

2. **Password handling issue**: Plain text comparison
   - Evidence: Direct password comparison
   - Reasoning: Suggests passwords stored in plain text

3. **Missing input validation**
   - Evidence: No sanitization or validation
   - Reasoning: Multiple attack vectors possible

**Improved Code**:
```python
def authenticate_user(username, password):
    # Input validation (defensive programming)
    if not username or not password:
        return None
    
    # Parameterized query (prevents SQL injection)
    user = db.query(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    
    # Secure password verification (hashed comparison)
    if user and verify_password_hash(password, user.password_hash):
        return create_session(user)
    
    return None
```

### Algorithm Selection: Comparative + Quantitative + Optimization Reasoning

**Problem**: Choose sorting algorithm for different data characteristics

**Analysis Matrix**:
| Algorithm | Time (Avg) | Time (Worst) | Space | Stable | Best Use Case |
|-----------|-----------|--------------|-------|--------|---------------|
| QuickSort | O(n log n) | O(n²) | O(log n) | No | General purpose, in-place needed |
| MergeSort | O(n log n) | O(n log n) | O(n) | Yes | Stable sort needed, linked lists |
| HeapSort | O(n log n) | O(n log n) | O(1) | No | Memory constrained, guaranteed performance |
| TimSort | O(n log n) | O(n log n) | O(n) | Yes | Real-world data with partial ordering |

**Reasoning Process**:
```python
def select_sorting_algorithm(data, constraints):
    """
    Multi-criteria decision using comparative and constraint-based reasoning
    """
    # Constraint-based reasoning
    if constraints.memory_limited and constraints.require_stable:
        # Impossible constraints
        return "heap_sort"  # Sacrifice stability for memory
    
    # Quantitative reasoning
    data_size = len(data)
    is_nearly_sorted = check_sorted_ratio(data) > 0.5
    
    # Comparative + heuristic reasoning
    if constraints.require_stable:
        if is_nearly_sorted:
            return "timsort"  # Optimized for partially sorted data
        elif data_size < 1000:
            return "insertion_sort"  # Simple, stable, good for small data
        else:
            return "mergesort"  # Stable, predictable
    
    elif constraints.memory_limited:
        return "heap_sort"  # In-place, guaranteed O(n log n)
    
    else:
        return "quicksort"  # Generally fastest in practice
```

### Architecture Design: Systems + Strategic + Constraint-Based Reasoning

**Scenario**: Design microservices architecture for e-commerce platform

**Systems Reasoning**:
```
Components:
- User Service (authentication, profiles)
- Product Service (catalog, inventory)
- Order Service (cart, checkout, orders)
- Payment Service (payment processing)
- Notification Service (emails, push notifications)

Interactions:
- User → Product (browse catalog)
- User → Order (create order)
- Order → Payment (process payment)
- Order → Notification (order confirmation)
- Payment → Notification (payment receipt)

Feedback Loops:
- Inventory updates → Product Service → Order Service
- Failed payments → Order Service → User notification
```

**Constraint-Based Reasoning**:
```yaml
constraints:
  performance:
    - response_time: < 200ms (p95)
    - throughput: > 10,000 requests/second
  
  reliability:
    - availability: 99.9% (three nines)
    - data_consistency: eventual consistency acceptable
  
  scalability:
    - horizontal_scaling: required
    - stateless_services: preferred
  
  security:
    - authentication: OAuth 2.0
    - encryption: TLS in transit, AES-256 at rest
    - pci_compliance: required for payment service
```

**Strategic Reasoning**:
```
Decision 1: Service Communication Pattern
Options:
  A) Synchronous REST
  B) Asynchronous message queue
  C) Hybrid approach

Analysis:
  REST: Simple, but tight coupling, cascading failures
  Queue: Loose coupling, resilient, but complex, eventual consistency
  Hybrid: Best of both, but increased complexity

Choice: Hybrid
  - REST for user-facing synchronous operations
  - Queue for background processing and inter-service events
  
Reasoning: Balance immediacy with resilience

Decision 2: Database Strategy
Options:
  A) Shared database
  B) Database per service
  C) Hybrid (shared + dedicated)

Analysis:
  Shared: Simple, but tight coupling, single point of failure
  Per service: True independence, but complex transactions
  
Choice: Database per service
  - Use saga pattern for distributed transactions
  - Accept eventual consistency
  
Reasoning: Prioritize service independence and scalability
```

---

## Data Science & Machine Learning

### Feature Engineering: Analytical + Domain-Specific + Creative Reasoning

**Problem**: Predict customer churn for subscription service

**Domain-Specific Reasoning**:
```python
# Understanding what matters in subscription business
behavioral_signals = [
    'login_frequency',  # Engagement indicator
    'feature_usage',    # Value realization
    'support_tickets',  # Friction/dissatisfaction
    'payment_issues',   # Financial barriers
]

temporal_patterns = [
    'usage_trend',           # Increasing or decreasing
    'days_since_last_login', # Recency
    'subscription_age',      # Lifecycle stage
]
```

**Creative Reasoning** (Feature Creation):
```python
def engineer_churn_features(customer_data):
    """
    Combine analytical understanding with creative feature engineering
    """
    features = {}
    
    # Ratio features (comparative reasoning)
    features['engagement_ratio'] = (
        customer_data['active_days'] / customer_data['subscription_days']
    )
    
    # Trend features (temporal reasoning)
    features['usage_trend'] = calculate_trend(customer_data['daily_usage'])
    
    # Interaction features (relational reasoning)
    features['value_engagement'] = (
        customer_data['features_used'] * customer_data['login_frequency']
    )
    
    # Anomaly features (statistical reasoning)
    features['usage_drop'] = detect_sudden_decrease(customer_data['usage_history'])
    
    # Lifecycle features (categorical reasoning)
    features['at_risk_phase'] = is_in_critical_period(
        customer_data['subscription_age'],
        critical_periods=[30, 90, 180]  # First month, quarter, half-year
    )
    
    return features
```

**Analytical Reasoning** (Feature Importance):
```python
# After model training
feature_importance = model.feature_importances_

# Analyze which features matter most
top_features = sorted(
    zip(feature_names, feature_importance),
    key=lambda x: x[1],
    reverse=True
)

# Interpret results (evidential reasoning)
"""
Finding: 'days_since_last_login' is most important predictor

Interpretation:
- Strong signal: Recent disengagement predicts churn
- Actionable: Can trigger re-engagement campaigns
- Causal hypothesis: Disengagement → forgetting value → churn

Implication for business:
- Focus retention efforts on detecting disengagement early
- Automated email campaigns after 7, 14, 21 days of inactivity
"""
```

### Model Selection: Comparative + Evidential + Trade-off Reasoning

**Problem**: Choose ML model for fraud detection

**Requirements Analysis**:
```python
requirements = {
    'performance': {
        'precision': 'high',  # Few false positives (don't block legitimate transactions)
        'recall': 'very_high',  # Catch most fraud (financial impact of misses is high)
        'latency': '<100ms',  # Real-time decision needed
    },
    'interpretability': 'high',  # Need to explain decisions for compliance
    'imbalanced_data': True,  # Fraud is rare (0.1% of transactions)
}
```

**Comparative Analysis**:
```python
models_evaluated = {
    'logistic_regression': {
        'pros': ['Fast', 'Interpretable', 'Simple'],
        'cons': ['May miss complex patterns', 'Linear decision boundary'],
        'metrics': {'precision': 0.85, 'recall': 0.75, 'latency': 10ms},
    },
    'random_forest': {
        'pros': ['Handles non-linear patterns', 'Handles imbalanced data well', 'Feature importance'],
        'cons': ['Less interpretable', 'Slower'],
        'metrics': {'precision': 0.90, 'recall': 0.88, 'latency': 50ms},
    },
    'xgboost': {
        'pros': ['Best performance', 'Handles imbalanced data', 'Fast prediction'],
        'cons': ['Complex to tune', 'Less interpretable'],
        'metrics': {'precision': 0.92, 'recall': 0.91, 'latency': 30ms},
    },
    'deep_learning': {
        'pros': ['Can learn complex patterns', 'Scalable'],
        'cons': ['Black box', 'Requires more data', 'Slow', 'Overkill'],
        'metrics': {'precision': 0.93, 'recall': 0.90, 'latency': 150ms},
    },
}
```

**Decision Matrix** (Multi-Criteria Reasoning):
```
           Performance  Interpretability  Latency  Complexity  SCORE
LR         ⭐⭐⭐        ⭐⭐⭐⭐⭐          ⭐⭐⭐⭐⭐   ⭐⭐⭐⭐⭐    88/100
RF         ⭐⭐⭐⭐      ⭐⭐⭐             ⭐⭐⭐⭐    ⭐⭐⭐       82/100
XGBoost    ⭐⭐⭐⭐⭐    ⭐⭐               ⭐⭐⭐⭐    ⭐⭐         85/100
DL         ⭐⭐⭐⭐⭐    ⭐                 ⭐⭐       ⭐           65/100

Decision: XGBoost
Reasoning:
- Best balance of performance and latency
- Meets latency requirement (<100ms)
- Can use SHAP for interpretability
- Proven effective for fraud detection
- Acceptable complexity for the team
```

---

## Scientific Research

### Hypothesis Testing: Abductive + Deductive + Evidential Reasoning

**Research Question**: Does regular meditation reduce stress levels?

**Phase 1: Abductive (Hypothesis Generation)**
```
Observation:
- Meditators report feeling calmer
- Brain imaging shows changes in stress-related regions
- Physiological markers differ between meditators and non-meditators

Possible Explanations:
1. Meditation directly reduces stress response
2. Selection bias (calm people choose meditation)
3. Expectation effects (placebo)
4. Lifestyle correlation (meditators have healthier lifestyles overall)

Best Hypothesis:
Regular meditation practice causes measurable reduction in stress levels
through neuroplastic changes in stress-response systems.
```

**Phase 2: Deductive (Prediction Derivation)**
```
If hypothesis is true, then we should observe:
1. Cortisol levels decrease after meditation training
2. fMRI shows reduced amygdala reactivity to stressors
3. Self-reported stress decreases
4. Effect should be dose-dependent (more practice → more benefit)
5. Effect should persist beyond meditation sessions
6. Randomized assignment should show effect (rules out selection bias)
```

**Phase 3: Experimental Design (Systematic + Methodological Reasoning)**
```python
study_design = {
    'type': 'Randomized Controlled Trial',
    'sample_size': 120,  # Power analysis for medium effect size
    'groups': {
        'experimental': 'Daily 20-min meditation for 8 weeks',
        'active_control': 'Daily 20-min listening to audiobook',
        'waitlist_control': 'No intervention'
    },
    'measures': {
        'primary': 'Cortisol levels (saliva samples)',
        'secondary': [
            'fMRI amygdala reactivity',
            'Perceived Stress Scale (PSS-10)',
            'Daily stress diaries'
        ]
    },
    'controls': {
        'randomization': 'Computer-generated random assignment',
        'blinding': 'Assessors blind to group assignment',
        'confounds': 'Control for exercise, sleep, diet'
    }
}
```

**Phase 4: Statistical Analysis (Quantitative + Probabilistic Reasoning)**
```python
# Statistical reasoning for hypothesis testing
results = {
    'cortisol_change': {
        'meditation_group': -15.2,  # percent change
        'audiobook_group': -2.1,
        'waitlist_group': +1.5,
        'p_value': 0.003,  # Probability of this difference by chance
        'effect_size': 0.62  # Cohen's d (medium-large effect)
    }
}

# Bayesian reasoning for interpretation
prior_probability = 0.3  # Based on literature review
likelihood = 0.997  # P(data | hypothesis true) from p-value
posterior_probability = bayesian_update(prior_probability, likelihood)
# Posterior: ~0.92 (strong evidence for hypothesis)
```

**Phase 5: Interpretation (Critical + Evidential Reasoning)**
```
Evidence Support:
✓ Cortisol decreased significantly in meditation group
✓ Effect was dose-dependent (compliance correlated with benefit)
✓ Active control rules out mere expectation/relaxation time
✓ Effect size clinically meaningful

Evidence Against:
✗ fMRI results showed trend but not significance (n too small?)
✗ Self-report measures showed smaller effect than physiological

Alternative Explanations Considered:
- Regression to mean: Unlikely (randomized assignment)
- Placebo effect: Partially controlled (active control group)
- Experimenter bias: Mitigated (blinded assessment)

Conclusion:
Strong evidence that meditation reduces stress via physiological pathways.
Effect robust but not universal. Further research needed on mechanisms
and individual differences in response.
```

---

## Business Strategy

### Market Entry Decision: Strategic + Game-Theoretic + Scenario Reasoning

**Situation**: Tech startup considering entering competitive SaaS market

**Strategic Analysis**:
```
Current Market Landscape:
- Dominant player: 60% market share
- 3 smaller competitors: 10-15% each
- Remaining: fragmented long tail

Our Advantages:
- Novel AI-powered feature
- Lower pricing tier
- Better UX for specific segment

Our Challenges:
- Unknown brand
- Limited resources
- Established competitors with network effects
```

**Game-Theoretic Reasoning** (Anticipating Competitor Responses):
```python
def analyze_competitive_dynamics(our_strategy):
    """
    Model likely competitor responses
    """
    scenarios = []
    
    # Scenario 1: Dominant player ignores us
    scenarios.append({
        'competitor_action': 'ignore',
        'probability': 0.3,
        'reasoning': 'We are too small to matter initially',
        'our_outcome': 'Successful niche entry',
        'payoff': 7
    })
    
    # Scenario 2: Dominant player matches our features
    scenarios.append({
        'competitor_action': 'feature_parity',
        'probability': 0.4,
        'reasoning': 'Protects market share, they have resources',
        'our_outcome': 'Differentiation lost, compete on price/brand',
        'payoff': 3
    })
    
    # Scenario 3: Dominant player acquires us
    scenarios.append({
        'competitor_action': 'acquisition_offer',
        'probability': 0.2,
        'reasoning': 'Cheaper than competing, gain our innovation',
        'our_outcome': 'Early exit',
        'payoff': 8
    })
    
    # Scenario 4: Aggressive price war
    scenarios.append({
        'competitor_action': 'price_war',
        'probability': 0.1,
        'reasoning': 'Send message to future entrants',
        'our_outcome': 'Unsustainable, potential failure',
        'payoff': 1
    })
    
    # Calculate expected value
    expected_value = sum(s['probability'] * s['payoff'] for s in scenarios)
    
    return scenarios, expected_value
```

**Scenario Planning** (Hypothetical + Contingency Reasoning):
```
Best Case (20% probability):
- Quick market acceptance
- Dominant player doesn't respond aggressively
- Capture 5% market share in year 1
- Path to profitability by year 2

Expected Case (60% probability):
- Moderate adoption
- Some competitive response
- Capture 2-3% market share in year 1
- Need additional funding round

Worst Case (20% probability):
- Slow adoption
- Aggressive competitive response
- Burn through funding
- Pivot or shutdown by year 2

Decision: Enter market with hedging strategy
- Start with focused vertical segment
- Build switching costs early
- Prepare for both acquisition and competition scenarios
- Reserve capital for 18 months runway minimum
```

---

## Legal Reasoning

### Case Analysis: Analogical + Evidential + Normative Reasoning

**Scenario**: Copyright infringement claim for software

**Analogical Reasoning** (Precedent Analysis):
```
Current Case:
Company A claims Company B copied their API design and documentation.

Relevant Precedent 1: Oracle v. Google (2021)
- Issue: Can API declarations be copyrighted?
- Holding: Fair use allows copying of API for interoperability
- Similarity: Both involve API copying
- Distinction: Google's use was transformative (Android platform)

Relevant Precedent 2: Lotus v. Borland (1995)
- Issue: Can menu command hierarchy be copyrighted?
- Holding: No, it's a method of operation (uncopyrightable)
- Similarity: Both involve functional interfaces
- Distinction: Lotus was about user interface, not API

Analogical Reasoning:
Our case is more like Oracle v. Google because:
- Involves API structure, not just menu layout
- Interoperability is central purpose
- Functional necessity drives design choices

However, distinction:
- Our defendant didn't create new platform
- More direct competitive copying
- Less transformative use
```

**Evidential Reasoning** (Weighing Evidence):
```
Evidence for Infringement:
✓ Substantial similarity in API structure
✓ Defendant had access to plaintiff's documentation
✓ Striking similarity suggests copying, not independent creation
✓ Identical naming conventions and parameter orders

Evidence Against Infringement:
✗ API structure dictated by industry standards
✗ Limited ways to implement the functionality
✗ Defendant's implementation code is original
✗ Fair use doctrine may apply

Standard: Preponderance of evidence (>50% likely)

Analysis:
While similarity is clear, functional necessity and fair use
considerations create reasonable doubt about infringement.
Likely outcome: Depends heavily on whether copying was necessary
for interoperability (protected) vs. competitive shortcut (infringement).
```

---

## Medical Diagnosis

### Differential Diagnosis: Abductive + Probabilistic + Evidential Reasoning

**Presenting Symptoms**:
- Chest pain (7/10 severity)
- Shortness of breath
- Sweating
- Radiating to left arm
- 55-year-old male
- History: Hypertension, smoking

**Bayesian Reasoning** (Prior Probabilities):
```python
differential_diagnosis = {
    'myocardial_infarction': {
        'prior_probability': 0.15,  # Base rate for demographics
        'likelihood_given_symptoms': 0.85,  # These symptoms strongly suggest MI
        'urgency': 'CRITICAL',
    },
    'angina': {
        'prior_probability': 0.20,
        'likelihood_given_symptoms': 0.65,
        'urgency': 'High',
    },
    'pulmonary_embolism': {
        'prior_probability': 0.05,
        'likelihood_given_symptoms': 0.40,
        'urgency': 'CRITICAL',
    },
    'anxiety_attack': {
        'prior_probability': 0.30,
        'likelihood_given_symptoms': 0.30,
        'urgency': 'Low',
    },
    'gastroesophageal_reflux': {
        'prior_probability': 0.25,
        'likelihood_given_symptoms': 0.20,
        'urgency': 'Low',
    }
}

# Calculate posterior probabilities
for condition, data in differential_diagnosis.items():
    posterior = (
        data['likelihood_given_symptoms'] * data['prior_probability']
    )
    data['posterior_probability'] = posterior

# Normalize
total = sum(d['posterior_probability'] for d in differential_diagnosis.values())
for data in differential_diagnosis.values():
    data['posterior_probability'] /= total
```

**Clinical Decision-Making** (Risk + Utility Reasoning):
```
Decision Framework:
- Rule out immediately life-threatening conditions first
- Cost of false negative (missing MI) >> Cost of false positive

Actions:
1. IMMEDIATE: ECG, cardiac biomarkers, oxygen (critical conditions)
2. Risk stratification (HEART score, TIMI score)
3. If high risk: Cardiac catheterization
4. If intermediate: Stress test, imaging
5. If low risk: Outpatient follow-up

Reasoning:
Cannot afford to miss MI or PE (potentially fatal).
Must treat as critical until ruled out, even if anxiety
is statistically more common in general population.
Risk-adjusted reasoning prioritizes worst-case scenarios
when stakes are life-and-death.
```

---

## Key Patterns Across Domains

### Common Reasoning Sequences

1. **Problem → Analysis → Solution**
   - Analytical → Decompositional → Synthetic

2. **Hypothesis → Test → Refine**
   - Abductive → Deductive → Evidential → Bayesian

3. **Options → Compare → Decide**
   - Divergent → Comparative → Evaluative → Decisive

4. **System → Diagnose → Fix**
   - Systems → Diagnostic → Causal → Prescriptive

5. **Strategy → Simulate → Execute**
   - Strategic → Scenario → Game-theoretic → Adaptive

### Domain-Specific Emphases

- **Engineering**: Systematic, algorithmic, constraint-based
- **Science**: Inductive, abductive, evidential
- **Business**: Strategic, comparative, optimization
- **Legal**: Analogical, evidential, normative
- **Medicine**: Probabilistic, diagnostic, risk-based
- **Creative**: Divergent, associative, intuitive

Understanding domain conventions helps apply reasoning appropriately and communicate effectively with domain experts.
