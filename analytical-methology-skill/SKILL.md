---
name: analytical-methodology
description: Structured analytical frameworks and methodologies (5W1H, SWOT, Root Cause Analysis, Fishbone, PESTLE, Force Field, Decision Matrix, Pareto, Stakeholder, Cost-Benefit, Risk Assessment) for systematic problem-solving. Use when the user needs structured analysis, decision-making frameworks, or comprehensive problem decomposition alongside DeepThinking MCP reasoning modes.
---

# Analytical Methodologies for DeepThinking MCP

This document describes structured analytical frameworks and methodologies that can be applied **within** or **alongside** DeepThinking MCP’s reasoning modes to enhance problem-solving effectiveness.

## Overview

While DeepThinking MCP provides 13 distinct **reasoning modes** (ways of thinking), this guide covers complementary **methodologies** (structured approaches to analysis). These frameworks help organize inquiry, break down problems systematically, and ensure comprehensive analysis.

### Distinction: Modes vs. Methodologies

- **Reasoning Modes** (e.g., Abductive, Causal, Bayesian): Cognitive approaches that define *how you think*
- **Analytical Methodologies** (e.g., 5W1H, SWOT, Root Cause Analysis): Structured frameworks that define *what to ask* and *how to organize* your analysis

Think of methodologies as **templates** or **checklists** that can be used within any reasoning mode to ensure thorough, systematic analysis.

-----

## Table of Contents

