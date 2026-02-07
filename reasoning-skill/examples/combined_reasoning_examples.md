# Combined Reasoning Examples

This file demonstrates how multiple reasoning types work together for complex, real-world problems.

## Example 1: Building a Recommendation System

### Problem Statement
Design and implement a content recommendation system for a streaming platform.

### Multi-Modal Reasoning Approach

#### Phase 1: Requirements Analysis (Analytical + Systems Reasoning)

**Analytical Decomposition**:
```
System Goals:
1. Increase user engagement (watch time)
2. Improve content discovery
3. Reduce churn
4. Balance exploration vs exploitation

Stakeholders:
- Users (want relevant content)
- Content creators (want exposure)
- Business (want metrics improvement)
- Engineering (want maintainability)
```

**Systems Reasoning**:
```
Components:
- User profiling system
- Content metadata system
- Recommendation engine
- A/B testing framework
- Feedback loop (implicit/explicit)

Interactions:
User behavior → Profile updates → Recommendations → User engagement → Profile updates
Content catalog → Metadata extraction → Recommendation eligibility
```

#### Phase 2: Algorithm Selection (Comparative + Quantitative + Evidential Reasoning)

**Comparative Analysis**:
```
Options:
1. Collaborative Filtering
   Pros: Discovers unexpected preferences, no content analysis needed
   Cons: Cold start problem, popularity bias
   
2. Content-Based Filtering
   Pros: No cold start for items, explainable
   Cons: Limited serendipity, requires content analysis
   
3. Hybrid Approach
   Pros: Best of both worlds
   Cons: Increased complexity
   
4. Deep Learning (Neural Collaborative Filtering)
   Pros: Captures complex patterns
   Cons: Computationally expensive, less interpretable
```

**Quantitative Reasoning**:
```python
# Offline evaluation metrics
metrics = {
    'collaborative_filtering': {
        'precision@10': 0.24,
        'recall@10': 0.18,
        'ndcg@10': 0.31,
        'coverage': 0.45,
        'training_time': '2 hours',
        'inference_latency': '50ms'
    },
    'content_based': {
        'precision@10': 0.21,
        'recall@10': 0.22,
        'ndcg@10': 0.28,
        'coverage': 0.85,
        'training_time': '1 hour',
        'inference_latency': '20ms'
    },
    'hybrid': {
        'precision@10': 0.28,
        'recall@10': 0.24,
        'ndcg@10': 0.36,
        'coverage': 0.65,
        'training_time': '3 hours',
        'inference_latency': '70ms'
    }
}

# Decision: Hybrid approach offers best performance
# Acceptable latency for online serving
# Coverage balanced between CF and CB
```

**Evidential Reasoning**:
```
A/B Test Design:
- Control: Current algorithm
- Treatment: Hybrid approach
- Metrics: Engagement rate, watch time, retention
- Duration: 2 weeks
- Sample size: 100K users (power analysis for 3% lift)

Results:
- Engagement: +5.2% (p < 0.001) ✓
- Watch time: +7.8% (p < 0.001) ✓
- Retention: +2.1% (p = 0.03) ✓
- Conclusion: Ship hybrid approach
```

#### Phase 3: Cold Start Problem (Abductive + Creative + Strategic Reasoning)

**Abductive Reasoning** (Why is cold start happening?):
```
Observation: New users get poor recommendations

Possible explanations:
1. Insufficient user data → Most likely
2. Algorithm bias toward popular content
3. Poor default preferences
4. Technical implementation issue

Best explanation: Insufficient data for personalization
```

**Creative Reasoning** (Generating solutions):
```
Brainstormed solutions:
1. Explicit onboarding questionnaire
2. Analyze behavior during free trial
3. Import preferences from connected social accounts
4. Use demographic-based stereotypes (ethical concerns)
5. Offer curated "starter packs" by genre/mood
6. Learn from micro-interactions (hover, scroll)
7. Hybrid of multiple approaches
```

**Strategic Reasoning** (Selecting approach):
```
Evaluation:
- Questionnaire: High friction, but explicit preferences
- Trial behavior: Low friction, but delayed personalization
- Social import: Low friction, but privacy concerns
- Demographic stereotypes: Fast, but may reinforce bias
- Starter packs: Medium friction, editorial control
- Micro-interactions: Low friction, implicit learning

Decision: Combine approaches
- Light questionnaire (3 questions max)
- Curated starter packs based on answers
- Aggressive learning from all interactions
- Gradually transition to full personalization
```

