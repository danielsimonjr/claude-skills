# Analytical Methodology Skill

Structured analytical frameworks and methodologies for systematic problem-solving and decision-making within Claude DeepThinking MCP reasoning modes.

## What It Does

This skill provides 12 comprehensive analytical frameworks that organize and structure complex problem analysis. Each framework integrates with specific Claude DeepThinking reasoning modes to ensure systematic coverage of problem spaces.

| Capability | Description |
|---|---|
| **Systematic Inquiry** | 5W1H framework for comprehensive problem decomposition |
| **Strategic Analysis** | SWOT analysis with scenario comparison and evidence-based assessment |
| **Root Cause Investigation** | 5 Whys and Fishbone frameworks for multi-level cause analysis |
| **Environmental Scanning** | PESTLE analysis for macro-environmental factor assessment |
| **Change Management** | Force Field and Stakeholder Analysis for organizational initiatives |
| **Decision Support** | Decision Matrix and Cost-Benefit Analysis for multi-criteria evaluation |
| **Prioritization** | Pareto Analysis (80/20 principle) for resource allocation |
| **Risk Management** | Risk Assessment Matrix for probability-impact evaluation |
| **Capability Planning** | Gap Analysis for current-to-desired state bridging |
| **Framework Composition** | Support for combining methodologies sequentially for deeper analysis |

## When to Use

- **User needs structured analysis** — Problem requires systematic decomposition rather than intuitive reasoning
- **Decision-making frameworks required** — Multiple options need objective evaluation against criteria
- **Comprehensive problem coverage needed** — Analysis must address multiple dimensions (causes, stakeholders, risks, opportunities)
- **Organizational change involved** — Initiatives require stakeholder alignment, force assessment, or capability planning
- **Complex trade-offs present** — Decisions involve competing priorities requiring weighted evaluation
- **Root cause identification critical** — Symptoms must be distinguished from underlying causes
- **Strategic planning context** — Long-term planning requires environmental scanning and scenario analysis
- **Risk mitigation needed** — Probability and impact assessment required for decision support

## When NOT to Use

- **Simple, straightforward decisions** — Problems with obvious solutions don't require framework overhead
- **Time-critical situations** — Frameworks are analysis-intensive; quick decisions may need faster approaches
- **Insufficient domain knowledge** — Some frameworks (5 Whys, Root Cause Analysis) depend on questioner expertise
- **Highly complex feedback-loop systems** — Frameworks assume relatively independent factors; complex systems may oversimplify
- **Purely creative/exploratory work** — Frameworks structure analysis; open-ended ideation may feel constraining
- **Single-cause problems** — Problems with one obvious cause don't benefit from multi-factor analysis

## Directory Structure

```
analytical-methology-skill/
├── SKILL.md                    # Skill definition with all 12 frameworks (loaded by Claude Code)
└── examples/
    └── EXAMPLES.md             # Worked examples for each framework
```

## Frameworks Reference

### 1. 5W1H (Systematic Inquiry)

Classical interrogative framework using six questions (Who, What, When, Where, Why, How) to systematically decompose problems and observations.

**When to use:** Problem definition and scoping, incident analysis, hypothesis generation, stakeholder mapping, evidence evaluation.

**Key components:** Who (actors/stakeholders), What (events/specifics), When (timeline/constraints), Where (location/scope), Why (motivations/causes), How (mechanisms/processes)

**Integration:** Shannon Mode (problem definition), Abductive Mode (hypothesis generation), Causal Mode (relationship mapping), Temporal Mode (timeline analysis), Evidential Mode (evidence evaluation)

---

### 2. SWOT Analysis

Strategic planning framework evaluating internal Strengths/Weaknesses (present state) and external Opportunities/Threats (future potential).

**When to use:** Strategic planning, architecture decisions, scenario planning, initiative evaluation.

**Key components:** Internal factors (Strengths/Weaknesses — controllable), External factors (Opportunities/Threats — environmental)

**Integration:** Sequential Mode (structured analysis), Counterfactual Mode (scenario comparison)

---

### 3. Root Cause Analysis (5 Whys)

Iterative interrogative technique exploring cause-and-effect relationships by repeatedly asking "Why?" until the fundamental root cause is identified.

**When to use:** Tracing causal chains, generating deeper hypotheses, identifying system failures. Best for problems with verifiable, traceable causes reachable within 5-7 iterations.

**When NOT to use:** Complex feedback-loop systems, multiple simultaneous root causes, time-critical situations.

**Integration:** Causal Mode (cause-effect analysis), Abductive Mode (hypothesis generation)

---

### 4. Fishbone Diagram (Ishikawa)

Visual tool for categorizing potential causes into structured categories (6Ms for manufacturing, 8Ps for services) to identify root causes systematically.

**When to use:** Comprehensive cause analysis, systematic hypothesis generation, multi-factor problems requiring team brainstorming.

**Category systems:**
- **6Ms (Manufacturing):** Methods, Machines, Materials, Measurements, Man (People), Mother Nature (Environment)
- **8Ps (Services):** Product/Service, Price, Place, Promotion, People, Process, Physical Evidence, Productivity

**Integration:** Causal Mode (cause-effect analysis), Abductive Mode (hypothesis generation)

---

### 5. PESTLE Analysis

Strategic macro-environmental assessment analyzing Political, Economic, Social, Technological, Legal, and Environmental factors impacting organizations.

**When to use:** Strategic planning, market expansion decisions, external risk assessment, scenario planning.