1. [5W1H Framework (Systematic Inquiry)](#5w1h-framework-systematic-inquiry)
1. [SWOT Analysis](#swot-analysis)
1. [Root Cause Analysis (5 Whys)](#root-cause-analysis-5-whys)
1. [Fishbone Diagram (Ishikawa)](#fishbone-diagram-ishikawa)
1. [PESTLE Analysis](#pestle-analysis)
1. [Force Field Analysis](#force-field-analysis)
1. [Decision Matrix Analysis](#decision-matrix-analysis)
1. [Pareto Analysis (80/20 Rule)](#pareto-analysis-8020-rule)
1. [Stakeholder Analysis](#stakeholder-analysis)
1. [Cost-Benefit Analysis](#cost-benefit-analysis)
1. [Risk Assessment Matrix](#risk-assessment-matrix)
1. [Gap Analysis](#gap-analysis)

-----

## 5W1H Framework (Systematic Inquiry)

### Also Known As

- Kipling’s Questions
- The Five Ws and How
- Hexadic Framework
- Circumstantial Questions (from classical rhetoric)

### Description

A fundamental interrogative framework that ensures comprehensive understanding by systematically asking six essential questions. Named after Rudyard Kipling’s poem “I Keep Six Honest Serving-Men,” this method originates from classical rhetoric’s *circumstances* (Latin: *Quis, Quid, Quando, Ubi, Cur, Quomodo*).

### The Six Questions

1. **Who?**
- Who is involved?
- Who is affected?
- Who has expertise/authority?
- Who benefits or suffers?
1. **What?**
- What happened/is happening?
- What are the specifics?
- What evidence exists?
- What are the boundaries?
1. **When?**
- When did/does/will it occur?
- What is the timeline?
- What are the temporal constraints?
- When are deadlines?
1. **Where?**
- Where did/does/will it occur?
- What is the location/context?
- Where is it documented?
- Where are the boundaries?
1. **Why?**
- Why did it happen?
- Why does it matter?
- Why these particular circumstances?
- Why now?
1. **How?**
- How did it happen?
- How does the mechanism work?
- How can we verify?
- How do we proceed?

### Application Within DeepThinking Modes

#### In Abductive Mode

Use 5W1H to structure hypothesis generation:

- **Who** observed the phenomenon?
- **What** exactly was observed?
- **When** did the observation occur?
- **Where** was it observed?
- **Why** might this phenomenon occur? (generates hypotheses)
- **How** can we test these hypotheses?

```javascript
{
  "mode": "abductive",
  "observations": [
    {
      "id": "obs1",
      "who": "Production team",
      "what": "System crashes",
      "when": "Daily at 3 AM",
      "where": "Primary database server",
      "confidence": 0.95
    }
  ],
  "hypotheses": [
    {
      "id": "h1",
      "why": "Memory leak in scheduled backup job",
      "how": "Job allocates memory without releasing it",
      "predictions": ["Memory usage should spike before crash"]
    }
  ]
}
```

#### In Causal Mode

Use 5W1H to map causal relationships:

- **Who** are the actors in the system?
- **What** are the cause-effect relationships?
- **When** do causal effects occur?
- **Where** in the system do these relationships exist?
- **Why** do these causal links exist?
- **How** strong are the causal connections?

```javascript
{
  "mode": "causal",
  "causalGraph": {
    "nodes": [
      {
        "id": "marketing",
        "who": "Marketing department",
        "what": "Advertising budget",
        "type": "cause"
      }
    ],
    "edges": [
      {
        "from": "marketing",
        "to": "revenue",
        "how": "Increases brand awareness leading to sales",
        "when": "Effects visible after 2-3 months",
        "strength": 0.7
      }
    ]
  }
}
```

#### In Shannon Mode

Shannon’s Stage 1 (Problem Definition) naturally incorporates 5W1H:

```javascript
{
  "mode": "shannon",
  "stage": "problem_definition",
  "thought": "Defining the optimization problem",
  "problemAnalysis": {
    "who": "E-commerce platform serving 10M users",
    "what": "Page load times exceeding 5 seconds",
    "when": "Peak traffic hours (6-9 PM)",
    "where": "Product listing pages",
    "why": "User experience degradation, lost conversions",
    "how": "Database queries bottleneck under load"
  }
}
```

#### In Temporal Mode

Use 5W1H to establish event contexts:

- **What** events occur?
- **When** do they occur (timestamps)?
- **Where** in the sequence?
- **Who** are the actors?
- **Why** is temporal ordering important?
- **How** do events relate temporally?

#### In Evidential Mode

Apply 5W1H to evidence evaluation:

- **What** is the evidence?
- **Where** did it come from (source)?
- **When** was it collected?
- **Who** collected/reported it?
- **Why** is it relevant?
- **How** reliable is it?

### Best Practices

1. **Start with 5W1H for any new problem** - Before choosing a reasoning mode, use 5W1H to understand the problem space
1. **Don’t skip questions** - Even if a question seems irrelevant, consider it briefly to ensure nothing is missed
1. **Ask iteratively** - Each answer may generate new questions
1. **Combine with other methods** - Use 5W1H as a precursor to more specialized analysis
1. **Document systematically** - Keep track of answers to build a complete picture

### Limitations

- Can feel mechanical or formulaic for simple problems
- May generate excessive detail for straightforward issues
- Requires discipline to avoid superficial answers
- Not all questions are equally important for every problem

-----

## SWOT Analysis

### Description

A strategic planning framework that evaluates **S**trengths, **W**eaknesses, **O**pportunities, and **T**hreats related to a project, business, initiative, or decision.

### Framework Structure

#### Internal Factors (Present State)

- **Strengths**: Internal positive attributes and resources
- **Weaknesses**: Internal negative attributes and limitations

#### External Factors (Future Potential)

- **Opportunities**: External factors that could be advantageous
- **Threats**: External factors that could cause problems

### Application Within DeepThinking Modes

#### In Strategic Analysis

```javascript
{
  "mode": "sequential",
  "thought": "SWOT analysis for microservices migration",
  "swotAnalysis": {
    "strengths": [
      {
        "factor": "Strong DevOps culture",
        "impact": "high",
        "evidence": "99.9% deployment success rate"
      },
      {
        "factor": "Experienced team with distributed systems knowledge",
        "impact": "high"
      }
    ],
    "weaknesses": [
      {
        "factor": "Legacy monolithic codebase with tight coupling",
        "impact": "high",
        "mitigation": "Incremental strangler pattern approach"
      },
      {
        "factor": "Limited observability infrastructure",
        "impact": "medium",
        "mitigation": "Implement distributed tracing first"
      }
    ],
    "opportunities": [
      {
        "factor": "Independent scaling of high-traffic services",
        "benefit": "Cost savings estimated at 30%",
        "timeframe": "6-12 months"
      },
      {
        "factor": "Faster feature deployment cycles",
        "benefit": "Competitive advantage"
      }
    ],
    "threats": [
      {
        "factor": "Increased operational complexity",
        "probability": "high",
        "severity": "medium",
        "mitigation": "Invest in automation and monitoring"
      },
      {
        "factor": "Data consistency challenges",
        "probability": "medium",
        "severity": "high",
        "mitigation": "Implement saga pattern, eventual consistency"
      }
    ]
  }
}
```

#### Combined with Counterfactual Mode

Use SWOT to structure “what-if” scenario analysis:

```javascript
{
  "mode": "counterfactual",
  "actual": {
    "name": "Current monolithic architecture",
    "swot": {
      "strengths": ["Simple deployment", "Easy debugging"],
      "weaknesses": ["Scaling limitations", "Deployment bottlenecks"]
    }
  },
  "counterfactuals": [
    {
      "name": "Microservices architecture",
      "swot": {
        "strengths": ["Independent scaling", "Team autonomy"],
        "weaknesses": ["Operational complexity", "Network overhead"],
        "opportunities": ["Cloud-native benefits", "Technology diversity"],
        "threats": ["Service mesh complexity", "Data consistency"]
      }
    }
  ]
}
```

### Best Practices

1. **Be specific and evidence-based** - Avoid vague statements like “good team”
1. **Prioritize factors** - Not all items are equally important
1. **Consider relationships** - How can strengths address weaknesses? How can opportunities mitigate threats?
1. **Include quantification** - Add metrics, percentages, or magnitudes where possible
1. **Update regularly** - SWOT is a snapshot; revisit periodically
1. **Action-oriented** - Convert insights into strategies and decisions

### Limitations

- Tends to generate lists without prioritization
- Can be subjective without proper evidence
- Doesn’t provide solutions, only highlights factors
- May oversimplify complex situations

-----

## Root Cause Analysis (5 Whys)

### Description

An iterative interrogative technique that explores cause-and-effect relationships by repeatedly asking “Why?” until the fundamental root cause is identified. Developed by Sakichi Toyoda for the Toyota Production System.

### Process

1. **State the problem clearly**
1. **Ask “Why did this happen?”**
1. **When you have an answer, ask “Why?” again**
1. **Repeat 5 times (or until root cause is reached)**
1. **Identify the root cause and implement solutions**

### Application Within DeepThinking Modes

#### In Abductive Mode

Use 5 Whys to generate deeper hypotheses:

```javascript
{
  "mode": "abductive",
  "problem": "Application crashes during peak hours",
  "fiveWhys": [
    {
      "level": 1,
      "question": "Why does the application crash during peak hours?",
      "answer": "The database connection pool is exhausted"
    },
    {
      "level": 2,
      "question": "Why is the connection pool exhausted?",
      "answer": "Connections are not being released properly"
    },
    {
      "level": 3,
      "question": "Why are connections not being released?",
      "answer": "Exception handling doesn't include connection cleanup"
    },
    {
      "level": 4,
      "question": "Why doesn't exception handling include connection cleanup?",
      "answer": "Connection management is scattered across multiple code paths"
    },
    {
      "level": 5,
      "question": "Why is connection management scattered?",
      "answer": "No standardized database access pattern was enforced",
      "rootCause": true,
      "solution": "Implement repository pattern with try-with-resources"
    }
  ]
}
```

#### In Causal Mode

Use 5 Whys to trace causal chains:

```javascript
{
  "mode": "causal",
  "causalChain": {
    "initialEffect": "Customer churn increased by 15%",
    "whyAnalysis": [
      {
        "level": 1,
        "cause": "Support response time increased to 48 hours",
        "mechanism": "direct"
      },
      {
        "level": 2,
        "cause": "Support team was understaffed",
        "mechanism": "direct"
      },
      {
        "level": 3,
        "cause": "Hiring freeze implemented",
        "mechanism": "direct"
      },
      {
        "level": 4,
        "cause": "Revenue projections missed by 20%",
        "mechanism": "indirect"
      },
      {
        "level": 5,
        "cause": "Market conditions changed unexpectedly",
        "mechanism": "indirect",
        "rootCause": true
      }
    ]
  }
}
```

### Best Practices

1. **Focus on processes, not people** - Avoid blame, focus on system failures
1. **Use evidence** - Each “why” answer should be verifiable
1. **Know when to stop** - Sometimes the root cause is found before 5 iterations
1. **Watch for multiple causes** - Problems may have several contributing factors
1. **Document the chain** - Keep track of the entire reasoning path
1. **Verify the root cause** - Test if addressing it would prevent the problem

### Limitations

- May oversimplify complex problems with multiple root causes
- Susceptible to cognitive biases (stopping too early, confirmation bias)
- Relies on questioner’s knowledge and experience
- Not suitable for complex systems with feedback loops
- Can lead to different conclusions depending on who asks the questions

-----

## Fishbone Diagram (Ishikawa)

### Also Known As

- Cause-and-Effect Diagram
- Ishikawa Diagram

### Description

A visual tool for categorizing potential causes of a problem to identify root causes. Developed by Kaoru Ishikawa, it organizes causes into categories (typically 6Ms or 8Ps) radiating from a central “spine.”

### Standard Categories

#### 6Ms (Manufacturing)

1. **Methods** - Processes, procedures, requirements
1. **Machines** - Equipment, tools, technology
1. **Materials** - Raw materials, inputs, components
1. **Measurements** - Inspections, data, metrics
1. **Man** (People) - Personnel, skills, training
1. **Mother Nature** (Environment) - Conditions, location, time

#### 8Ps (Service Industries)

1. **Product/Service** - What is being delivered
1. **Price** - Cost considerations
1. **Place** - Location, distribution
1. **Promotion** - Marketing, awareness
1. **People** - Personnel, skills
1. **Process** - Workflows, procedures
1. **Physical Evidence** - Tangible elements
1. **Productivity** - Efficiency, output

### Application Within DeepThinking Modes

#### In Causal Mode

Structure comprehensive cause analysis:

```javascript
{
  "mode": "causal",
  "problem": "High defect rate in production",
  "fishboneAnalysis": {
    "effect": "15% defect rate (target: 2%)",
    "categories": {
      "methods": [
        {
          "cause": "Inadequate testing procedures",
          "subCauses": [
            "No automated integration tests",
            "Manual testing insufficient for scale"
          ],
          "impact": "high"
        },
        {
          "cause": "Unclear deployment process",
          "subCauses": ["Documentation outdated", "Process varies by team"],
          "impact": "medium"
        }
      ],
      "machines": [
        {
          "cause": "Insufficient test environments",
          "subCauses": [
            "Only 2 staging servers for 5 teams",
            "Test data doesn't match production"
          ],
          "impact": "high"
        }
      ],
      "materials": [
        {
          "cause": "Third-party library vulnerabilities",
          "subCauses": ["Dependencies not regularly updated"],
          "impact": "medium"
        }
      ],
      "measurements": [
        {
          "cause": "No defect tracking metrics",
          "subCauses": ["Can't identify patterns", "No early warning system"],
          "impact": "high"
        }
      ],
      "people": [
        {
          "cause": "High team turnover",
          "subCauses": [
            "Knowledge loss",
            "Onboarding insufficient"
          ],
          "impact": "medium"
        }
      ],
      "environment": [
        {
          "cause": "Tight release deadlines",
          "subCauses": ["Pressure to skip testing", "Technical debt accumulation"],
          "impact": "high"
        }
      ]
    },
    "rootCauseHypothesis": "Combination of inadequate testing procedures (methods) and insufficient test environments (machines) amplified by tight deadlines (environment)"
  }
}
```

#### In Abductive Mode

Use categories to systematically generate hypotheses:

```javascript
{
  "mode": "abductive",
  "observation": "Website conversion rate dropped 40% overnight",
  "categoryHypotheses": {
    "methods": ["Checkout process changed", "Payment gateway updated"],
    "machines": ["Server performance degraded", "CDN issues"],
    "materials": ["Third-party script broke", "API integration failed"],
    "measurements": ["Analytics tracking misconfigured"],
    "people": ["Code deployment error"],
    "environment": ["Browser update incompatibility", "Mobile platform changes"]
  }
}
```

### Best Practices

1. **Start with clear problem statement** - The “effect” must be specific and measurable
1. **Brainstorm causes systematically** - Go through each category methodically
1. **Dig deeper with sub-causes** - Each major cause may have contributing factors
1. **Use visual representation** - Drawing the diagram helps see relationships
1. **Involve diverse perspectives** - Different team members see different causes
1. **Verify with data** - Not all identified causes are actual root causes

### Limitations

- Can become overwhelming with too many causes
- Doesn’t prioritize causes by impact
- Requires facilitation skills for group sessions
- May miss systemic or cultural issues
- Visual format doesn’t translate well to some documentation systems

-----

## PESTLE Analysis

### Description

A strategic framework for analyzing macro-environmental factors that impact organizations, projects, or decisions. Used primarily in strategic planning, market research, and risk assessment.

### Six Factors

1. **Political** - Government policies, regulations, political stability, trade restrictions, tax policy
1. **Economic** - Economic growth, interest rates, inflation, unemployment, exchange rates
1. **Social** - Demographics, cultural attitudes, lifestyle changes, education levels
1. **Technological** - Technological innovation, automation, R&D activity, tech infrastructure
1. **Legal** - Employment law, consumer protection, health & safety, intellectual property
1. **Environmental** - Climate change, sustainability, waste disposal, carbon footprint

### Application Within DeepThinking Modes

#### In Strategic Planning with Sequential Mode

```javascript
{
  "mode": "sequential",
  "thought": "PESTLE analysis for expanding into European market",
  "pestleAnalysis": {
    "political": [
      {
        "factor": "Brexit implications",
        "impact": "high",
        "effect": "negative",
        "details": "Trade barriers with UK, regulatory divergence",
        "mitigation": "Focus on EU27 markets initially"
      },
      {
        "factor": "GDPR compliance requirements",
        "impact": "high",
        "effect": "neutral",
        "details": "Requires significant investment but manageable"
      }
    ],
    "economic": [
      {
        "factor": "Strong Euro",
        "impact": "medium",
        "effect": "positive",
        "details": "Favorable exchange rate for USD operations",
        "timeframe": "short-term"
      },
      {
        "factor": "Rising labor costs",
        "impact": "medium",
        "effect": "negative",
        "details": "Especially in Western Europe"
      }
    ],
    "social": [
      {
        "factor": "Growing digital adoption among seniors",
        "impact": "high",
        "effect": "positive",
        "details": "Expanding addressable market"
      },
      {
        "factor": "Privacy-conscious consumer base",
        "impact": "high",
        "effect": "neutral",
        "details": "Requires privacy-first approach"
      }
    ],
    "technological": [
      {
        "factor": "Advanced 5G infrastructure",
        "impact": "medium",
        "effect": "positive",
        "details": "Enables better mobile experience"
      }
    ],
    "legal": [
      {
        "factor": "DSA/DMA regulations",
        "impact": "high",
        "effect": "negative",
        "details": "Compliance costs, operational restrictions"
      }
    ],
    "environmental": [
      {
        "factor": "EU carbon border adjustment",
        "impact": "low",
        "effect": "negative",
        "details": "May affect supply chain costs"
      }
    ]
  }
}
```

#### Combined with Counterfactual Mode

```javascript
{
  "mode": "counterfactual",
  "actual": {
    "name": "Current market conditions",
    "pestleSnapshot": {
      "political": "Stable",
      "economic": "Growth phase",
      "social": "Pro-technology"
    }
  },
  "counterfactuals": [
    {
      "name": "Economic recession scenario",
      "pestleChanges": {
        "economic": {
          "from": "2% GDP growth",
          "to": "-1% GDP contraction",
          "implications": [
            "Reduced consumer spending",
            "B2B contracts delayed",
            "Investment capital scarce"
          ]
        }
      },
      "adjustedStrategy": "Focus on cost-saving value proposition"
    }
  ]
}
```

### Best Practices

1. **Regular updates** - PESTLE factors change; reassess quarterly or semi-annually
1. **Prioritize factors** - Not all are equally relevant to your context
1. **Quantify impact** - Where possible, use metrics (e.g., “15% tariff increase”)
1. **Consider interactions** - Factors influence each other (e.g., political → legal)
1. **Scenario planning** - Use multiple PESTLE scenarios (optimistic, pessimistic, likely)
1. **Connect to strategy** - Don’t just list factors; derive strategic implications

### Limitations

- External focus only; doesn’t address internal capabilities
- Can generate overwhelming amounts of data
- Factors may overlap between categories
- May miss rapid, unexpected changes
- Effectiveness depends on quality of information sources

-----

## Force Field Analysis

### Description

A decision-making technique developed by Kurt Lewin that visualizes forces for and against a change or decision. Helps identify factors that support or hinder progress toward a goal.

### Components

- **Driving Forces** - Factors pushing toward the desired change (pros, enablers)
- **Restraining Forces** - Factors resisting or blocking the change (cons, barriers)
- **Equilibrium** - Current state maintained by balance of forces
- **Force Strength** - Magnitude/importance of each force (typically 1-5 scale)

### Application Within DeepThinking Modes

#### In Decision Analysis

```javascript
{
  "mode": "sequential",
  "decision": "Migrate from on-premise to cloud infrastructure",
  "forceFieldAnalysis": {
    "currentState": "On-premise data centers",
    "desiredState": "Cloud-native infrastructure",
    "drivingForces": [
      {
        "force": "Scalability requirements",
        "strength": 5,
        "description": "Need to handle 10x traffic growth",
        "stakeholder": "Engineering, Product"
      },
      {
        "force": "Operational cost reduction",
        "strength": 4,
        "description": "30% projected savings on infrastructure",
        "stakeholder": "Finance, Executive"
      },
      {
        "force": "Faster deployment cycles",
        "strength": 4,
        "description": "Enable CI/CD, reduce time-to-market",
        "stakeholder": "Engineering, Product"
      },
      {
        "force": "Global availability",
        "strength": 3,
        "description": "Serve international customers with low latency",
        "stakeholder": "Sales, Product"
      }
    ],
    "restrainingForces": [
      {
        "force": "Migration complexity",
        "strength": 5,
        "description": "200+ legacy applications, 6-12 month effort",
        "stakeholder": "Engineering"
      },
      {
        "force": "Security concerns",
        "strength": 4,
        "description": "Data sovereignty, compliance requirements",
        "stakeholder": "Security, Legal"
      },
      {
        "force": "Team skill gaps",
        "strength": 3,
        "description": "Need to train staff on cloud technologies",
        "stakeholder": "Engineering, HR"
      },
      {
        "force": "Upfront migration costs",
        "strength": 3,
        "description": "$2M investment before cost savings realized",
        "stakeholder": "Finance"
      },
      {
        "force": "Vendor lock-in risk",
        "strength": 2,
        "description": "Concern about dependency on cloud provider",
        "stakeholder": "Architecture, Executive"
      }
    ],
    "netForce": 1,
    "analysis": {
      "drivingTotal": 16,
      "restrainingTotal": 17,
      "assessment": "Forces nearly balanced; slight resistance to change",
      "strategy": "Strengthen driving forces and/or weaken restraining forces"
    },
    "actionItems": [
      {
        "type": "strengthen_driving",
        "action": "Secure executive sponsorship for scalability mandate",
        "targetForce": "Scalability requirements",
        "expectedImpact": "+1 strength"
      },
      {
        "type": "weaken_restraining",
        "action": "Implement multi-cloud strategy to address vendor lock-in",
        "targetForce": "Vendor lock-in risk",
        "expectedImpact": "-1 strength"
      },
      {
        "type": "weaken_restraining",
        "action": "Phase migration approach reduces complexity perception",
        "targetForce": "Migration complexity",
        "expectedImpact": "-2 strength"
      },
      {
        "type": "weaken_restraining",
        "action": "Comprehensive training program addresses skill gaps",
        "targetForce": "Team skill gaps",
        "expectedImpact": "-2 strength"
      }
    ]
  }
}
```

#### Combined with Counterfactual Mode

```javascript
{
  "mode": "counterfactual",
  "scenarios": [
    {
      "name": "Strengthen driving forces strategy",
      "forceFieldChanges": {
        "drivingTotal": 18,
        "restrainingTotal": 17,
        "netForce": 1,
        "outcome": "Slight momentum for change"
      }
    },
    {
      "name": "Weaken restraining forces strategy",
      "forceFieldChanges": {
        "drivingTotal": 16,
        "restrainingTotal": 12,
        "netForce": 4,
        "outcome": "Strong momentum for change - recommended approach"
      }
    }
  ]
}
```

### Best Practices

1. **Involve stakeholders** - Different perspectives reveal hidden forces
1. **Be realistic about force strength** - Avoid wishful thinking
1. **Prioritize actionable forces** - Focus on forces you can influence
1. **Create action plans** - Identify specific ways to strengthen/weaken forces
1. **Reassess after actions** - Update the analysis as conditions change
1. **Consider timing** - Some forces may be stronger/weaker at different times

### Limitations

- Subjective assessment of force strength
- May oversimplify complex organizational dynamics
- Doesn’t address root causes behind forces
- Static snapshot; doesn’t capture dynamic changes
- Can be manipulated to justify predetermined decisions

-----

## Decision Matrix Analysis

### Also Known As

- Pugh Matrix
- Grid Analysis
- Multi-Criteria Decision Analysis (MCDA)

### Description

A structured approach to evaluating multiple options against a set of weighted criteria. Particularly useful when decisions involve multiple factors and complex trade-offs.

### Process

1. **List all options** (alternatives, solutions, choices)
1. **Identify decision criteria** (factors that matter)
1. **Assign weights to criteria** (importance: 1-5 or 1-10)
1. **Score each option** against each criterion (1-5 or 1-10)
1. **Calculate weighted scores** (score × weight)
1. **Sum totals** and compare options

### Application Within DeepThinking Modes

#### In Bayesian Mode

Combine with probabilistic reasoning:

```javascript
{
  "mode": "bayesian",
  "decision": "Select cloud provider for migration",
  "decisionMatrix": {
    "criteria": [
      {
        "id": "cost",
        "name": "Total Cost of Ownership",
        "weight": 8,
        "description": "5-year TCO including infrastructure and operations"
      },
      {
        "id": "performance",
        "name": "Performance & Latency",
        "weight": 7,
        "description": "Compute power, network latency, storage speeds"
      },
      {
        "id": "security",
        "name": "Security & Compliance",
        "weight": 9,
        "description": "Certifications, data sovereignty, security features"
      },
      {
        "id": "ecosystem",
        "name": "Ecosystem & Tools",
        "weight": 6,
        "description": "Available services, integrations, marketplace"
      },
      {
        "id": "support",
        "name": "Support Quality",
        "weight": 5,
        "description": "Technical support, documentation, community"
      },
      {
        "id": "reliability",
        "name": "Reliability & SLA",
        "weight": 8,
        "description": "Uptime guarantees, redundancy, disaster recovery"
      }
    ],
    "options": [
      {
        "id": "aws",
        "name": "Amazon Web Services",
        "scores": {
          "cost": { "score": 6, "weighted": 48, "notes": "Competitive pricing, reserved instance discounts" },
          "performance": { "score": 9, "weighted": 63, "notes": "Excellent performance, global CDN" },
          "security": { "score": 9, "weighted": 81, "notes": "Strong compliance, certifications" },
          "ecosystem": { "score": 10, "weighted": 60, "notes": "Largest ecosystem, most services" },
          "support": { "score": 7, "weighted": 35, "notes": "Good docs, paid support tiers" },
          "reliability": { "score": 9, "weighted": 72, "notes": "99.99% SLA, proven track record" }
        },
        "totalScore": 359,
        "normalizedScore": 8.33
      },
      {
        "id": "azure",
        "name": "Microsoft Azure",
        "scores": {
          "cost": { "score": 7, "weighted": 56, "notes": "Good pricing, hybrid benefits" },
          "performance": { "score": 8, "weighted": 56, "notes": "Strong performance" },
          "security": { "score": 9, "weighted": 81, "notes": "Enterprise security, compliance" },
          "ecosystem": { "score": 8, "weighted": 48, "notes": "Growing ecosystem, Microsoft integration" },
          "support": { "score": 8, "weighted": 40, "notes": "Enterprise support" },
          "reliability": { "score": 8, "weighted": 64, "notes": "99.95% SLA" }
        },
        "totalScore": 345,
        "normalizedScore": 8.01
      },
      {
        "id": "gcp",
        "name": "Google Cloud Platform",
        "scores": {
          "cost": { "score": 8, "weighted": 64, "notes": "Sustained use discounts, competitive" },
          "performance": { "score": 9, "weighted": 63, "notes": "Excellent network, BigQuery performance" },
          "security": { "score": 8, "weighted": 72, "notes": "Good security, improving compliance" },
          "ecosystem": { "score": 7, "weighted": 42, "notes": "Smaller but growing ecosystem" },
          "support": { "score": 6, "weighted": 30, "notes": "Improving but less mature" },
          "reliability": { "score": 8, "weighted": 64, "notes": "99.95% SLA" }
        },
        "totalScore": 335,
        "normalizedScore": 7.78
      }
    ],
    "recommendation": {
      "selected": "aws",
      "reasoning": "Highest total score (359), particularly strong in security (weighted 81), ecosystem (60), and reliability (72)",
      "confidence": 0.85,
      "sensitivity": "Decision is robust - AWS leads even if weights change by ±20%"
    },
    "sensitivityAnalysis": {
      "costDoubled": {
        "awsScore": 407,
        "azureScore": 401,
        "gcpScore": 399,
        "winner": "aws"
      },
      "securityDoubled": {
        "awsScore": 440,
        "azureScore": 426,
        "gcpScore": 407,
        "winner": "aws"
      }
    }
  }
}
```

#### In Sequential Mode

Use for iterative option refinement:

```javascript
{
  "mode": "sequential",
  "thoughtNumber": 1,
  "thought": "Initial decision matrix for database selection",
  "decisionMatrix": {
    "options": ["PostgreSQL", "MongoDB", "DynamoDB"],
    "criteria": ["Performance", "Scalability", "Cost", "Team Expertise"],
    "initialScores": "..."
  },
  "nextThoughtNeeded": true
},
{
  "mode": "sequential",
  "thoughtNumber": 2,
  "thought": "Refining scores based on benchmark results",
  "buildUpon": ["thought1_id"],
  "decisionMatrix": {
    "updatedScores": "...",
    "reasoning": "Actual load testing revealed PostgreSQL performs better than expected"
  }
}
```

### Best Practices

1. **Clear, measurable criteria** - Avoid vague criteria like “quality”
1. **Independent criteria** - Minimize overlap between criteria
1. **Consistent scoring scale** - Use same scale (1-5 or 1-10) throughout
1. **Involve stakeholders in weighting** - Different perspectives on importance
1. **Document scoring rationale** - Explain why each score was assigned
1. **Sensitivity analysis** - Test how results change with different weights
1. **Qualitative overlay** - Numbers don’t tell the whole story

### Limitations

- Can feel overly mechanical for simple decisions
- Scoring subjectivity can bias results
- Assumes criteria independence (often not true)
- Equal score intervals may not reflect real differences
- May ignore intangible factors difficult to quantify

-----

## Pareto Analysis (80/20 Rule)

### Description

A statistical technique based on the Pareto Principle, which states that roughly 80% of effects come from 20% of causes. Used to identify the most significant factors in a set of data.

### Key Concept

Focus effort on the “vital few” rather than the “trivial many” to maximize impact.

### Application Within DeepThinking Modes

#### In Causal Mode

Identify high-impact causes:

```javascript
{
  "mode": "causal",
  "problem": "Customer support ticket volume",
  "paretoAnalysis": {
    "totalTickets": 10000,
    "issueCategories": [
      {
        "category": "Password reset requests",
        "count": 4200,
        "percentage": 42,
        "cumulativePercentage": 42,
        "rank": 1,
        "impactCategory": "vital"
      },
      {
        "category": "Payment processing errors",
        "count": 2100,
        "percentage": 21,
        "cumulativePercentage": 63,
        "rank": 2,
        "impactCategory": "vital"
      },
      {
        "category": "Account activation issues",
        "count": 1500,
        "percentage": 15,
        "cumulativePercentage": 78,
        "rank": 3,
        "impactCategory": "vital"
      },
      {
        "category": "Feature questions",
        "count": 800,
        "percentage": 8,
        "cumulativePercentage": 86,
        "rank": 4,
        "impactCategory": "useful"
      },
      {
        "category": "Billing inquiries",
        "count": 600,
        "percentage": 6,
        "cumulativePercentage": 92,
        "rank": 5,
        "impactCategory": "useful"
      },
      {
        "category": "Other",
        "count": 800,
        "percentage": 8,
        "cumulativePercentage": 100,
        "rank": 6,
        "impactCategory": "trivial"
      }
    ],
    "vitalFew": [
      "Password reset requests",
      "Payment processing errors",
      "Account activation issues"
    ],
    "impact": "These 3 categories (30% of issue types) account for 78% of all tickets",
    "recommendations": [
      {
        "category": "Password reset requests",
        "solution": "Implement self-service password reset with SMS/email",
        "estimatedReduction": "90% reduction (3,780 tickets saved)"
      },
      {
        "category": "Payment processing errors",
        "solution": "Improve payment gateway error handling and user feedback",
        "estimatedReduction": "50% reduction (1,050 tickets saved)"
      },
      {
        "category": "Account activation issues",
        "solution": "Automate activation email retries, clearer instructions",
        "estimatedReduction": "60% reduction (900 tickets saved)"
      }
    ],
    "projectedImpact": "Addressing top 3 categories could reduce overall ticket volume by 57%"
  }
}
```

#### In Abductive Mode

Prioritize hypothesis testing:

```javascript
{
  "mode": "abductive",
  "observation": "Website conversion rate dropped 25%",
  "hypothesesByImpact": [
    {
      "hypothesis": "Checkout page broken on mobile",
      "potentialImpact": "60% of traffic is mobile",
      "estimatedEffect": "15% conversion drop",
      "priorityRank": 1,
      "testEffort": "low"
    },
    {
      "hypothesis": "Payment gateway intermittent failures",
      "potentialImpact": "All payment attempts",
      "estimatedEffect": "8% conversion drop",
      "priorityRank": 2,
      "testEffort": "low"
    },
    {
      "hypothesis": "Price increase not communicated",
      "potentialImpact": "Price-sensitive customers",
      "estimatedEffect": "2% conversion drop",
      "priorityRank": 3,
      "testEffort": "medium"
    }
  ],
  "paretoStrategy": "Test top 2 hypotheses first - likely to explain 23% of 25% drop"
}
```

### Best Practices

1. **Sort data by frequency or impact** - Arrange from highest to lowest
1. **Calculate cumulative percentages** - Track running total
1. **Visualize with Pareto chart** - Bar chart + line graph shows distribution
1. **Apply iteratively** - After addressing top items, repeat analysis
1. **Consider effort vs. impact** - Sometimes #2 item is easier to fix than #1
1. **Don’t ignore the “trivial many”** - They still matter, just prioritize differently

### Limitations

- Assumes causes are independent (often not true)
- 80/20 split is approximate, may be 70/30 or 90/10
- Historical data may not predict future patterns
- Can lead to neglecting important low-frequency issues
- May miss systemic root causes underlying multiple symptoms

-----

## Stakeholder Analysis

### Description

A technique for identifying and analyzing individuals or groups who have an interest in or influence over a project, decision, or initiative. Essential for change management and strategic planning.

### Dimensions Analyzed

1. **Power/Influence** - Ability to affect outcomes
1. **Interest/Impact** - Level of concern or effect on stakeholder
1. **Attitude** - Supportive, neutral, or resistant
1. **Role** - Decision-maker, influencer, implementer, affected party

### Application Within DeepThinking Modes

#### In Game Theory Mode

Model stakeholder interactions:

```javascript
{
  "mode": "gametheory",
  "scenario": "Implementing new performance review system",
  "stakeholderAnalysis": {
    "stakeholders": [
      {
        "id": "executives",
        "name": "Executive Leadership",
        "power": "high",
        "interest": "high",
        "attitude": "supportive",
        "role": "decision-maker",
        "objectives": ["Improve retention", "Data-driven decisions"],
        "concerns": ["Cost", "Implementation disruption"],
        "influence": "Final approval authority",
        "strategy": "Keep satisfied and engaged"
      },
      {
        "id": "managers",
        "name": "Middle Management",
        "power": "medium",
        "interest": "high",
        "attitude": "neutral-resistant",
        "role": "implementer",
        "objectives": ["Manageable workload", "Fair process"],
        "concerns": ["Additional work", "Difficult conversations"],
        "influence": "Can sabotage implementation",
        "strategy": "Involve in design, provide training"
      },
      {
        "id": "employees",
        "name": "Individual Contributors",
        "power": "low-medium",
        "interest": "high",
        "attitude": "skeptical",
        "role": "affected party",
        "objectives": ["Fair evaluation", "Career growth"],
        "concerns": ["Subjectivity", "Negative impact on compensation"],
        "influence": "Collective resistance possible",
        "strategy": "Transparent communication, pilot program"
      },
      {
        "id": "hr",
        "name": "HR Department",
        "power": "medium",
        "interest": "high",
        "attitude": "supportive",
        "role": "implementer",
        "objectives": ["Successful rollout", "Compliance"],
        "concerns": ["Resource availability", "System integration"],
        "influence": "Design and execution",
        "strategy": "Empower as champions"
      },
      {
        "id": "legal",
        "name": "Legal/Compliance",
        "power": "medium",
        "interest": "medium",
        "attitude": "neutral",
        "role": "gatekeeper",
        "objectives": ["Legal compliance", "Risk mitigation"],
        "concerns": ["Discrimination claims", "Documentation"],
        "influence": "Veto power on legal grounds",
        "strategy": "Early involvement, clear guidelines"
      }
    ],
    "powerInterestMatrix": {
      "highPowerHighInterest": ["executives", "managers", "hr"],
      "highPowerLowInterest": [],
      "lowPowerHighInterest": ["employees"],
      "lowPowerLowInterest": ["legal"]
    },
    "engagementStrategies": {
      "executives": "Monthly steering committee, regular updates",
      "managers": "Co-design workshops, early access, dedicated support",
      "employees": "Town halls, FAQ sessions, feedback channels",
      "hr": "Dedicated project team, authority to make decisions",
      "legal": "Compliance review at milestones"
    },
    "risks": [
      {
        "risk": "Manager resistance derails implementation",
        "probability": "medium",
        "mitigation": "Involve managers in design phase"
      },
      {
        "risk": "Employee mistrust reduces participation",
        "probability": "high",
        "mitigation": "Pilot with volunteers, transparent communication"
      }
    ]
  }
}
```

#### In Causal Mode

Map stakeholder influence chains:

```javascript
{
  "mode": "causal",
  "causalGraph": {
    "nodes": [
      { "id": "executives", "type": "actor" },
      { "id": "managers", "type": "actor" },
      { "id": "budget_approval", "type": "decision" },
      { "id": "implementation_quality", "type": "outcome" },
      { "id": "employee_adoption", "type": "outcome" }
    ],
    "edges": [
      {
        "from": "executives",
        "to": "budget_approval",
        "strength": 1.0,
        "mechanism": "direct authority"
      },
      {
        "from": "budget_approval",
        "to": "implementation_quality",
        "strength": 0.8,
        "mechanism": "resources enable quality"
      },
      {
        "from": "managers",
        "to": "employee_adoption",
        "strength": 0.9,
        "mechanism": "managers influence team attitudes"
      },
      {
        "from": "implementation_quality",
        "to": "employee_adoption",
        "strength": 0.7,
        "mechanism": "quality drives acceptance"
      }
    ]
  }
}
```

### Best Practices

1. **Cast a wide net initially** - Better to identify too many than miss key stakeholders
1. **Update regularly** - Stakeholder power and interest shift over time
1. **Consider indirect stakeholders** - Those affected even if not directly involved
1. **Map relationships** - Stakeholders influence each other
1. **Differentiate strategies** - One-size-fits-all doesn’t work
1. **Document assumptions** - Power and attitude assessments are subjective

### Limitations

- Difficult to assess power and influence objectively
- Stakeholder positions may be unclear or hidden
- Dynamic situations require constant reassessment
- May miss informal influencers without formal power
- Can become overly complex with too many stakeholders

-----

## Cost-Benefit Analysis

### Description

A systematic approach to estimating the strengths and weaknesses of alternatives by comparing total expected costs against total expected benefits. Used to determine the best approach or whether a project is worthwhile.

### Components

1. **Costs** - All expenses (direct, indirect, opportunity costs, risks)
1. **Benefits** - All gains (direct, indirect, intangible)
1. **Time horizon** - Period over which costs and benefits are evaluated
1. **Discount rate** - Accounts for time value of money
1. **Net Present Value (NPV)** - Benefits minus costs, adjusted for time

### Application Within DeepThinking Modes

#### In Bayesian Mode

Incorporate uncertainty:

```javascript
{
  "mode": "bayesian",
  "decision": "Implement AI-powered customer support chatbot",
  "costBenefitAnalysis": {
    "timeHorizon": "3 years",
    "discountRate": 0.08,
    "costs": {
      "development": {
        "oneTime": 500000,
        "description": "Custom AI model, integration, testing",
        "confidence": 0.85,
        "range": { "low": 400000, "high": 650000 }
      },
      "implementation": {
        "oneTime": 150000,
        "description": "Training, change management, initial support",
        "confidence": 0.90,
        "range": { "low": 120000, "high": 180000 }
      },
      "operations": {
        "annual": 200000,
        "description": "Maintenance, model updates, hosting",
        "confidence": 0.80,
        "range": { "low": 160000, "high": 250000 }
      },
      "opportunityCost": {
        "oneTime": 100000,
        "description": "Team focus diverted from other initiatives",
        "confidence": 0.60,
        "range": { "low": 50000, "high": 200000 }
      }
    },
    "benefits": {
      "supportCostReduction": {
        "annual": 400000,
        "description": "30% reduction in support staff costs",
        "confidence": 0.75,
        "range": { "low": 300000, "high": 500000 },
        "assumptions": ["Chatbot handles 60% of tier-1 inquiries"]
      },
      "customerSatisfaction": {
        "annual": 150000,
        "description": "24/7 availability, faster response times",
        "confidence": 0.65,
        "range": { "low": 80000, "high": 220000 },
        "metric": "Reduced churn, increased NPS",
        "assumptions": ["5% churn reduction valued at $150k annually"]
      },
      "scalability": {
        "annual": 100000,
        "description": "Support volume growth without proportional cost increase",
        "confidence": 0.70,
        "range": { "low": 50000, "high": 180000 },
        "assumptions": ["Business growth of 20% annually"]
      },
      "dataInsights": {
        "annual": 50000,
        "description": "ML insights into customer issues, product improvements",
        "confidence": 0.50,
        "range": { "low": 0, "high": 100000 },
        "metric": "Hard to quantify"
      }
    },
    "npvCalculation": {
      "year0": {
        "costs": 750000,
        "benefits": 0,
        "netCashFlow": -750000,
        "discountedValue": -750000
      },
      "year1": {
        "costs": 200000,
        "benefits": 700000,
        "netCashFlow": 500000,
        "discountedValue": 462963
      },
      "year2": {
        "costs": 200000,
        "benefits": 700000,
        "netCashFlow": 500000,
        "discountedValue": 428669
      },
      "year3": {
        "costs": 200000,
        "benefits": 700000,
        "netCashFlow": 500000,
        "discountedValue": 396916
      },
      "totalNPV": 538548,
      "roi": 0.72,
      "roiPercentage": "72%",
      "paybackPeriod": "1.5 years"
    },
    "sensitivityAnalysis": {
      "optimistic": {
        "npv": 892000,
        "scenario": "High adoption, low costs"
      },
      "expected": {
        "npv": 538548,
        "scenario": "Base case"
      },
      "pessimistic": {
        "npv": 125000,
        "scenario": "Low adoption, high costs"
      }
    },
    "probabilisticAnalysis": {
      "priorProbability": {
        "projectSuccess": 0.7,
        "justification": "Similar projects in industry have 70% success rate"
      },
      "evidence": [
        {
          "factor": "Experienced AI team",
          "likelihoodGivenSuccess": 0.9,
          "likelihoodGivenFailure": 0.3
        },
        {
          "factor": "Clear requirements",
          "likelihoodGivenSuccess": 0.85,
          "likelihoodGivenFailure": 0.4
        }
      ],
      "posteriorProbability": {
        "projectSuccess": 0.85,
        "calculation": "Bayesian update based on evidence"
      }
    },
    "recommendation": {
      "decision": "Proceed with implementation",
      "reasoning": "Positive NPV ($538k) with 85% probability of success. Even in pessimistic scenario, NPV remains positive ($125k). Strong ROI (72%) with payback in 1.5 years.",
      "conditions": [
        "Secure executive sponsorship",
        "Phase 1 pilot to validate assumptions",
        "Quarterly reviews to reassess benefits realization"
      ]
    }
  }
}
```

#### In Counterfactual Mode

Compare alternative scenarios:

```javascript
{
  "mode": "counterfactual",
  "alternatives": [
    {
      "name": "Build custom AI chatbot",
      "npv": 538548,
      "roi": 0.72,
      "risks": ["Development complexity", "Long timeline"]
    },
    {
      "name": "Purchase off-the-shelf solution",
      "npv": 425000,
      "roi": 0.65,
      "risks": ["Limited customization", "Vendor dependency"]
    },
    {
      "name": "Hire additional support staff",
      "npv": -200000,
      "roi": -0.15,
      "risks": ["Ongoing high costs", "Scaling challenges"]
    },
    {
      "name": "Status quo",
      "npv": 0,
      "roi": 0,
      "risks": ["Competitive disadvantage", "Customer satisfaction decline"]
    }
  ]
}
```

### Best Practices

1. **Include all relevant costs** - Don’t forget indirect, opportunity, and sunk costs
1. **Quantify intangibles** - Attempt to value benefits like brand reputation
1. **Use appropriate discount rate** - Reflects risk and time value of money
1. **Sensitivity analysis** - Test how results change with different assumptions
1. **Monte Carlo simulation** - For complex analyses with many uncertainties
1. **Document assumptions** - Make them explicit and testable
1. **Consider non-financial factors** - Some things can’t be monetized

### Limitations

- Difficulty quantifying intangible benefits (e.g., employee morale)
- Assumption-heavy, especially for long time horizons
- May overlook qualitative strategic considerations
- Can be manipulated by adjusting assumptions
- Doesn’t account for option value (flexibility to change course)
- Ethical concerns may not be captured in monetary terms

-----

## Risk Assessment Matrix

### Description

A visual tool for assessing and prioritizing risks by plotting them on a matrix based on two dimensions: **Probability** (likelihood of occurrence) and **Impact** (severity if it occurs).

### Matrix Structure

|                      |Low Impact |Medium Impact|High Impact  |
|----------------------|-----------|-------------|-------------|
|**High Probability**  |Medium Risk|High Risk    |Critical Risk|
|**Medium Probability**|Low Risk   |Medium Risk  |High Risk    |
|**Low Probability**   |Low Risk   |Low Risk     |Medium Risk  |

### Application Within DeepThinking Modes

#### In Evidential Mode

Incorporate uncertainty and incomplete information:

```javascript
{
  "mode": "evidential",
  "project": "Cloud infrastructure migration",
  "riskAssessment": {
    "risks": [
      {
        "id": "r1",
        "risk": "Data loss during migration",
        "category": "technical",
        "probability": {
          "assessment": "low",
          "numericValue": 0.15,
          "beliefFunction": {
            "low": 0.7,
            "medium": 0.2,
            "high": 0.1
          },
          "evidence": [
            {
              "source": "Historical data",
              "reliability": 0.9,
              "supports": "low probability"
            },
            {
              "source": "Expert assessment",
              "reliability": 0.8,
              "supports": "low probability"
            }
          ]
        },
        "impact": {
          "assessment": "critical",
          "numericValue": 0.95,
          "consequences": [
            "Business disruption",
            "Regulatory penalties",
            "Customer trust damage"
          ],
          "financialImpact": "$2M - $5M"
        },
        "riskLevel": "high",
        "riskScore": 0.14,
        "mitigations": [
          {
            "mitigation": "Multi-stage backup and verification",
            "effectiveness": 0.85,
            "cost": 50000,
            "residualProbability": 0.02
          },
          {
            "mitigation": "Pilot migration with non-critical systems",
            "effectiveness": 0.7,
            "cost": 20000,
            "residualProbability": 0.045
          }
        ],
        "owner": "Infrastructure Lead",
        "status": "Active mitigation"
      },
      {
        "id": "r2",
        "risk": "Team skill gaps delay migration",
        "category": "resource",
        "probability": {
          "assessment": "medium",
          "numericValue": 0.45,
          "beliefFunction": {
            "low": 0.2,
            "medium": 0.6,
            "high": 0.2
          }
        },
        "impact": {
          "assessment": "medium",
          "numericValue": 0.50,
          "consequences": [
            "Timeline extension 2-3 months",
            "Budget overrun 15-20%"
          ],
          "financialImpact": "$150k - $300k"
        },
        "riskLevel": "medium",
        "riskScore": 0.225,
        "mitigations": [
          {
            "mitigation": "Comprehensive training program",
            "effectiveness": 0.6,
            "cost": 40000,
            "residualProbability": 0.18
          },
          {
            "mitigation": "Hire external consultants",
            "effectiveness": 0.8,
            "cost": 120000,
            "residualProbability": 0.09
          }
        ],
        "owner": "Engineering Manager",
        "status": "Training program initiated"
      },
      {
        "id": "r3",
        "risk": "Cost overruns exceed budget by 50%",
        "category": "financial",
        "probability": {
          "assessment": "medium",
          "numericValue": 0.35,
          "beliefFunction": {
            "low": 0.3,
            "medium": 0.5,
            "high": 0.2
          }
        },
        "impact": {
          "assessment": "high",
          "numericValue": 0.80,
          "consequences": [
            "Budget reallocation required",
            "Other projects delayed",
            "Executive scrutiny"
          ],
          "financialImpact": "$500k - $750k"
        },
        "riskLevel": "high",
        "riskScore": 0.28,
        "mitigations": [
          {
            "mitigation": "Phased approach with go/no-go gates",
            "effectiveness": 0.7,
            "cost": 0,
            "residualProbability": 0.105
          },
          {
            "mitigation": "Contingency reserve 20%",
            "effectiveness": 0.5,
            "cost": 200000,
            "residualProbability": 0.175
          }
        ],
        "owner": "Program Manager",
        "status": "Contingency approved"
      },
      {
        "id": "r4",
        "risk": "Security breach due to misconfiguration",
        "category": "security",
        "probability": {
          "assessment": "medium",
          "numericValue": 0.30,
          "beliefFunction": {
            "low": 0.4,
            "medium": 0.4,
            "high": 0.2
          }
        },
        "impact": {
          "assessment": "critical",
          "numericValue": 0.90,
          "consequences": [
            "Data breach",
            "Regulatory fines",
            "Reputation damage",
            "Customer churn"
          ],
          "financialImpact": "$1M - $10M"
        },
        "riskLevel": "critical",
        "riskScore": 0.27,
        "mitigations": [
          {
            "mitigation": "Security audit at each migration phase",
            "effectiveness": 0.75,
            "cost": 80000,
            "residualProbability": 0.075
          },
          {
            "mitigation": "Infrastructure-as-code with security scanning",
            "effectiveness": 0.8,
            "cost": 60000,
            "residualProbability": 0.06
          }
        ],
        "owner": "Security Lead",
        "status": "Active mitigation"
      }
    ],
    "riskMatrix": {
      "critical": ["r1", "r4"],
      "high": ["r3"],
      "medium": ["r2"],
      "low": []
    },
    "overallRiskProfile": {
      "totalRisks": 4,
      "criticalRisks": 2,
      "aggregateRiskScore": 0.935,
      "topRisks": ["r4", "r3", "r1"],
      "mitigationStatus": {
        "fullyMitigated": 0,
        "activeMitigation": 3,
        "planned": 0,
        "accepted": 0
      }
    }
  }
}
```

#### In Bayesian Mode

Update risk assessments with new evidence:

```javascript
{
  "mode": "bayesian",
  "riskUpdate": {
    "risk": "Data loss during migration",
    "prior": {
      "probability": 0.15,
      "basis": "Industry statistics and expert judgment"
    },
    "evidence": {
      "description": "Pilot migration of non-critical system completed successfully",
      "likelihoodGivenRisk": 0.4,
      "likelihoodGivenNoRisk": 0.95
    },
    "posterior": {
      "probability": 0.07,
      "calculation": "Bayesian update reduces probability by more than half",
      "interpretation": "Successful pilot significantly reduces assessed risk"
    },
    "updatedRiskLevel": "medium (downgraded from high)"
  }
}
```

### Best Practices

1. **Use consistent scales** - Define probability and impact scales clearly
1. **Involve diverse perspectives** - Different stakeholders see different risks
1. **Quantify where possible** - Use percentages and dollar amounts
1. **Update regularly** - Risk profiles change as projects progress
1. **Focus on top risks** - Concentrate mitigation efforts on critical/high risks
1. **Document assumptions** - Explain how probability and impact were assessed
1. **Consider risk interdependencies** - Some risks increase probability of others

### Limitations

- Subjective assessments of probability and impact
- Doesn’t capture risk interdependencies well
- Binary thinking (risk happens or doesn’t) vs. partial outcomes
- May miss “unknown unknowns” (unidentified risks)
- Static snapshot; doesn’t show how risks evolve

-----

## Gap Analysis

### Description

A structured comparison between current state and desired future state, identifying the “gaps” that need to be bridged. Used in strategic planning, capability assessment, and process improvement.

### Components

1. **Current State** - Where you are now (as-is)
1. **Desired State** - Where you want to be (to-be)
1. **Gap** - The difference between current and desired
1. **Action Plan** - How to bridge the gap

### Application Within DeepThinking Modes

#### In Sequential Mode

Structured gap closure planning:

```javascript
{
  "mode": "sequential",
  "gapAnalysis": {
    "domain": "AI/ML capabilities for personalization",
    "currentState": {
      "capabilities": [
        {
          "capability": "Basic rule-based recommendations",
          "maturityLevel": 2,
          "description": "Simple if-then rules based on purchase history",
          "limitations": [
            "No learning from user behavior",
            "Limited personalization",
            "Manual rule updates required"
          ]
        },
        {
          "capability": "A/B testing infrastructure",
          "maturityLevel": 3,
          "description": "Can test variants, manual analysis"
        },
        {
          "capability": "Customer data warehouse",
          "maturityLevel": 3,
          "description": "Centralized storage, some analytics"
        }
      ],
      "metrics": {
        "recommendationCTR": "2.5%",
        "personalizationCoverage": "30%",
        "modelUpdateFrequency": "Quarterly"
      },
      "team": {
        "dataScientists": 0,
        "mlEngineers": 1,
        "analyticsEngineers": 2
      }
    },
    "desiredState": {
      "capabilities": [
        {
          "capability": "Real-time ML-powered recommendations",
          "maturityLevel": 4,
          "description": "Personalized recommendations using collaborative filtering and deep learning",
          "requirements": [
            "Real-time inference infrastructure",
            "Automated model retraining",
            "A/B testing integrated with ML pipeline"
          ]
        },
        {
          "capability": "Multi-armed bandit optimization",
          "maturityLevel": 4,
          "description": "Continuous experimentation and optimization"
        },
        {
          "capability": "Feature store",
          "maturityLevel": 4,
          "description": "Centralized feature management and serving"
        }
      ],
      "metrics": {
        "recommendationCTR": "8-10%",
        "personalizationCoverage": "90%",
        "modelUpdateFrequency": "Daily"
      },
      "team": {
        "dataScientists": 3,
        "mlEngineers": 3,
        "analyticsEngineers": 2
      }
    },
    "gaps": [
      {
        "id": "gap1",
        "category": "technology",
        "description": "No real-time ML inference infrastructure",
        "impact": "high",
        "effort": "high",
        "priority": 1,
        "bridgingActions": [
          {
            "action": "Deploy model serving platform (e.g., Seldon, KFServing)",
            "duration": "3 months",
            "dependencies": [],
            "resources": "2 ML engineers, $50k cloud costs"
          },
          {
            "action": "Implement feature store",
            "duration": "2 months",
            "dependencies": ["Model serving platform"],
            "resources": "1 ML engineer, 1 data engineer"
          }
        ]
      },
      {
        "id": "gap2",
        "category": "capability",
        "description": "Lack of deep learning expertise",
        "impact": "high",
        "effort": "medium",
        "priority": 2,
        "bridgingActions": [
          {
            "action": "Hire 2 senior data scientists with deep learning experience",
            "duration": "4-6 months",
            "dependencies": [],
            "resources": "$300k annual compensation"
          },
          {
            "action": "Training program for existing team",
            "duration": "Ongoing, 6 months intensive",
            "dependencies": [],
            "resources": "$40k training budget"
          }
        ]
      },
      {
        "id": "gap3",
        "category": "process",
        "description": "Manual model deployment and monitoring",
        "impact": "medium",
        "effort": "medium",
        "priority": 3,
        "bridgingActions": [
          {
            "action": "Implement MLOps pipeline (CI/CD for ML)",
            "duration": "2 months",
            "dependencies": ["Model serving platform"],
            "resources": "1 ML engineer"
          },
          {
            "action": "Model monitoring and alerting",
            "duration": "1 month",
            "dependencies": ["MLOps pipeline"],
            "resources": "1 ML engineer"
          }
        ]
      },
      {
        "id": "gap4",
        "category": "data",
        "description": "Insufficient feature engineering and data quality",
        "impact": "high",
        "effort": "high",
        "priority": 1,
        "bridgingActions": [
          {
            "action": "Data quality framework and monitoring",
            "duration": "3 months",
            "dependencies": [],
            "resources": "1 analytics engineer, 1 data engineer"
          },
          {
            "action": "Automated feature engineering pipeline",
            "duration": "2 months",
            "dependencies": ["Feature store"],
            "resources": "1 ML engineer, 1 data scientist"
          }
        ]
      }
    ],
    "roadmap": {
      "phase1": {
        "name": "Foundation (Months 1-3)",
        "goals": ["Deploy model serving", "Establish data quality"],
        "gaps": ["gap1", "gap4"],
        "milestones": [
          "Model serving platform operational",
          "Data quality dashboards live"
        ]
      },
      "phase2": {
        "name": "Capability Building (Months 4-6)",
        "goals": ["Hire team", "Implement MLOps"],
        "gaps": ["gap2", "gap3"],
        "milestones": [
          "2 data scientists onboarded",
          "Automated model deployment working"
        ]
      },
      "phase3": {
        "name": "Advanced Features (Months 7-12)",
        "goals": ["Deep learning models", "Real-time personalization"],
        "gaps": [],
        "milestones": [
          "Deep learning recommendation model in production",
          "10% CTR achieved"
        ]
      }
    },
    "estimatedImpact": {
      "revenue": "+$2M annually from improved recommendations",
      "efficiency": "50% reduction in manual model maintenance",
      "customerExperience": "Improved personalization for 90% of users"
    },
    "risks": [
      {
        "risk": "Hiring delays push timeline by 3-6 months",
        "probability": "medium",
        "mitigation": "Start recruiting immediately, consider contractors"
      },
      {
        "risk": "Data quality issues block model performance",
        "probability": "medium",
        "mitigation": "Prioritize data quality framework in Phase 1"
      }
    ]
  }
}
```

### Best Practices

1. **Be specific about states** - Vague goals lead to unclear gaps
1. **Involve stakeholders** - Different perspectives reveal hidden gaps
1. **Prioritize gaps** - Not all gaps are equally important
1. **Consider dependencies** - Some gaps must be closed before others
1. **Realistic timelines** - Account for complexity and resource constraints
1. **Measure progress** - Define KPIs to track gap closure
1. **Iterate** - Gap analysis should be ongoing, not one-time

### Limitations

- Assumes desired state is well-defined (often it’s not)
- May miss innovative approaches by focusing on predefined goal
- Can be time-consuming for large, complex organizations
- Static analysis; doesn’t adapt to changing goals or circumstances
- May overlook cultural or behavioral gaps

-----

## Combining Methodologies

These methodologies are most powerful when used in combination. Here are some effective pairings:

### 5W1H + SWOT

Use 5W1H to thoroughly understand each SWOT element:

- **Strength**: What is it? Why is it a strength? How can we leverage it?
- **Threat**: What is the threat? When might it materialize? How can we mitigate it?

### Root Cause Analysis + Fishbone

Use 5 Whys to drill down within each Fishbone category:

- Start with Fishbone to organize potential causes
- Apply 5 Whys to each major cause to find root causes

### SWOT + Force Field

Convert SWOT insights into Force Field analysis:

- **Strengths** become driving forces
- **Weaknesses** become restraining forces
- **Opportunities** become driving forces
- **Threats** become restraining forces

### Gap Analysis + Decision Matrix

Use Decision Matrix to evaluate alternative paths for closing gaps:

- Each gap closure approach becomes an option
- Criteria: cost, time, effectiveness, risk

### Stakeholder Analysis + Force Field

Map stakeholders onto Force Field:

- Supportive stakeholders → driving forces
- Resistant stakeholders → restraining forces
- Strategy: Increase support, reduce resistance

### Pareto Analysis + Risk Assessment

Apply Pareto principle to risk management:

- Identify vital few risks (80% of impact from 20% of risks)
- Focus mitigation efforts on high-impact, high-probability risks

-----

## Integration with DeepThinking MCP Modes

### Quick Reference: Which Methodology with Which Mode?

|Methodology        |Best DeepThinking Modes                  |Primary Use Case                           |
|-------------------|-----------------------------------------|-------------------------------------------|
|**5W1H**           |All modes (especially Shannon, Abductive)|Problem definition, hypothesis generation  |
|**SWOT**           |Sequential, Counterfactual               |Strategic planning, decision analysis      |
|**5 Whys**         |Abductive, Causal                        |Root cause analysis, debugging             |
|**Fishbone**       |Causal, Abductive                        |Comprehensive cause analysis               |
|**PESTLE**         |Sequential, Temporal                     |Environmental scanning, strategy           |
|**Force Field**    |Sequential, Counterfactual               |Change management, decision support        |
|**Decision Matrix**|Bayesian, Sequential                     |Multi-criteria decisions, option comparison|
|**Pareto**         |Causal, Sequential                       |Prioritization, resource allocation        |
|**Stakeholder**    |Game Theory, Causal                      |Change management, politics                |
|**Cost-Benefit**   |Bayesian, Counterfactual                 |Investment decisions, ROI analysis         |
|**Risk Assessment**|Evidential, Bayesian                     |Risk management, project planning          |
|**Gap Analysis**   |Sequential, Temporal                     |Strategic planning, capability building    |

-----

## Conclusion

These analytical methodologies complement DeepThinking MCP’s reasoning modes by providing structured approaches to organize inquiry, ensure comprehensive analysis, and communicate findings effectively.

**Key Takeaways:**

1. **Methodologies are tools, not rules** - Adapt them to your context
1. **Combine for power** - Multiple methodologies often work better together
1. **Document your process** - Structured approaches improve transparency
1. **Iterate and refine** - Analysis is rarely perfect on the first attempt
1. **Balance rigor with pragmatism** - Don’t let methodology become bureaucracy

Use these frameworks within DeepThinking MCP’s reasoning modes to enhance systematic thinking, improve decision quality, and build stronger arguments backed by structured analysis.

-----

## Further Resources

- **5W1H**: “I Keep Six Honest Serving-Men” by Rudyard Kipling
- **SWOT**: “Strengths, Weaknesses, Opportunities, Threats” - Learned, Christensen, Andrews, Guth (1965)
- **5 Whys**: Toyota Production System documentation
- **Fishbone**: Kaoru Ishikawa, “Guide to Quality Control” (1968)
- **PESTLE**: Originally PEST by Francis Aguilar, “Scanning the Business Environment” (1967)
- **Force Field**: Kurt Lewin, “Field Theory in Social Science” (1951)
- **Decision Matrix**: Stuart Pugh, “Total Design” (1990)
- **Pareto**: Vilfredo Pareto, economic distribution principles
- **Stakeholder Analysis**: R. Edward Freeman, “Strategic Management: A Stakeholder Approach” (1984)

-----

**Document Version**: 1.0  
**Last Updated**: November 19, 2025  
**Maintained by**: Daniel Simon Jr.  
**Repository**: [deepthinking-mcp](https://github.com/danielsimonjr/deepthinking-mcp)