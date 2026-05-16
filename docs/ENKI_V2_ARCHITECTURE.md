# ENKI v2.0 Architecture Design
## "Scaffolding & Resilience" — Addressing v1.0 Vulnerabilities

**Date:** April 14, 2026  
**Status:** Design Document (Implementation Ready)  
**Previous Version:** v1.0-enki (basic pipeline)  
**New Version:** v2.0-scaffold (resilience + semantic evaluation)

---

## Executive Summary

Enki v2.0 shifts from a **brittle, structural-only** evaluation framework to a **resilient, semantically-aware** system that:

1. **Separates formatting from capability** (JSON crashes don't kill the pipeline)
2. **Measures semantic quality, not just structure** (evaluator model as judge)
3. **Discovers required scaffolding** (auto-retry with CoT/few-shot/schema)
4. **Provides actionable Router guidance** (scaffolding_level_required in registry)

---

## Part 1: Red-Team Critique of v1.0

### Vulnerability 1A: The Self-Assessment Paradox
**Problem:**
- Small/weak models (7B) exhibit Dunning-Kruger: produce garbage but rate confidence 4-5/5
- Large/aligned models (70B) are cautious: excellent output but rate confidence 2-3/5
- v1.0 composite score favors confident incompetence over cautious excellence

**Current Impact:**
- Router might prefer a 7B model with inflated confidence over a 70B model with realistic caution
- Stage 3 (Self-Assessment) is **not a corrective mechanism** — it amplifies bias

**v2.0 Solution:**
- Introduce **Evaluator Model** (external judge) to validate Stage 2 output semantically
- Evaluator score factors directly into composite, overriding model's self-rating
- Stage 3 becomes a **calibration diagnostic** rather than a score input

---

### Vulnerability 1B: Metric Gamification (Shape vs. Substance)
**Problem:**
- Task granularity is purely **structural**: count tasks in 1-4 hour bucket
- A model can game this: output 30 useless micro-tasks (2 hours each)
- Achieves 100% "granularity score" with semantically worthless decomposition

**Current Impact:**
- We measure the *shape* of decomposition, not the *substance*
- Metrics are easy to fake; we don't detect nonsense outputs

**v2.0 Solution:**
- Evaluator Model grades decomposition on **semantic meaningfulness** (1-5)
- Evaluator checks: Do tasks map to skeleton modules? Are dependencies logical? Are estimates realistic?
- Semantic score floors the granularity score (if semantics=1, granularity is capped at 2, regardless of bucket counts)

---

### Vulnerability 2A: The Strict JSON Domino Effect
**Problem:**
- Model outputs valid JSON wrapped in markdown: ```json {...}```
- `json.loads()` fails, script crashes
- v1.0 conflates **formatting failure** (minor) with **capability failure** (major)
- Stage 3 never runs; we lose self-assessment data

**Current Impact:**
- Models that fail JSON formatting are marked "unsuitable for decomposition"
- We discard Stage 3 calibration that might reveal the model is actually good at task design

**v2.0 Solution:**
- Implement `clean_json_output()` utility:
  - Strip markdown fences (`\`\`\`json ... \`\`\``)
  - Remove leading/trailing junk
  - Repair common escaping issues
- If cleaning succeeds, pipeline continues; log a **"Strict Formatting Penalty"** in registry
- Stage 3 runs regardless; we capture self-assessment data
- Router knows: "This model is good at decomposition but needs strict output schema to format correctly"

---

### Vulnerability 2B: Context Window Exhaustion (Silent Truncation)
**Problem:**
- Large skeletons → large JSON outputs (deeply nested modules, many tasks)
- Ollama's default `num_predict` limit cuts off mid-generation
- Result: truncated, unparseable JSON
- v1.0 logs this as **"instruction following failure"** (capability issue)
- Actually: **token limit exhaustion** (infrastructure issue)

**Current Impact:**
- Models fail on large skeletons, appear "unsuitable"
- Smaller models succeed on smaller skeletons, appear better
- We can't test fairly across different skeleton sizes

**v2.0 Solution:**
- Explicitly set `num_predict: 8192` (or configurable) in Ollama payload
- If output truncates, detect it and **retry with smaller skeleton or multi-step decomposition**
- Log **"Context Window Exhaustion"** as distinct failure mode
- Router knows: "This model needs structured input or multi-stage decomposition"

---

### Vulnerability 2C: Synchronous Timeouts
**Problem:**
- Hardcoded `TIMEOUT_SECONDS = 300` (5 minutes)
- Testing 70B on CPU offloading can take 20+ minutes
- Timeout fires; script crashes
- Logged as capability failure, actually infrastructure timeout

**Current Impact:**
- Heavy models fail on consumer hardware
- We incorrectly conclude they're not suitable
- Can't fairly compare 7B (fast) vs. 70B (slow)

**v2.0 Solution:**
- Make timeout configurable: `--timeout 600` (10 min default, adjustable)
- Distinguish timeout from real failure in logs
- Router knows: "This model needs more time on your hardware"

---

## Part 2: v2.0 Architecture & Requirements

### Requirement 2.1: Evaluator Model (LLM-as-a-Judge)

**What it is:**
A separate, heavy model (typically frontier or 70B+) that **grades Stage 2 output semantically**.

**How it works:**
```
Stage 2 Output (Decomposition)
  ↓
Evaluator Model receives:
  - Original skeleton
  - Model's decomposition
  - Prompts: "On a scale 1-5, how well does this decomposition match the skeleton?"
  - Criteria: Task relevance, dependency logic, estimate realism, assumption identification
  ↓
Evaluator returns: semantic_quality_score (1-5)
  ↓
analyze_coding_audit.py integrates into composite:
  composite_score = (granularity_score * 0.3 + semantic_score * 0.4 + self_awareness_score * 0.3)
```

**Implementation:**
- New CLI parameter: `--evaluator-model llama3:70b`
- If not provided, skip evaluator (backward compatible with v1.0)
- Add to `analyze_coding_audit.py`: new `evaluate_semantic_quality()` function
- Registry entry includes `semantic_quality_score` (if available)

**Why it matters:**
- Separates **structure** (granularity) from **substance** (semantics)
- Catches gamified outputs (30 micro-tasks)
- Provides objective third-party judgment

---

### Requirement 2.2: JSON Auto-Repair & Decoupling

**What it is:**
A utility function that repairs common JSON formatting issues, allowing the pipeline to continue even if formatting fails.

**Implementation:**

```python
def clean_json_output(raw_text: str) -> tuple[dict, bool, str]:
    """
    Attempt to parse and repair JSON output.
    
    Returns:
      (parsed_dict, was_repaired, repair_method)
    """
    # Try raw first
    try:
        return json.loads(raw_text), False, "raw"
    except json.JSONDecodeError:
        pass
    
    # Strip markdown fences
    if "```json" in raw_text:
        match = re.search(r'```json\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1)), True, "markdown_stripping"
            except json.JSONDecodeError:
                pass
    
    # Remove leading junk
    if "{" in raw_text:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        try:
            return json.loads(raw_text[start:end]), True, "trim_and_extract"
        except json.JSONDecodeError:
            pass
    
    # All repairs failed
    return None, False, "no_repair_possible"
```

**Pipeline integration:**
```python
# In enki_stage2_decompose.py
raw_content = resp.get("message", {}).get("content", "")
decomposition, was_repaired, repair_method = clean_json_output(raw_content)

if decomposition is None:
    # Real failure
    return {"success": False, "error": "JSON parsing failed"}

if was_repaired:
    # Flag for registry
    results["formatting_issue"] = {
        "required_repair": repair_method,
        "penalty": "formatting_strict"  # Router knows to add output schema
    }
else:
    results["formatting_issue"] = None
```

**Why it matters:**
- Decouples formatting from capability
- Loses data when a simple fix could recover it
- Router learns: "This model needs explicit output schema in production"

---

### Requirement 2.3: API Resilience Controls

**Temperature Tuning:**
```python
# Stage 2: Decomposition (strict JSON)
STAGE2_TEMPERATURE = 0.1  # Deterministic; reduce hallucination

# Stage 3: Self-Assessment (some creativity ok)
STAGE3_TEMPERATURE = 0.3  # Slightly more exploration
```

**Token Limits:**
```python
payload = {
    "model": model,
    "messages": messages,
    "stream": False,
    "options": {
        "temperature": temperature,
        "num_predict": 8192,  # Explicit ceiling; adjust per skeleton size
    },
}
```

**Configurable Timeout:**
```bash
python enki_stage2_decompose.py \
  --model gemma4:26b \
  --skeleton skeleton.json \
  --timeout 900  # 15 minutes for heavy models
```

**Detection & Logging:**
```python
def detect_failure_mode(error, response_length, timeout_seconds):
    """Classify failure as capability vs. infrastructure issue."""
    if error == "timeout":
        return "infrastructure_timeout"
    elif response_length > 0 and not response_valid:
        return "context_window_exhaustion"
    elif json_parse_fails:
        return "formatting_error"
    else:
        return "capability_failure"
```

**Why it matters:**
- Fair comparison across models and hardware
- Distinguishes infrastructure from capability issues
- Router gets actionable parameters (timeout, token limits, temperature)

---

### Requirement 2.4: Multi-Tiered Scaffolding Logic (Core v2.0 Feature)

**What it is:**
Automatic retry sequence if Stage 2 fails, with increasing levels of scaffolding.

**Scaffolding Levels:**

| Level | Name | Prompt Modification | Use Case |
|-------|------|-------------------|----------|
| 0 | Zero-Shot | Original v1.0 prompt | Model gets it right first try |
| 1 | Few-Shot + Schema | Add explicit JSON schema + 1-shot example | Model needs structure hint |
| 2 | CoT + Schema | Add "Think step-by-step" + schema + example | Model needs reasoning scaffold |

**Implementation:**

```python
def build_decomposition_prompt(skeleton: dict, scaffolding_level: int) -> str:
    """Build prompt with scaffolding appropriate to level."""
    base_prompt = build_base_prompt(skeleton)
    
    if scaffolding_level == 0:
        # v1.0 style
        return base_prompt
    
    elif scaffolding_level == 1:
        # Add JSON schema + example
        schema = """
        Output MUST be valid JSON matching:
        {
          "project_title": string,
          "module_decomposition": {
            "module_name": {
              "description": string,
              "atomic_tasks": [
                {
                  "id": "MOD_001",
                  "name": string,
                  "estimated_hours": number,
                  "dependencies": [string]
                }
              ]
            }
          }
        }
        """
        example = """
        Example output:
        {
          "project_title": "Stock Trading Simulator",
          "module_decomposition": {
            "market_data_fetcher": {
              "description": "Fetches real-time stock prices",
              "atomic_tasks": [
                {
                  "id": "MARKET_001",
                  "name": "Implement IEX Cloud API client",
                  "estimated_hours": 2,
                  "dependencies": []
                }
              ]
            }
          }
        }
        """
        return base_prompt + schema + example
    
    elif scaffolding_level == 2:
        # Add CoT
        cot_trigger = """
        Before generating JSON, think through the decomposition:
        1. List each module
        2. For each module, list 2-3 key sub-tasks
        3. Estimate hours for each task
        4. Identify dependencies
        5. Now generate the final JSON.
        """
        return base_prompt + cot_trigger + (level_1 schema + example)
```

**Retry Logic:**

```python
def run_decomposition_with_retries(host, model, skeleton, max_level=2):
    """Retry decomposition with increasing scaffolding."""
    for level in range(max_level + 1):
        prompt = build_decomposition_prompt(skeleton, level)
        resp = chat(host, model, [{"role": "user", "content": prompt}])
        raw = resp.get("message", {}).get("content", "")
        
        decomposition, was_repaired, repair_method = clean_json_output(raw)
        
        if decomposition is not None:
            # Success!
            return {
                "decomposition": decomposition,
                "scaffolding_level": level,
                "was_repaired": was_repaired,
                "repair_method": repair_method,
            }
    
    # All levels failed
    return {
        "decomposition": None,
        "scaffolding_level": None,
        "error": "All scaffolding levels exhausted"
    }
```

**Registry Entry:**

```yaml
model: gemma4:26b
category: coding_decomposition
scaffolding_required:
  decomposition_level: 1  # Needs few-shot + schema
  selfassess_level: 0     # Zero-shot ok
  formatting_strict: true # Output schema penalty
enki_composite_score: 3.5
```

**Why it matters:**
- Discovers that most models are **actually capable** with the right scaffolding
- v1.0 discarded models that just needed a hint
- Router knows exactly how much context to prepend in production
- Enables **pragmatic deployment**: "Use Gemma 4 26B for decomposition, but prepend few-shot examples"

---

## Part 3: File Structure & Changes

### New/Modified Files

```
enki/v2.0/
├── utils/
│   ├── json_repair.py              [NEW] JSON cleaning + repair
│   ├── scaffolding.py              [NEW] Prompt builders for 3 levels
│   └── failure_detection.py        [NEW] Classify failure modes
│
├── enki_stage2_decompose.py        [MODIFIED] Add retry logic, cleaning
├── enki_stage3_selfassess.py       [MODIFIED] Add optional evaluator
├── enki_stage4_analyze.py          [MODIFIED] Semantic scoring, registry
│
├── evaluators/
│   └── semantic_evaluator.py       [NEW] LLM-as-a-judge for Stage 2
│
└── v2_ARCHITECTURE.md              [NEW] This document
```

### Backward Compatibility

- v2.0 scripts accept `--evaluator-model` (optional; defaults to None)
- Without evaluator: composite score = v1.0 algorithm (backward compatible)
- Scaffolding retry is optional: `--max-scaffolding-level 0` disables (v1.0 behavior)
- JSON repair is automatic but logged

**v1.0 users can upgrade to v2.0 with zero config changes.**

---

## Part 4: Success Criteria for v2.0

### Methodological Improvements

- [ ] Evaluator model provides semantic quality score (1-5)
- [ ] Composite score accounts for semantic quality (not just structure)
- [ ] Small models with garbage outputs don't score higher than large models
- [ ] Metric gamification is detected (evaluator flags 30 micro-tasks as nonsense)

### Pipeline Resilience

- [ ] JSON formatting errors don't crash the pipeline
- [ ] Stage 3 runs even if Stage 2 formatting is bad
- [ ] Formatting penalty is clearly logged in registry
- [ ] Context window exhaustion is detected and logged separately

### Scaffolding Discovery

- [ ] Models retry with Level 1 (few-shot) if zero-shot fails
- [ ] Models retry with Level 2 (CoT) if Level 1 fails
- [ ] Final registry entry includes `scaffolding_level_required`
- [ ] Router can use this to prepend context in production

### Infrastructure Resilience

- [ ] Timeout is configurable per run
- [ ] Token limits are explicitly set
- [ ] Temperature is optimized per stage
- [ ] Failure modes are classified (capability vs. infrastructure)

---

## Part 5: Deployment Considerations

### v1.0 → v2.0 Migration Path

**Week 1:** Deploy v2.0 with evaluator disabled (`--evaluator-model none`)
- Baseline: Run existing v1.0 tests against v2.0 code
- Verify backward compatibility
- Ensure scaffolding retries work as expected

**Week 2:** Enable evaluator on one model (Gemma 4 26B)
- Compare v1.0 scores vs. v2.0 scores
- Analyze variance (expected if evaluator reveals hidden issues)
- Validate that evaluator is making sensible judgments

**Week 3:** Full fleet evaluation with v2.0 + evaluator
- Re-audit all models with new framework
- Generate new registry entries with scaffolding levels
- Update Concierge Router with new model profiles

**Week 4+:** Ongoing
- Monitor Router's use of scaffolding levels in production
- Refine evaluator prompts if needed
- Expand test skeletons to edge cases

---

## Part 6: Open Questions & Future Work

1. **Evaluator Licensing:** Can we use a local 70B model as evaluator, or do we need a frontier model (Claude, Gemini)? This impacts cost/latency.

2. **Semantic Grading Criteria:** What exactly should the evaluator score? (Relevance, completeness, realism of estimates, dependency accuracy?) Should these be separate scores or one holistic score?

3. **Scaffolding Autoscaling:** Should we automatically increase `num_predict` if we detect context window exhaustion, or just retry with scaffolding?

4. **Multi-Skeleton Testing:** v2.0 currently works on one skeleton per audit. Should we test a model against 3-5 different skeletons (stock trading, web app, microservices, DevOps, etc.) to get a better profile?

---

## Summary

Enki v2.0 transforms from a **structural audit framework** to a **resilient, semantically-aware evaluation system** that:

✅ Measures **substance, not just shape**  
✅ Separates **formatting issues from capability issues**  
✅ **Discovers required scaffolding** for borderline models  
✅ Provides **actionable Router guidance** (scaffolding_level_required)  
✅ Maintains **backward compatibility** with v1.0  

---

*v2.0 Architecture Design complete. Ready for implementation.*