**Key components:** Political (regulatory/governance), Economic (market/financial), Social (demographic/cultural), Technological (innovation/infrastructure), Legal (compliance/regulatory), Environmental (sustainability/ecological)

**Integration:** Sequential Mode (structured analysis), Counterfactual Mode (scenario planning)

---

### 6. Force Field Analysis

Decision-making technique that visualizes driving and restraining forces to assess momentum for organizational change.

**When to use:** Change management, strategic initiatives requiring stakeholder alignment, situations where forces are nearly balanced.

**Key components:** Driving Forces (enablers pushing toward change), Restraining Forces (barriers resisting change), Force Strength scoring (1-5 scale), Net Force calculation

**Integration:** Sequential Mode (structured decision analysis), Counterfactual Mode ("what-if" scenarios)

---

### 7. Decision Matrix Analysis

Structured evaluation of multiple options against weighted criteria for complex trade-off decisions. Also known as Pugh Matrix or Multi-Criteria Decision Analysis (MCDA).

**When to use:** Multi-factor decisions, comparing alternatives systematically, decisions requiring objective scoring across dimensions.

**Process:** (1) List options, (2) Identify criteria + assign weights (1-10), (3) Score each option per criterion (1-10), (4) Calculate weighted scores, (5) Sum and rank, (6) Select

**Integration:** Bayesian Mode (incorporating uncertainty), Sequential Mode (structured analysis)

---

### 8. Pareto Analysis (80/20 Rule)

Statistical technique identifying the vital few causes (20%) that produce most effects (80%), enabling prioritized resource allocation.

**When to use:** Prioritizing issues by impact, identifying high-impact causes, resource allocation decisions, iterative problem-solving.

**Key capabilities:** Categorizes by frequency and cumulative impact; ranks items as "vital," "useful," or "trivial"; generates impact projections

**Integration:** Causal Mode (identifying high-impact causes), Risk Assessment (focusing on high-impact risks)

---

### 9. Stakeholder Analysis

Technique for identifying and analyzing individuals or groups with interest in or influence over a project, decision, or initiative.

**When to use:** Change management, strategic planning, project implementation, processes requiring buy-in and alignment.

**Key dimensions:** Power/Influence, Interest/Impact, Attitude (supportive/neutral/resistant), Role (decision-maker/influencer/implementer/affected)

**Integration:** Game Theory Mode (modeling stakeholder interactions), Causal Mode (mapping influence chains)

---

### 10. Cost-Benefit Analysis

Systematic comparison of total expected costs against total expected benefits to determine project viability and select optimal approaches.

**When to use:** Evaluating project investments, comparing alternative solutions, resource allocation, multi-year project evaluations.

**Key components:** Costs (direct, indirect, opportunity, risk), Benefits (direct, indirect, intangible), Time horizon, Discount rate, Net Present Value (NPV)

**Integration:** Bayesian Mode (incorporating uncertainty with confidence ranges), Counterfactual Mode (comparing scenarios)

---

### 11. Risk Assessment Matrix

Visual tool for assessing and prioritizing risks by plotting probability (likelihood) against impact (severity) to determine risk level.

**When to use:** Project risk management, identifying critical vs. low-priority risks, mitigation planning, regulatory compliance.

**Key components:** Probability scale (1-5: Rare to Almost Certain), Impact scale (1-5: Negligible to Catastrophic), Risk Level (probability x impact), Mitigation strategies per risk level

**Risk levels:** Critical (>15) — immediate action required, High (10-15) — priority mitigation, Medium (5-9) — monitor and plan, Low (<5) — accept or routine monitoring

**Integration:** Bayesian Mode (probabilistic assessment), Sequential Mode (structured evaluation)

---

### 12. Gap Analysis

Framework for identifying the difference between current state and desired future state, then planning actions to bridge the gap.

**When to use:** Capability planning, process improvement, strategic transformation, performance benchmarking.

**Key components:** Current State assessment, Desired State definition, Gap identification (capability/process/resource/knowledge), Action Plan with priorities and timelines

**Integration:** Sequential Mode (structured gap evaluation), Temporal Mode (timeline planning), Counterfactual Mode (scenario comparison)

## Modes vs. Methodologies

The skill distinguishes between two complementary concepts:

- **Reasoning Modes** (e.g., Abductive, Causal, Bayesian): Cognitive approaches that define *how you think*
- **Analytical Methodologies** (e.g., 5W1H, SWOT, Root Cause): Structured frameworks that define *what to ask* and *how to organize* your analysis

Methodologies are templates/checklists that can be used within any reasoning mode to ensure thorough, systematic analysis.

## Framework Composition

Frameworks can be combined sequentially for deeper analysis:

| Combination | Use Case |
|---|---|
| 5W1H → Root Cause Analysis | Define problem scope, then drill into causes |
| SWOT → Decision Matrix | Identify factors, then systematically evaluate options |
| PESTLE → Force Field | Scan environment, then assess change dynamics |
| Stakeholder → Cost-Benefit | Map affected parties, then evaluate financial impact |
| Risk Assessment → Pareto | Identify risks, then prioritize by impact |
| Gap Analysis → Force Field | Identify gaps, then assess forces for/against closing them |

## Usage

The skill triggers automatically in Claude Code when the user needs structured analysis, decision-making frameworks, or comprehensive problem decomposition. It works alongside DeepThinking MCP reasoning modes.

Typical workflow:
1. User describes a problem or decision
2. Claude selects the appropriate framework(s) based on the problem type
3. Framework templates guide systematic analysis
4. Results integrate with DeepThinking MCP reasoning modes for deeper insights
5. Multiple frameworks can be chained for comprehensive coverage