#### Phase 4: Fairness and Ethics (Normative + Critical + Ethical Reasoning)

**Normative Reasoning** (What should we do?):
```
Principles:
1. Don't discriminate based on protected attributes
2. Provide diverse recommendations (filter bubble concern)
3. Respect user privacy
4. Be transparent about personalization
5. Allow user control

Implementation:
- Fair representation in training data
- Diversity injection in recommendations
- Privacy-preserving techniques (federated learning)
- Explainability features
- User controls for personalization level
```

**Critical Reasoning** (Evaluating trade-offs):
```
Tension: Engagement vs Diversity

Pure engagement optimization:
+ Maximizes watch time
- May create filter bubbles
- Reduces content discovery
- Potential ethical concerns

Diversity-aware optimization:
+ Broader content discovery
+ Reduces filter bubbles
+ Ethical benefits
- May reduce short-term engagement

Resolution: Multi-objective optimization
- Primary: Engagement (weight: 0.7)
- Secondary: Diversity (weight: 0.2)
- Secondary: Fairness (weight: 0.1)
```

#### Phase 5: System Design (Systems + Constraint-Based + Optimization Reasoning)

**Systems Architecture**:
```
Online Path (Real-time, <100ms):
User Request → Cache Check → 
→ Quick Scoring (pre-computed candidates) → 
→ Re-ranking → 
→ Response

Offline Path (Batch, daily):
User Data → Model Training → 
→ Candidate Generation → 
→ Feature Computation → 
→ Cache Population

Feedback Loop:
User Interactions → Event Stream → 
→ Profile Updates → 
→ Model Retraining Trigger
```

**Constraint-Based Reasoning**:
```
Constraints:
- Latency: p95 < 100ms
- Throughput: 10K requests/second
- Cost: < $0.10 per user/month
- Storage: Distributed, redundant
- Privacy: No PII in training data

Design decisions driven by constraints:
- Pre-compute candidates offline (latency)
- Use caching aggressively (latency + cost)
- Two-stage ranking (latency)
- Sample user interactions (cost)
- Federated learning (privacy)
```

**Optimization Reasoning**:
```python
# Optimize for latency-cost trade-off

def optimize_cache_strategy():
    """
    Decision: How many recommendations to pre-compute?
    """
    options = {
        'aggressive': {
            'precompute': 'Top 1000 per user',
            'cache_hit_rate': 0.95,
            'latency_p95': 45,  # ms
            'storage_cost': 15000,  # $/month
        },
        'moderate': {
            'precompute': 'Top 100 per user',
            'cache_hit_rate': 0.75,
            'latency_p95': 72,  # ms
            'storage_cost': 3000,  # $/month
        },
        'minimal': {
            'precompute': 'Top 20 per user',
            'cache_hit_rate': 0.40,
            'latency_p95': 98,  # ms
            'storage_cost': 800,  # $/month
        }
    }
    
    # Optimize: Meet latency constraint at minimum cost
    # Decision: Moderate caching
    # Rationale: Meets p95 < 100ms at 1/5 cost of aggressive
```

---

## Example 2: Investigating Production Incident

### Incident: E-commerce Checkout Failure Spike

#### Phase 1: Initial Response (Diagnostic + Heuristic Reasoning)

**Heuristic Triage** (Fast pattern matching):
```
Symptoms:
- Checkout completion rate dropped from 68% to 12%
- Started at 14:23 UTC
- Error rate spiking on payment service
- No recent deployments

Quick checks:
✓ Payment provider status page: All systems operational
✓ Database connections: Normal
✓ Server resources: Normal
✗ Payment service response time: 50x slower than baseline

Initial hypothesis: Payment service degradation
Priority: P0 - Revenue impacting
```

#### Phase 2: Root Cause Analysis (Systematic + Decompositional + Causal Reasoning)

**Systematic Investigation**:
```
Timeline reconstruction:
14:00 - Normal operation
14:20 - Traffic spike begins (+300%)
14:23 - Payment timeouts start
14:25 - Cascading failures to checkout service
14:30 - Incident detected, team alerted

Decomposition by layer:
1. Client-side: No issues detected
2. Load balancer: Evenly distributing traffic
3. Application servers: High CPU but responsive
4. Payment service: High latency, connection pool exhaustion
5. Database: Query patterns normal
6. External APIs: Payment provider responding normally
```

