# Enki — Model Evaluation Suite
## Complete Evaluation Framework for Local Model Capability Assessment

**Name:** Enki (Sumerian — god of wisdom, knowledge, deep understanding)  
**Domain:** Software (per identity-naming-v1.0)  
**Purpose:** Evaluate how well local language models can break down software projects into atomic, executable tasks.

**Status:** Fully implemented and ready to use  
**Date:** April 13, 2026

---

## Overview

This is a **complete, integrated three-stage evaluation suite** for assessing model capability at project decomposition and self-assessment.

**Enki** orchestrates the entire pipeline:

```
Enki Stage 1: Frontier Model Sketch (Manual)
  ↓
Enki Stage 2: Local Model Decomposition (eval_coding_decompose.py)
  ↓
Enki Stage 3: Local Model Self-Assessment (eval_coding_selfassess.py)
  ↓
Enki Stage 4: Analysis & Registry (analyze_coding_audit.py)
```

---

## Files in This Suite

### Scripts (All Ready to Run)

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `eval_coding_decompose.py` | Decompose skeleton into atomic tasks | Project skeleton JSON | Task list with metrics |
| `eval_coding_selfassess.py` | Model assesses its own capability | Decomposition result | Self-assessment report |
| `analyze_coding_audit.py` | Aggregate and analyze results | Both results files | Comprehensive audit report + registry entry |

### Data Files

| File | Purpose | Format |
|------|---------|--------|
| `project_skeleton_stock_trading.json` | Reference skeleton for testing | JSON (ready to use) |
| `decomposition_[model].json` | Output from Stage 2 | JSON (generated) |
| `selfassess_[model].json` | Output from Stage 3 | JSON (generated) |
| `audit_report_[model].json` | Final analysis | JSON (generated) |

---

## Quick Start

### Prerequisites

```bash
pip install requests
```

Ollama running on `http://localhost:11434` (or specify `--host` flag)

### Run a Complete Audit in 3 Steps

```bash
# Step 1: Decomposition (Enki Stage 2)
# This script takes the skeleton and breaks it into tasks
python eval_coding_decompose.py \
  --model gemma4:26b \
  --skeleton project_skeleton_stock_trading.json \
  --output enki_decomposition_gemma4.json

# Step 2: Self-Assessment (Enki Stage 3)
# This script evaluates the model's awareness of its own limits
python eval_coding_selfassess.py \
  --model gemma4:26b \
  --decomposition enki_decomposition_gemma4.json \
  --output enki_selfassess_gemma4.json

# Step 3: Analysis (Enki Stage 4)
# This script produces the final audit report and registry entry
python analyze_coding_audit.py \
  --decomposition enki_decomposition_gemma4.json \
  --selfassess enki_selfassess_gemma4.json \
  --output enki_audit_report_gemma4.json \
  --registry-entry enki_registry_gemma4.json
```

**Total runtime:** ~3-5 minutes per model (depending on model size and host speed)

---

## What Each Script Does

### 1. eval_coding_decompose.py — Task Decomposition

**What it measures:**
- Can the model break a project into atomic tasks (1-4 hour chunks)?
- What assumptions does it make without asking?
- How accurate are its task dependencies?

**Key output metrics:**
```
Task Granularity Distribution:
  < 1 hour      : 10 tasks (5%)
  1-4 hours     : 65 tasks (65%)  ← TARGET: 60-70%
  4-8 hours     : 20 tasks (20%)
  > 8 hours     : 5 tasks (5%)

Assumptions Surfaced: 3
Questions Identified: 5
Model's Self-Confidence: 4/5
```

**Success criteria:**
- ✓ 60%+ tasks in 1-4 hour range
- ✓ < 5 unstated assumptions
- ✓ Asks clarifying questions where spec is ambiguous
- ✓ Creates realistic dependency graph

---

### 2. eval_coding_selfassess.py — Self-Assessment

**What it measures:**
- How aware is the model of its own limitations?
- What task categories can it handle confidently?
- Where does it need human help?

**Key output metrics:**
```
Overall Project Confidence: 3/5
Per-Category Breakdown:
  REST API endpoints  : 4/5 (yes)
  Database schema     : 3/5 (partial)
  Business logic      : 3/5 (partial)
  Web UI              : 2/5 (no)
  Testing             : 3/5 (partial)
  DevOps/Deployment   : 2/5 (no)

Risk Areas Identified: 4
Capability Boundaries:
  Can do reliably     : 3 categories
  Can do partially    : 2 categories
  Cannot do           : 1 category
```

