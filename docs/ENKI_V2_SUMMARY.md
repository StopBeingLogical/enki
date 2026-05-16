# ENKI v2.0 — Executive Summary
## From "Brittle Structuralism" to "Resilient Semantics"

**Date:** April 14, 2026  
**Previous Version:** v1.0-enki (baseline, completed)  
**New Version:** v2.0-scaffold (resilience pass, designed)  
**Status:** Architecture & roadmap complete, ready for implementation

---

## What Changed? (And Why)

### v1.0: The Original Enki
**Strengths:**
- ✅ Three-stage pipeline (decompose → self-assess → analyze)
- ✅ Comprehensive documentation
- ✅ Ready to deploy and use
- ✅ Backward compatible

**Weaknesses (Discovered via Red-Team Critique):**
- ❌ **Measures structure, not substance** (30 useless micro-tasks score perfectly)
- ❌ **One JSON formatting error crashes the entire pipeline** (v1.0 loses Stage 3 data)
- ❌ **Hardcoded timeouts/token limits** fail on heavy models or consumer hardware
- ❌ **Self-assessment is unreliable** (7B models overconfident, 70B models too cautious)
- ❌ **No retry mechanism** (if zero-shot decomposition fails, it's marked "unsuitable" forever)

### v2.0: The Resilience Pass
**What's New:**
- ✅ **LLM-as-a-Judge** (semantic evaluator grades Stage 2 output)
- ✅ **JSON Auto-Repair** (pipeline continues even if formatting fails)
- ✅ **Configurable timeouts & token limits** (works on any hardware)
- ✅ **Multi-tiered scaffolding** (auto-retry with few-shot, CoT if needed)
- ✅ **Failure mode classification** (infrastructure vs. capability)
- ✅ **Backward compatible** (run v2.0 like v1.0 if you want)

**The Core Insight:**
*Most models are actually capable. They just need the right scaffolding or context.*

---

## The Four Major Improvements

### Improvement 1: Semantic Evaluation (Not Just Counting)

**v1.0 Problem:**
```
Output 1: 65 realistic tasks, 2 hours each → Granularity score: 65/100 ✓
Output 2: 30 useless micro-tasks → Granularity score: 100/100 ✗

v1.0 prefers Output 2 (higher score) but Output 1 is semantically superior.
```

**v2.0 Solution:**
```
Evaluator Model (70B+) grades both on:
  - Task relevance (do they match skeleton?)
  - Dependency logic (are dependencies correct?)
  - Estimate realism (are hours reasonable?)
  - Assumption quality

Output 1: Semantic quality = 4.5/5
Output 2: Semantic quality = 1/5

Composite score = (granularity * 0.3) + (semantic * 0.4) + (self-awareness * 0.3)
Output 1 wins. Router trusts it.
```

**Impact:**
- We catch gamified outputs
- Semantic quality is an explicit metric in the registry
- Router gets objective judgment, not just counts

---

### Improvement 2: Decoupled Pipeline (Formatting ≠ Capability)

**v1.0 Problem:**
```
Model outputs valid JSON wrapped in markdown:
  ```json
  {
    "project_title": "...",
    ...
  }
  ```

json.loads() fails → Script crashes
Stage 2 crash → Stage 3 never runs
Result: Marked "unsuitable for decomposition" forever

Actually: The model was fine at decomposition, just bad at formatting.
```

**v2.0 Solution:**
```
New utility: clean_json_output()
  1. Try raw JSON → success? Done.
  2. Strip markdown fences → parse → success? Log repair, continue.
  3. Extract braces → parse → success? Log repair, continue.
  4. All failed? Return None, mark as capability failure.

If cleaning succeeds:
  - Pipeline continues to Stage 3
  - Registry gets: "formatting_issue: markdown_fences"
  - Router knows: "Add output schema to prompt in production"

We keep the Stage 3 self-assessment data.
```

**Impact:**
- Models aren't discarded for minor formatting issues
- Formatting problems are separate from capability problems
- Router has actionable guidance for each issue

---

### Improvement 3: Resilient Infrastructure (Timeouts & Token Limits)

**v1.0 Problem:**
```
Hardcoded:
  - TIMEOUT_SECONDS = 300 (5 minutes)
  - num_predict = (default Ollama limit)

Testing 70B model on CPU offloading → Takes 15 minutes
Timeout fires → Script crashes → Marked "slow/unsuitable"

Actually: Model would have succeeded if we gave it time.
```

**v2.0 Solution:**
```
Configurable parameters:
  --timeout 900          # 15 minutes for heavy models
  --temperature-stage2 0.1  # Deterministic for JSON
  --max-predict 8192     # Explicit token ceiling

All infrastructure issues are logged separately:
  failure_mode: "timeout"
  failure_mode: "context_window_exhaustion"
  failure_mode: "infrastructure_error"

vs. capability_failure (model actually can't do the task)

Router knows: "This model needs more time/memory, not a better model"
```

**Impact:**
- Fair comparison across models and hardware
- Infrastructure issues don't doom a model
- Router can add timeout parameters to task assignment

---

### Improvement 4: Scaffolding Discovery (The Crown Jewel)

**v1.0 Problem:**
```
Gemma 4 26B zero-shot decomposition fails (bad JSON formatting)
→ Marked "unsuitable"
→ Router never uses it
→ Actually: Would work with a few-shot example + explicit schema
```

**v2.0 Solution:**
```
Multi-tiered retry logic:

Level 0 (Zero-Shot): Original v1.0 prompt
  → Success? Done. scaffolding_level = 0
  → Fail? Try Level 1.

Level 1 (Few-Shot + Schema): Add explicit JSON schema + 1-shot example
  → Success? Done. scaffolding_level = 1
  → Fail? Try Level 2.

Level 2 (CoT + Schema): Add "Think step-by-step" + schema + example
  → Success? Done. scaffolding_level = 2
  → Fail? Marked unsuitable.

Registry entry:
  {
    "model": "gemma4:26b",
    "scaffolding": {
      "decomposition_level": 1,  # Needs few-shot + schema
      "formatting_penalty": false,
      "failure_mode": null
    }
  }

Router deployment:
  if model.scaffolding.decomposition_level == 1:
    prepend_few_shot_examples = True
    output_schema = "strict"
  elif model.scaffolding.decomposition_level == 0:
    prepend_few_shot_examples = False
    output_schema = "none"
```

**Impact:**
- Most models are salvageable with the right scaffolding
- v1.0 would discard them; v2.0 catalogs their requirements
- Router can deploy Gemma 4 26B at full capability (not discarded)
- Clear guidance: "Use Gemma 4 26B for decomposition, prepend few-shot"

---

## Metrics: v1.0 vs. v2.0

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Semantic Quality** | Counts tasks (gameable) | LLM-as-a-judge (robust) |
| **Pipeline Resilience** | Crashes on JSON errors | Auto-repairs + continues |
| **Infrastructure Tuning** | Hardcoded | Configurable |
| **Scaffolding** | None | Multi-level retry |
| **Failure Classification** | Generic "failure" | 5 specific modes |
| **Registry Data** | Basic scores | Scaffolding levels + penalties |
| **Router Guidance** | "Use or don't use" | "Use it, prepend schema" |
| **Backward Compatibility** | N/A | 100% compatible |

---

## What's in the v2.0 Package

### Design Documents
1. **ENKI_V2_ARCHITECTURE.md** (comprehensive design)
2. **ENKI_V2_IMPLEMENTATION_ROADMAP.md** (stage-by-stage build plan)
3. **This summary** (executive overview)

### Code Not Yet Written (But Designed)
- `enki/utils/json_repair.py` — JSON cleaning
- `enki/utils/failure_detection.py` — Failure classification
- `enki/utils/scaffolding.py` — Prompt builders (3 levels)
- `enki_stage2b_semantic_evaluator.py` — Evaluator model
- Modified `enki_stage2_decompose.py` — Add scaffolding retries
- Modified `enki_stage3_selfassess.py` — Add timeout tuning
- Modified `enki_stage4_analyze.py` — Semantic scoring
- Test suite + documentation updates

---

## Key Design Decisions

### Decision 1: Evaluator Model is Optional
**Why:** Not all users have access to heavy models or frontier APIs.
**Implementation:** If `--evaluator-model` is not provided, skip semantic scoring and use v1.0 composite algorithm.
**Result:** v2.0 is fully backward compatible.

### Decision 2: Scaffolding is Automatic (Not Manual)
**Why:** We want to discover what each model needs, not let users guess.
**Implementation:** If Level 0 fails, try Level 1. If Level 1 fails, try Level 2. Log the result.
**Result:** Models are automatically profiled, Router gets exact scaffolding requirements.

### Decision 3: Semantic Score Floors Granularity Score
**Why:** A model can't score high overall if it produces semantic garbage.
**Implementation:** `semantic_score` directly reduces `granularity_score` if semantics are bad.
**Result:** Metric gaming is prevented. A model with bad semantics can't hide behind good structure.

### Decision 4: Failure Modes Are Classified, Not Hidden
**Why:** Infrastructure issues (timeout, token exhaustion) look like capability failures if we don't distinguish them.
**Implementation:** Explicit failure classification: timeout, context_window_exhaustion, formatting_error, capability_failure, infrastructure_error.
**Result:** Router knows whether to swap models, increase timeouts, or adjust context.

---

## Implementation Timeline

**Week 1:** Build utilities (json_repair, failure_detection, scaffolding)  
**Week 2:** Refactor core pipeline (stages 2, 3, 4)  
**Week 2-3:** Testing & validation  
**Week 3:** Deploy with v1.0 compatibility, then roll out v2.0 features  

**Estimated effort:** 22-32 hours (can be parallelized)

---

## Success Criteria for v2.0

**Methodological:**
- [ ] Semantic evaluator prevents metric gamification
- [ ] Small weak models don't score higher than large capable models
- [ ] Evaluator judgments are sensible and explainable

**Resilience:**
- [ ] JSON formatting errors don't crash the pipeline
- [ ] Stage 3 runs even if Stage 2 formatting is imperfect
- [ ] Context window exhaustion is detected and logged separately
- [ ] Timeouts are configurable and don't cause false negatives

**Scaffolding:**
- [ ] Models retry with Level 1 (few-shot) if zero-shot fails
- [ ] Models retry with Level 2 (CoT) if Level 1 fails
- [ ] Registry shows which models need scaffolding (level 0, 1, or 2)
- [ ] Router can prepend context based on scaffolding level

**Backward Compatibility:**
- [ ] v1.0 users can upgrade to v2.0 with zero config changes
- [ ] Running v2.0 with `--max-scaffolding-level 0` produces v1.0 behavior
- [ ] Running v2.0 without `--evaluator-model` uses v1.0 scoring

---

## The Big Picture

**v1.0 asked:** "Can this model decompose projects?"  
**Answer:** Yes or no (binary).

**v2.0 asks:**
- "Can this model decompose projects?" (Yes/No, but more accurate)
- "How well is the semantic quality?" (Evaluator judgment)
- "What scaffolding does it need?" (Zero-shot / few-shot / CoT)
- "How aware is it of its limits?" (Confidence calibration)

**Result:** Instead of binary yes/no, Router gets a nuanced profile:
```
Gemma 4 26B:
  - Decomposition: 3.5/5
  - Semantic Quality: 3.8/5 (evaluator)
  - Self-Awareness: 3.2/5
  - Scaffolding Required: Level 1 (few-shot + schema)
  - Formatting Penalty: markdown_fences
  - Suitable? Yes, with caveats
```

**Router deployment:**
```
if model.requires_level_1_scaffolding:
    prepend_few_shot_examples()
    output_schema = "strict"
run_decomposition(model)
```

---

## What's Next?

1. **Read** ENKI_V2_ARCHITECTURE.md (understand the design)
2. **Read** ENKI_V2_IMPLEMENTATION_ROADMAP.md (understand the plan)
3. **Implement** Phase 1 (utilities) using Claude Code
4. **Implement** Phase 2 (core pipeline) using Claude Code
5. **Test** Phase 4 (validation suite)
6. **Deploy** Phase 5 (rollout with backward compatibility)

---

## Summary

**Enki v2.0 transforms the evaluation framework from:**
- Brittle → Resilient
- Structural → Semantic
- Binary → Nuanced
- One-shot → Scaffolded

**While maintaining 100% backward compatibility with v1.0.**

The goal: **Most models are actually capable. We just need to find the right scaffolding and measure their quality accurately.**

---

*v2.0 design complete. Architecture & roadmap ready for implementation. April 14, 2026.*