**Causal Chain**:
```
Root Cause Analysis (5 Whys):

1. Why did checkouts fail?
   → Payment service timeouts

2. Why did payment service timeout?
   → Connection pool exhausted

3. Why was connection pool exhausted?
   → Each request holding connections 50x longer

4. Why were requests taking 50x longer?
   → External API calls to fraud detection service timing out

5. Why were fraud detection calls timing out?
   → No timeout configuration + fraud service degradation

Root Cause: Missing timeout configuration caused request backlog
when fraud detection service degraded, exhausting connection pool.
```

#### Phase 3: Immediate Mitigation (Pragmatic + Strategic Reasoning)

**Pragmatic Decision-Making**:
```
Options for immediate mitigation:
1. Restart payment service (clears connections)
2. Scale payment service (more connection capacity)
3. Disable fraud checks temporarily
4. Add aggressive timeouts

Trade-off analysis:
- Restart: Fast but brief outage (30s)
- Scale: Safe but slow (5-10 min)
- Disable fraud: Fast but risky (fraud exposure)
- Add timeouts: Safe but requires deployment

Decision: Combination approach
1. Add aggressive timeout (30s) via configuration reload (1 min)
2. Scale up payment service 3x (5 min)
3. Monitor fraud detection service recovery

Reasoning: Minimize downtime while maintaining fraud protection
```

**Strategic Mitigation**:
```
Short-term (next hour):
- Monitor recovery
- Prepare rollback plan
- Communication to stakeholders

Medium-term (next day):
- Add circuit breakers
- Implement timeout defaults
- Add fallback fraud detection

Long-term (next sprint):
- Implement rate limiting
- Add load shedding
- Improve observability
- Chaos engineering testing
```

#### Phase 4: Post-Mortem Analysis (Critical + Evidential + Meta-Reasoning)

**Critical Analysis**:
```
What went wrong:
1. System design: No timeout defaults
2. Dependency management: Tight coupling to fraud service
3. Monitoring: Didn't alert on latency increase
4. Load testing: Didn't test failure modes

What went right:
1. Detection: Caught within 7 minutes
2. Response: Team mobilized quickly
3. Communication: Clear incident updates
4. Mitigation: Successful within 15 minutes
```

**Evidential Documentation**:
```
Metrics evidence:
- Checkout rate: 68% → 12% → 65% (post-mitigation)
- Payment latency: 120ms → 6000ms → 180ms
- Connection pool: 50/100 → 100/100 → 40/100
- Revenue impact: ~$47K (estimated)

Timeline evidence:
[Detailed timeline with logs, metrics, actions]

Root cause verification:
- Added timeouts → Latency improved
- Fraud service recovered → Full restoration
- Reproduced in staging → Confirms hypothesis
```

**Meta-Reasoning** (Learning from incident):
```
Process improvements:
1. Add timeout defaults to all external calls
2. Implement circuit breakers for all dependencies
3. Add synthetic testing of failure modes
4. Improve runbook for payment service issues
5. Add alerting on p99 latency increases

Knowledge captured:
- Document failure mode in architecture docs
- Add to on-call training materials
- Create chaos test for similar scenario
- Update deployment checklist

Systemic thinking:
This wasn't a single failure but a system design issue.
Missing defensive programming (timeouts, circuit breakers)
turned partial degradation into complete outage.
```

---

## Example 3: Data Science Project - Customer Churn Prediction

### Full Lifecycle with Multi-Modal Reasoning

#### Phase 1: Problem Framing (Abductive + Strategic + Domain-Specific Reasoning)

**Abductive Problem Definition**:
```
Business observation: Churn rate increased from 5% to 8% monthly

Possible explanations:
1. Product quality issues
2. Competitive pressure
3. Price sensitivity
4. Poor onboarding
5. Lack of feature engagement

Hypothesis: Can we predict churn early and intervene?

ML Framing: Binary classification problem
- Target: Will customer churn in next 30 days?
- Use case: Proactive retention campaigns
```

**Strategic Reasoning**:
```
Project value:
- Current churn: 8% of 100K customers = 8K/month
- Average LTV lost: $1,200
- Monthly impact: $9.6M
- If model prevents 20% of churn: $1.92M/month

Investment:
- DS team: 2 engineers × 2 months = $80K
- Infrastructure: $10K/month
- Campaign costs: $50/customer contacted

ROI analysis:
- Break-even: If model achieves >5% precision at 20% recall
- Expected value: Positive with moderate performance
- Decision: Proceed with project
```