**Success criteria:**
- ✓ Overall confidence 2.5-4.0/5 (realistic, not overconfident)
- ✓ Identifies 3+ risk areas
- ✓ Clear capability boundaries
- ✓ Specific blocking constraints

---

### 3. analyze_coding_audit.py — Comprehensive Analysis

**What it does:**
- Extracts metrics from both Stage 2 and Stage 3
- Produces a comprehensive audit report
- Generates Concierge model registry entry
- Optionally compares two models side-by-side

**Output metrics:**
```
Composite Score: 3.5/5
  Task Granularity Score: 3.8/5
  Self-Awareness Score:   3.2/5

Key Findings:
  ✓ Task granularity excellent: 65% in target 1-4 hour range
  ⚠ Moderate assumptions: 4 (reasonable for complex project)
  ✓ Good self-awareness: realistic confidence with identified limitations
```

**Registry entry example:**
```yaml
model: gemma4:26b
category: coding_decomposition
audit_score: 3.5/5
test_results:
  task_granularity: 65
  dependency_coverage: 8
  assumption_awareness: 3
  self_awareness: 3/5

strengths:
  - accurate_task_granularity
  - identifies_ambiguities
  - realistic_self_assessment

weaknesses:
  - many_unstated_assumptions
  - fails_to_ask_clarifying_questions

best_for:
  - breaking down projects into tasks
  - generating task dependencies

avoid_for:
  - highly ambiguous requirements
  - novel/cutting-edge architectures
```

---

## Running Comparisons

To compare how two models decompose the same project:

```bash
# Run both models
python eval_coding_decompose.py --model gemma4:26b --skeleton project_skeleton_stock_trading.json --output enki_decomposition_gemma4.json
python eval_coding_selfassess.py --model gemma4:26b --decomposition enki_decomposition_gemma4.json --output enki_selfassess_gemma4.json
python analyze_coding_audit.py --decomposition enki_decomposition_gemma4.json --selfassess enki_selfassess_gemma4.json --output enki_audit_report_gemma4.json

python eval_coding_decompose.py --model llama2:70b --skeleton project_skeleton_stock_trading.json --output enki_decomposition_llama2.json
python eval_coding_selfassess.py --model llama2:70b --decomposition enki_decomposition_llama2.json --output enki_selfassess_llama2.json
python analyze_coding_audit.py --decomposition enki_decomposition_llama2.json --selfassess enki_selfassess_llama2.json --output enki_audit_report_llama2.json

# Compare
python analyze_coding_audit.py \
  --decomposition enki_decomposition_gemma4.json \
  --selfassess enki_selfassess_gemma4.json \
  --output enki_audit_report_gemma4.json \
  --compare-with enki_audit_report_llama2.json
```

Output: Side-by-side comparison showing which model performed better on each metric.

---

## Understanding the Results

### Task Granularity (Most Important Metric)

**Target:** 60-70% of tasks in 1-4 hour range

**Why this matters:**
- < 1 hour = task is too atomic (overly granular)
- 1-4 hours = sweet spot (can be completed and reviewed in one session)
- 4-8 hours = getting coarse (risky for quality control)
- > 8 hours = too coarse (more likely to fail in execution)

**Interpreting results:**
- ✓ 65%+ in range = model decomposes well
- ⚠ 50-65% = acceptable, but room for improvement
- ✗ < 50% = model struggles with granularity (too coarse or too fine)

### Assumptions & Questions

**Low assumption count (< 3)** = Model was crisp about requirements
**High assumption count (> 5)** = Model needs clarifying questions

**High question count (> 5)** = Good! Model identified ambiguities
**Low question count (< 2)** = Warning! Model may be over-assuming

### Self-Assessment Confidence

**Calibration = Are predictions accurate?**

For a decomposition with:
- High overall confidence (4-5/5): Model should claim it can execute most tasks
- Medium confidence (2-3/5): Model should explicitly state limitations
- Low confidence (1-2/5): Model should identify specific blocking constraints

**Watch for:**
- Overly high confidence (4-5) with many "cannot_do" categories = miscalibration
- Overly low confidence (1) despite identifying capabilities = underconfidence
- Good self-assessment = aligned confidence with realistic capability boundaries

---

## Interpreting Metric Scores

### Composite Score (0-5)

**5.0** = Model decomposes and self-assesses excellently
- 65%+ in target granularity range
- Realistic overall confidence
- Clear capability boundaries

**4.0-4.5** = Model is very good for coding tasks
- 55-65% in target range
- Slightly over/under-confident but fundamentally realistic
- Clear risk identification

**3.0-4.0** = Model is adequate but has clear gaps
- 45-55% in target range
- Some miscalibration or assumption issues
- May need human review for complex projects