#### Phase 2: Data Exploration (Inductive + Statistical + Visual Reasoning)

**Inductive Pattern Discovery**:
```python
# Statistical exploration
churn_analysis = {
    'overall_churn_rate': 0.08,
    
    'by_subscription_age': {
        '<30_days': 0.22,    # New users at highest risk
        '30-90_days': 0.12,  # Critical period
        '90-180_days': 0.06,
        '>180_days': 0.03    # Established users stable
    },
    
    'by_engagement': {
        'low_usage': 0.18,   # Strong predictor
        'med_usage': 0.06,
        'high_usage': 0.02
    },
    
    'by_support_tickets': {
        '0_tickets': 0.06,
        '1-2_tickets': 0.09,
        '3+_tickets': 0.25   # Frustrated users
    }
}

# Inductive generalization:
# "Users with low engagement + support issues + early lifecycle
#  have very high churn probability"
```

**Visual Reasoning**:
```
Key visualizations:
1. Survival curves by user segment
   → Shows divergence around day 45
   
2. Feature correlation heatmap
   → Last login days highly correlated with churn
   
3. Decision tree visualization (simple model)
   → Most important splits: days_since_login, support_tickets
   
4. Confusion matrix from baseline model
   → High false positive rate needs addressing
```

#### Phase 3: Feature Engineering (Creative + Domain-Specific + Analytical Reasoning)

**Creative Feature Generation**:
```python
def engineer_features(customer_data):
    features = {}
    
    # Temporal features (temporal reasoning)
    features['days_since_last_login'] = (
        today - customer_data['last_login']
    ).days
    features['login_frequency_trend'] = calculate_trend(
        customer_data['login_history']
    )
    
    # Engagement features (analytical reasoning)
    features['feature_adoption_rate'] = (
        customer_data['features_used'] / 
        customer_data['features_available']
    )
    features['engagement_velocity'] = (
        recent_usage - early_usage
    ) / subscription_age
    
    # Interaction features (creative reasoning)
    features['value_engagement_score'] = (
        customer_data['features_used'] * 
        customer_data['login_frequency'] *
        customer_data['session_duration']
    )
    
    # Behavioral change features (temporal + statistical reasoning)
    features['usage_dropped_suddenly'] = detect_changepoint(
        customer_data['daily_usage']
    )
    
    # Contextual features (domain-specific reasoning)
    features['in_critical_period'] = is_between_days(
        customer_data['account_age'], 30, 90
    )
    
    return features
```

#### Phase 4: Model Development (Comparative + Mathematical + Evidential Reasoning)

**Comparative Model Selection**:
```
Models evaluated:
1. Logistic Regression (baseline)
2. Random Forest
3. Gradient Boosting (XGBoost)
4. Neural Network

Cross-validation results (5-fold):
                   Precision  Recall  F1     AUC    Train Time
Logistic Reg       0.42       0.65    0.51   0.82   2 min
Random Forest      0.48       0.71    0.57   0.86   15 min
XGBoost           0.52       0.73    0.61   0.89   8 min
Neural Net         0.51       0.69    0.59   0.88   30 min

Decision: XGBoost
Reasoning:
- Best overall performance (F1, AUC)
- Reasonable training time
- Built-in feature importance
- Handles imbalanced data well
```

**Mathematical Threshold Optimization**:
```python
# Optimize threshold for business objective
# Cost of false positive: $50 (campaign cost)
# Cost of false negative: $1,200 (lost LTV)

def expected_value(threshold, fpr, tpr, n_customers=8000):
    """
    Calculate expected value at different thresholds
    """
    TP = n_customers * tpr * churn_rate
    FP = n_customers * fpr * (1 - churn_rate)
    FN = n_customers * (1 - tpr) * churn_rate
    TN = n_customers * (1 - fpr) * (1 - churn_rate)
    
    # Value calculation
    value = (
        TP * (0.20 * 1200 - 50) +  # Saved customers minus campaign cost
        FP * (-50) +                 # Wasted campaign costs
        FN * (-1200) +               # Lost customers
        TN * 0                       # True negatives cost nothing
    )
    
    return value

# Optimize threshold
optimal_threshold = optimize_threshold(
    objective=expected_value,
    constraints=[precision >= 0.40]  # Don't spam users
)
# Result: threshold = 0.35 (default was 0.50)
```