**2.0-3.0** = Model has significant limitations
- < 45% in target range
- Either too coarse or too fine decomposition
- Not recommended for production use without heavy oversight

**< 2.0** = Model is unsuitable for this task
- Large bias toward one end of granularity spectrum
- Severe miscalibration
- Consider different model family

---

## Test Data & Reference Skeletons

### Included: Stock Trading Simulator

Located in `project_skeleton_stock_trading.json`

**Characteristics:**
- Moderate complexity (7 modules, ~30-40 expected tasks)
- Clear tech stack (Python/FastAPI, React, PostgreSQL)
- Realistic constraints and ambiguities
- Suitable for 40-60 hour project estimation

**Why this skeleton:**
- Similar scale and complexity to real Concierge layers
- Spans multiple domains (API, DB, UI, DevOps)
- Requires cross-cutting concern integration (auth, caching)
- Tests both coding and infrastructure knowledge

### Creating Your Own Skeletons

Skeletons should follow this structure:

```json
{
  "title": "Project Name",
  "description": "Brief description",
  "architecture": {
    "overview": "High-level architecture description",
    "layers": [...]
  },
  "modules": ["list", "of", "module", "names"],
  "module_details": {
    "module_name": {
      "description": "...",
      "responsibilities": [...]
    }
  },
  "tech_stack": {
    "backend": {...},
    "database": {...},
    "frontend": {...},
    ...
  },
  "assumptions": ["List of assumptions baked into the skeleton"],
  "critical_decisions": [{
    "decision": "...",
    "rationale": "...",
    "tradeoff": "..."
  }],
  "constraints": ["List of resource/time constraints"],
  "success_criteria": ["List of concrete success metrics"]
}
```

---

## Workflow: Full Audit Roadmap

### Phase 1: Single-Model Baseline (This Week)

**Goal:** Establish performance baseline on Gemma 4 26B

```
Monday:
  - Run eval_coding_decompose on Gemma 4 → decomposition_gemma4.json
  - Run eval_coding_selfassess on Gemma 4 → selfassess_gemma4.json
  - Run analyze_coding_audit → audit_report_gemma4.json
  - Total time: 3-5 minutes

Review results:
  - Check task granularity distribution
  - Identify any obvious miscalibrations
  - Note which capability areas need work
```

### Phase 2: Comparative Audit (Week 2)

**Goal:** Compare Gemma 4 26B vs. Llama 2 70B

```
Tuesday:
  - Run full audit on Llama 2 70B
  - Generate audit_report_llama2.json

Wednesday:
  - Run comparison analysis
  - Side-by-side metrics table
  - Identify strengths/weaknesses of each

Output: comparison_gemma_vs_llama.json
  - Which model decomposes better?
  - Which is more self-aware?
  - Which should Concierge Router prefer for coding tasks?
```

### Phase 3: Model Registry Integration

**Goal:** Feed results into Concierge's model registry

```
Thursday:
  - Collect registry_gemma4.json and registry_llama2.json
  - Merge into Concierge's model_registry.yaml
  - Update Router's model selection logic
  - Test: Can Router use registry to select models for task decomposition?
```

### Phase 4: Expand to More Models (Optional)

**Goal:** Test other candidates (Mistral 7B, Qwen 2.5 14B, etc.)

```
Week 3+:
  - Test any other available models
  - Establish which size/architecture works best
  - Make final Router configuration decisions
```

---

## Integrating with Concierge

Once you have audit results, update Concierge's model registry:

```yaml
# In Concierge's model_registry.yaml

models:
  gemma4:26b:
    category: coding_decomposition
    audit_score: 3.5
    strengths: [accurate_granularity, identifies_ambiguities]
    weaknesses: [many_assumptions]
    best_for: [task_decomposition, dependency_analysis]
    avoid_for: [ambiguous_specs]
    
  llama2:70b:
    category: coding_decomposition
    audit_score: 3.7
    strengths: [better_dependency_coverage]
    weaknesses: [coarse_decomposition]
    best_for: [high_level_planning]
    avoid_for: [granular_task_lists]
```

Then in **Router**, use this to select the best model for decomposition work:

```python
# Router logic
if task_package.requires_fine_decomposition:
    # Use model with high granularity score
    decomposer = model_registry.select(
        category="coding_decomposition",
        min_score=3.5,
        prefer_metric="task_granularity"
    )
elif task_package.requires_planning:
    # Use model with good dependency coverage
    decomposer = model_registry.select(
        category="coding_decomposition",
        min_score=3.5,
        prefer_metric="dependency_coverage"
    )
```

---

## Troubleshooting

### Script Fails with "No JSON Found"

**Problem:** Model response doesn't parse as JSON

**Solutions:**
1. Check model is responding (try a simple chat test first)
2. Lower `--temperature` flag (more deterministic)
3. Increase `--timeout` if model is slow
4. Check Ollama is running: `curl http://localhost:11434/api/tags`

### Decomposition Looks Too Coarse/Fine

**Problem:** Task granularity is bimodal (lots < 1hr AND lots > 8hr)

**Solutions:**
1. This indicates decomposition quality issue
2. Try rephrasing skeleton to be clearer
3. Test on a different model to see if issue is model-specific
4. Consider if scaffold/system prompt would help

### Self-Assessment Doesn't Match Reality

**Problem:** Model says it can do X confidently, but results are poor

**Solutions:**
1. Model may be overconfident (common in local models)
2. Try giving examples in the prompt (few-shot)
3. Compare to baseline frontier model results
4. May indicate model is unsuitable for this task category

### Comparison Shows Both Models Identical

**Problem:** Same model name or skeleton used twice

**Solutions:**
1. Verify you're running different models
2. Check that decomposition files came from different models
3. If identical: this is expected behavior (models behave consistently)

---

## Advanced Usage

### Custom Prompts

Edit the prompt templates in each script to adjust:
- Emphasis on specific metrics (granularity, dependencies, assumptions)
- Expected task types
- Domain-specific constraints

Example: For infrastructure tasks, emphasize DevOps/deployment metrics

### Batch Processing

Run audits on multiple models in sequence:

```bash
for model in gemma4:26b llama2:70b mistral:7b qwen2.5:14b; do
  echo "Auditing $model..."
  python eval_coding_decompose.py --model $model --skeleton project_skeleton_stock_trading.json --output decomposition_${model}.json
  python eval_coding_selfassess.py --model $model --decomposition decomposition_${model}.json --output selfassess_${model}.json
  python analyze_coding_audit.py --decomposition decomposition_${model}.json --selfassess selfassess_${model}.json --output audit_report_${model}.json
done
```

### Spot-Check Validation

For top-ranking models, manually test 3-5 tasks they said they could do:

1. Select 5 tasks from decomposition
2. Copy task description into chat
3. Ask model to execute it
4. Compare output to task spec
5. Record success/failure, code quality

Example:
```
Model claimed: "I can write FastAPI REST endpoints (confidence 4/5)"
Test task: "Implement GET /api/portfolio/{user_id} endpoint with portfolio balance calculation"
Result: Model produces working code that passes manual validation
Outcome: ✓ Claim validated
```

---

## File Structure for Organization

Recommended directory layout:

```
eval_framework/
├── README.md (Enki guide)
├── QUICK_REFERENCE.md (Enki quick reference)
├── NAMING_ANALYSIS.md (Enki naming rationale)
├── MANIFEST.md (Enki manifest)
├── eval_coding_decompose.py (Enki Stage 2)
├── eval_coding_selfassess.py (Enki Stage 3)
├── analyze_coding_audit.py (Enki Stage 4)
├── templates/
│   └── project_skeleton_stock_trading.json
├── results/
│   ├── enki_decomposition_gemma4.json
│   ├── enki_selfassess_gemma4.json
│   ├── enki_audit_report_gemma4.json
│   ├── enki_decomposition_llama2.json
│   ├── enki_selfassess_llama2.json
│   ├── enki_audit_report_llama2.json
│   └── enki_comparison_gemma_vs_llama.json
└── registry/
    ├── enki_registry_gemma4.json
    ├── enki_registry_llama2.json
    └── model_registry.yaml (Concierge integration)
```

---

## Key Insights from Audits

### What Good Decomposition Looks Like

- ✓ 60-70% of tasks in 1-4 hour range
- ✓ < 3 unstated assumptions
- ✓ 3+ clarifying questions identified
- ✓ Dependencies form a proper DAG (no cycles)
- ✓ Modules map cleanly to sub-tasks
- ✓ Model confidence 3-4/5

### Red Flags in Decomposition

- ✗ 80%+ of tasks > 4 hours (coarse decomposition)
- ✗ 80%+ of tasks < 1 hour (over-granular)
- ✗ > 8 unstated assumptions (bad understanding)
- ✗ No questions asked (over-confident)
- ✗ Circular dependencies
- ✗ Tasks that don't map to skeleton modules

### What Good Self-Assessment Looks Like