#### Phase 5: Deployment and Monitoring (Systems + Pragmatic + Adaptive Reasoning)

**Systems Integration**:
```
Architecture:
1. Batch scoring pipeline (daily)
   - Pull customer data
   - Engineer features
   - Score all active users
   - Write to churn prediction table

2. Campaign trigger system
   - Query high-risk users (score > threshold)
   - Filter by intervention eligibility
   - Trigger retention campaigns
   - Track outcomes

3. Feedback loop
   - Collect actual churn outcomes
   - Compare to predictions
   - Retrain model monthly
   - Update feature engineering
```

**Adaptive Monitoring**:
```
Model monitoring:
1. Performance drift
   - Track precision/recall over time
   - Alert if F1 drops >5%
   
2. Feature drift
   - Monitor feature distributions
   - Alert if significant shift
   
3. Prediction drift
   - Track score distribution
   - Alert if median shifts >10%
   
4. Business impact
   - Track actual vs predicted churn
   - Measure retention campaign ROI
   - A/B test: Contacted vs not contacted

Adaptive response:
- Drift detected → Trigger retraining
- Performance degradation → Investigate root cause
- Campaign ineffective → Revisit intervention strategy
```

---

## Key Takeaways from Combined Reasoning

### 1. Complex Problems Require Multiple Reasoning Types

No single reasoning type suffices for real-world problems. The examples above used:

**Recommendation System**: 10+ reasoning types
- Analytical, Systems, Comparative, Quantitative, Evidential, Abductive, Creative, Strategic, Normative, Critical, Constraint-based, Optimization

**Incident Response**: 8+ reasoning types
- Diagnostic, Heuristic, Systematic, Decompositional, Causal, Pragmatic, Strategic, Critical, Evidential, Meta-reasoning

**Data Science Project**: 12+ reasoning types
- Abductive, Strategic, Domain-specific, Inductive, Statistical, Visual, Creative, Analytical, Comparative, Mathematical, Evidential, Systems, Pragmatic, Adaptive

### 2. Reasoning Types Are Applied in Sequences

Notice the phased approach in each example:
1. **Understanding phase** (Analytical, Diagnostic, Abductive)
2. **Option generation phase** (Divergent, Creative, Comparative)
3. **Evaluation phase** (Evidential, Critical, Quantitative)
4. **Decision phase** (Strategic, Pragmatic, Economic)
5. **Implementation phase** (Systems, Systematic, Pragmatic)
6. **Learning phase** (Meta-reasoning, Adaptive, Reflective)

### 3. Context Determines Emphasis

Different contexts emphasize different reasoning:
- **Emergency incidents**: Heuristic → Diagnostic → Pragmatic (speed matters)
- **Strategic decisions**: Analytical → Comparative → Game-theoretic (thoroughness matters)
- **Scientific problems**: Abductive → Deductive → Evidential (rigor matters)

### 4. Iteration Is Essential

All examples showed iteration:
- Recommendation system: Evaluate → Deploy → Monitor → Improve
- Incident response: Diagnose → Mitigate → Analyze → Prevent
- Data science: Explore → Model → Deploy → Monitor → Retrain

### 5. Meta-Reasoning Enables Learning

Each example concluded with reflection:
- What reasoning worked well?
- What should we do differently next time?
- What patterns can we extract?
- How do we improve our reasoning process?

## Practice Exercise: Your Turn

**Scenario**: Design a fraud detection system for a fintech company

Apply multi-modal reasoning:
1. **Problem framing** (What reasoning types?)
2. **Data analysis** (What reasoning types?)
3. **Algorithm selection** (What reasoning types?)
4. **System design** (What reasoning types?)
5. **Deployment** (What reasoning types?)

Try to identify 8-10 distinct reasoning types you would use and explain why each is appropriate for its phase.

**Hint**: Consider the phases in the examples above as a template, but adapt to the fraud detection context.

---

## Conclusion

Mastering combined reasoning means:
- **Knowing** which reasoning types exist
- **Recognizing** when each is appropriate
- **Applying** them in effective sequences
- **Integrating** insights from multiple modes
- **Reflecting** on reasoning quality
- **Adapting** based on feedback

Real-world expertise comes from fluency in switching between reasoning modes and combining them effectively for complex problems.