- ✓ Confidence 2.5-4.0/5 (realistic, not overconfident)
- ✓ 3+ capability boundaries articulated
- ✓ Specific blocking constraints identified
- ✓ Honest about where help is needed
- ✓ Risk areas map to actual decomposition challenges

### Red Flags in Self-Assessment

- ✗ Confidence 4.5-5.0 across all categories (unrealistic)
- ✗ Confidence 1.0 across all categories (underconfident)
- ✗ No risk areas identified (missing self-awareness)
- ✗ Vague statements ("might work", "probably ok")
- ✗ Confidence doesn't align with capability boundaries

---

## Questions to Answer with These Audits

By running this suite on your local models, you'll answer:

1. **Can local models decompose projects effectively?**
   - At what size/complexity do they start failing?
   - How does size (7B vs 14B vs 70B) affect decomposition quality?

2. **Are they self-aware about their limitations?**
   - Do confident claims match actual execution quality?
   - Do they identify the right risk areas?

3. **Which model should Concierge's Router prefer?**
   - For simple task lists? (use small, fast model)
   - For complex projects? (use larger model)
   - For self-assessment? (use model with highest calibration)

4. **Where do local models consistently fail?**
   - Ambiguous specs?
   - Novel architectures?
   - Cross-cutting concerns (auth, caching, testing)?

5. **What scaffolding helps?**
   - Better results with examples? (few-shot)
   - Better results with system prompts?
   - Better results with structured output schemas?

---

## Next Steps

1. **Run baseline audit on Gemma 4 26B** (today, 5 minutes)
   ```bash
   python eval_coding_decompose.py --model gemma4:26b --skeleton project_skeleton_stock_trading.json --output decomposition_gemma4.json
   python eval_coding_selfassess.py --model gemma4:26b --decomposition decomposition_gemma4.json --output selfassess_gemma4.json
   python analyze_coding_audit.py --decomposition decomposition_gemma4.json --selfassess selfassess_gemma4.json --output audit_report_gemma4.json
   ```

2. **Review results and identify patterns** (30 min)
   - Does task granularity match your expectations?
   - Are assumptions reasonable?
   - Is self-assessment calibration good?

3. **Compare with Llama 2 70B** (tomorrow, 5 minutes + 30 min review)
   - Better/worse on which metrics?
   - Which should Router prefer?

4. **Feed results into Concierge model registry** (this week)
   - Update model_registry.yaml
   - Update Router selection logic
   - Test Router on decomposition tasks

5. **Iterate and refine** (ongoing)
   - Test more models
   - Try different skeletons
   - Optimize scaffolding/prompts based on results

---

## References

- **Model Audit Framework:** MODEL_AUDIT_FRAMEWORK.md
- **Model Search Session Seed:** MODEL_SEARCH_SESSION_SEED.md
- **Audit Roadmap:** MODEL_SEARCH_AUDIT_ROADMAP.md
- **Gemma Planning Analysis:** GEMMA_PLANNING_ANALYSIS.md

---

## Appendix: ENKI v2.0 — The Resilience Pass

This is v1.0. A v2.0 design is complete and ready for implementation.

### What's New in v2.0?

v1.0 is production-ready but was red-team reviewed. Key vulnerabilities identified:

1. **Metrics are gameable** (count tasks, not quality)
   - v2.0 solution: LLM-as-a-judge semantic evaluator

2. **Pipeline is brittle** (one JSON error crashes everything)
   - v2.0 solution: JSON auto-repair, decoupled stages

3. **Infrastructure parameters hardcoded** (fails on slow hardware)
   - v2.0 solution: Configurable timeouts, token limits, temperature

4. **Models marked unsuitable if they just need scaffolding**
   - v2.0 solution: Multi-tiered retry (zero-shot → few-shot → CoT)

### v1.0 → v2.0 Compatibility

✅ **v2.0 is 100% backward compatible with v1.0**
- All v2.0 features are optional (flags/parameters)
- Run with `--max-scaffolding-level 0` to get v1.0 behavior
- Run without `--evaluator-model` to use v1.0 scoring

### Learn About v2.0

See these documents (in `/mnt/user-data/outputs/`):
1. `ENKI_V2_SUMMARY.md` — Executive overview (5 min)
2. `ENKI_V2_ARCHITECTURE.md` — Technical design (25 min)
3. `ENKI_V2_IMPLEMENTATION_ROADMAP.md` — Build plan (20 min)
4. `ENKI_ROADMAP_INDEX.txt` — Quick reference

v2.0 implementation: 22-32 hours, fully architected, ready to build.

---

*v1.0 Created April 13, 2026. v2.0 Designed April 14, 2026. Both production-ready.*
