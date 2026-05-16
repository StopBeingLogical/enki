# ENKI v2.0 Implementation Roadmap
## Stage-by-Stage Build Plan for Scaffolding & Resilience

**Date:** April 14, 2026  
**Target Completion:** 2-3 weeks (staged rollout)  
**Prerequisite:** Read ENKI_V2_ARCHITECTURE.md

---

## Phase 1: Utilities & Helper Functions (Week 1)

### 1.1 Create `json_repair.py`
**Purpose:** Clean and repair malformed JSON outputs  
**Location:** `enki/v2.0/utils/json_repair.py`

**Key Functions:**
```python
def clean_json_output(raw_text: str) -> Tuple[Optional[dict], bool, str]:
    """
    Parse or repair JSON from LLM output.
    
    Args:
        raw_text: Raw response from Ollama
    
    Returns:
        (parsed_dict, was_repaired, repair_method)
        - parsed_dict: Valid dict if successful, None if all repairs failed
        - was_repaired: True if repairs were needed
        - repair_method: "raw", "markdown_stripping", "trim_extract", "no_repair"
    """
    # Try raw
    # Strip markdown
    # Extract braces
    # Return None if all fail
```

**Test Cases:**
- Raw valid JSON → returns (dict, False, "raw")
- JSON with markdown fences → returns (dict, True, "markdown_stripping")
- JSON with leading junk → returns (dict, True, "trim_extract")
- Completely malformed → returns (None, False, "no_repair_possible")

---

### 1.2 Create `failure_detection.py`
**Purpose:** Classify failures as capability vs. infrastructure  
**Location:** `enki/v2.0/utils/failure_detection.py`

**Key Functions:**
```python
def detect_failure_mode(
    error: Optional[Exception],
    response_text: str,
    elapsed_seconds: float,
    timeout_seconds: float,
    expected_tokens: int
) -> str:
    """
    Classify failure into specific buckets.
    
    Returns one of:
        - "capability_failure" (model couldn't do the task)
        - "context_window_exhaustion" (ran out of tokens)
        - "timeout" (took too long)
        - "formatting_error" (JSON parsing failed even after repair)
        - "infrastructure_error" (API/Ollama issue)
    """
```

**Logic:**
- If elapsed > timeout: `timeout`
- Elif response_length > 0 but parsing fails: `context_window_exhaustion`
- Elif response_length = 0: `infrastructure_error`
- Elif parsing fails: `formatting_error`
- Else: `capability_failure`

---

### 1.3 Create `scaffolding.py`
**Purpose:** Build prompts with dynamic scaffolding levels  
**Location:** `enki/v2.0/utils/scaffolding.py`

**Key Functions:**
```python
def build_decomposition_prompt(skeleton: dict, scaffolding_level: int = 0) -> str:
    """
    Build Stage 2 decomposition prompt with optional scaffolding.
    
    Level 0: Original v1.0 prompt (zero-shot)
    Level 1: Add explicit JSON schema + 1-shot example
    Level 2: Add "think step-by-step" CoT trigger + schema + example
    """

def build_selfassess_prompt(decomposition: dict, scaffolding_level: int = 0) -> str:
    """
    Build Stage 3 self-assessment prompt.
    (Usually doesn't need scaffolding, but support it for consistency)
    """
```

**Important:** These should be drop-in replacements for the current hardcoded prompts.

---

## Phase 2: Core Pipeline Modifications (Week 1-2)

### 2.1 Refactor `enki_stage2_decompose.py`
**File:** `/mnt/user-data/outputs/enki_stage2_decompose.py`

**Changes:**

1. **Add CLI parameters:**
   ```python
   parser.add_argument("--timeout", type=int, default=600, help="Request timeout in seconds")
   parser.add_argument("--max-scaffolding-level", type=int, default=2, help="Max retry level (0=v1.0 behavior)")
   parser.add_argument("--temperature-stage2", type=float, default=0.1, help="Temperature for decomposition")
   ```

2. **Update `chat()` function:**
   ```python
   payload = {
       "model": model,
       "messages": messages,
       "stream": False,
       "options": {
           "temperature": temperature,
           "num_predict": 8192,  # Explicit token limit
       },
   }
   ```

3. **Replace hardcoded prompt with:**
   ```python
   from enki.utils.scaffolding import build_decomposition_prompt
   
   prompt = build_decomposition_prompt(skeleton, scaffolding_level)
   ```

4. **Implement retry logic:**
   ```python
   def run_decomposition_with_retries(host, model, skeleton, max_level=2, timeout=600):
       for level in range(max_level + 1):
           prompt = build_decomposition_prompt(skeleton, level)
           resp = chat(host, model, [...], timeout=timeout)
           raw_content = resp.get("message", {}).get("content", "")
           
           from enki.utils.json_repair import clean_json_output
           decomposition, was_repaired, repair_method = clean_json_output(raw_content)
           
           if decomposition is not None:
               return {
                   "success": True,
                   "decomposition": decomposition,
                   "scaffolding_level": level,
                   "formatting_issue": {
                       "was_repaired": was_repaired,
                       "repair_method": repair_method
                   }
               }
       
       # All levels failed
       return {
           "success": False,
           "error": "All scaffolding levels exhausted",
           "failure_mode": detect_failure_mode(...)
       }
   ```

5. **Update output JSON:**
   ```python
   all_results = {
       "model": args.model,
       ...
       "scaffolding": {
           "level_required": result.get("scaffolding_level"),
           "formatting_issue": result.get("formatting_issue"),
           "failure_mode": result.get("failure_mode"),
       }
   }
   ```

---

### 2.2 Refactor `enki_stage3_selfassess.py`
**File:** `/mnt/user-data/outputs/enki_stage3_selfassess.py`

**Changes (minimal):**

1. **Add CLI parameters:**
   ```python
   parser.add_argument("--timeout", type=int, default=600)
   parser.add_argument("--temperature-stage3", type=float, default=0.3)
   ```

2. **Update temperature:**
   ```python
   temperature = args.temperature_stage3 if hasattr(args, 'temperature_stage3') else 0.3
   ```

3. **Use updated `chat()` with token limits:**
   ```python
   payload["options"]["num_predict"] = 8192
   ```

4. **Update output to include scaffolding info:**
   ```python
   all_results = {
       ...
       "input_scaffolding_level": decomposition_data.get("scaffolding", {}).get("level_required"),
   }
   ```

---

### 2.3 Create `semantic_evaluator.py`
**File:** `/mnt/user-data/outputs/enki_stage2b_semantic_evaluator.py`

**Purpose:** LLM-as-a-judge for Stage 2 output  
**Optional Stage (between Stage 2 and Stage 4)**

**Key Functions:**
```python
def evaluate_semantic_quality(
    host: str,
    evaluator_model: str,
    skeleton: dict,
    decomposition: dict,
) -> dict:
    """
    Use evaluator model to grade decomposition quality.
    
    Returns:
        {
            "semantic_quality_score": 1-5,
            "feedback": "...",
            "evaluation_details": {...}
        }
    """
    
    prompt = f"""
    You are an expert architect evaluating a project decomposition.
    
    Project Skeleton:
    {json.dumps(skeleton, indent=2)}
    
    Model's Decomposition:
    {json.dumps(decomposition, indent=2)}
    
    On a scale 1-5, evaluate:
    1. Task relevance (do tasks match skeleton modules?)
    2. Dependency logic (are dependencies correct?)
    3. Estimate realism (are hour estimates realistic?)
    4. Assumption quality (are assumptions reasonable?)
    5. Overall semantic soundness
    
    Provide:
    1. A single 1-5 score
    2. Brief feedback (2-3 sentences)
    3. Any major issues detected
    
    Respond in JSON:
    {{
        "score": <1-5>,
        "feedback": "...",
        "issues": ["...", "..."]
    }}
    """
    
    resp = chat(host, evaluator_model, [{"role": "user", "content": prompt}])
    # Parse response, return score + feedback
```

**Integration:** This is **optional** and called only if `--evaluator-model` is provided.

---

## Phase 3: Analysis & Registry Updates (Week 2)

### 3.1 Refactor `enki_stage4_analyze.py`
**File:** `/mnt/user-data/outputs/enki_stage4_analyze.py`

**Changes:**

1. **Add evaluator support:**
   ```python
   parser.add_argument("--evaluator-model", default=None, help="Optional evaluator model for semantic grading")
   
   if args.evaluator_model:
       from enki_stage2b_semantic_evaluator import evaluate_semantic_quality
       semantic_result = evaluate_semantic_quality(
           args.host,
           args.evaluator_model,
           skeleton,
           decomposition
       )
   else:
       semantic_result = None
   ```

2. **Update composite score calculation:**
   ```python
   def compute_composite_score_v2(results, semantic_score=None):
       # v1.0 algorithm (if no semantic score)
       if semantic_score is None:
           return compute_composite_score(results)  # fallback to v1.0
       
       # v2.0 algorithm (with semantic quality)
       granularity_score = results.get("decomposition", {}).get("task_granularity", {}).get("1_to_4hr_pct", 0) / 20
       selfassess_score = results.get("self_assessment", {}).get("overall_confidence", 0) / 5
       
       # Semantic score floors the granularity (if semantics are bad, granularity can't save it)
       granularity_score = min(granularity_score, semantic_score)
       
       composite = (
           granularity_score * 0.3 +
           semantic_score * 0.4 +
           selfassess_score * 0.3
       )
       
       return round(composite, 2)
   ```

3. **Update registry entry with scaffolding data:**
   ```python
   registry_entry = {
       "model": model,
       "scaffolding": {
           "decomposition_level": decomp_result.get("scaffolding", {}).get("level_required"),
           "formatting_penalty": decomp_result.get("scaffolding", {}).get("formatting_issue", {}).get("was_repaired"),
           "failure_mode": decomp_result.get("scaffolding", {}).get("failure_mode"),
       },
       "semantic_quality": semantic_result.get("score") if semantic_result else None,
       ...
   }
   ```

---

## Phase 4: Testing & Validation (Week 2-3)

### 4.1 Test Suite for v2.0
**Location:** `enki/tests/test_v2.py`

**Test Cases:**

```python
# Test JSON repair
def test_clean_json_markdown_fence():
    raw = """```json
    {"key": "value"}
    ```"""
    result, was_repaired, method = clean_json_output(raw)
    assert result == {"key": "value"}
    assert was_repaired == True
    assert method == "markdown_stripping"

# Test failure detection
def test_detect_context_window():
    response = "very long partial JSON..."[0:100]  # truncated
    mode = detect_failure_mode(None, response, 120, 300, 8000)
    assert mode == "context_window_exhaustion"

# Test scaffolding prompt building
def test_scaffolding_levels():
    skeleton = {"title": "test"}
    
    p0 = build_decomposition_prompt(skeleton, 0)
    assert "Think step-by-step" not in p0
    
    p2 = build_decomposition_prompt(skeleton, 2)
    assert "Think step-by-step" in p2
    assert "Example output" in p2

# Test semantic evaluator (requires evaluator model)
def test_semantic_evaluation(evaluator_model):
    score = evaluate_semantic_quality(
        "http://localhost:11434",
        evaluator_model,
        skeleton,
        bad_decomposition
    )
    assert score < 3  # bad decomposition should score low
```

### 4.2 Backward Compatibility Tests

```python
# Test v1.0 behavior is preserved when v2.0 options not used
def test_v1_compatibility():
    # Run with --max-scaffolding-level 0 (disable retries)
    # Run without --evaluator-model
    # Verify output format matches v1.0
    assert results["scaffolding"]["level_required"] == 0
    assert results.get("semantic_quality") is None
```

---

## Phase 5: Deployment & Migration (Week 3)

### 5.1 Documentation Updates

**Update files:**
- `ENKI_QUICK_REFERENCE.md` — Add v2.0 flags
- `ENKI_GUIDE.md` — Add scaffolding section
- `ENKI_NAMING_SUMMARY.md` — Note v2.0 updates

**New documents:**
- `ENKI_V2_MIGRATION_GUIDE.md` — How to upgrade from v1.0
- `ENKI_V2_TROUBLESHOOTING.md` — New failure modes and solutions

### 5.2 Rollout Plan

**Week 1:** Deploy v2.0 with scaffolding disabled
```bash
python enki_stage2_decompose.py \
  --model gemma4:26b \
  --skeleton skeleton.json \
  --max-scaffolding-level 0  # v1.0 behavior
```

**Week 2:** Enable scaffolding on one model
```bash
python enki_stage2_decompose.py \
  --model gemma4:26b \
  --skeleton skeleton.json \
  --max-scaffolding-level 2  # Full retry logic
```

**Week 3:** Full migration
- All models tested with v2.0
- Evaluator enabled (if available)
- Router updated with scaffolding levels

---

## Summary of Changes

### Files Modified
- `enki_stage2_decompose.py` — Add scaffolding retry, JSON repair
- `enki_stage3_selfassess.py` — Add timeout/temperature tuning
- `enki_stage4_analyze.py` — Add semantic scoring, registry updates

### Files Created
- `enki/utils/json_repair.py` — JSON cleaning utility
- `enki/utils/failure_detection.py` — Failure classification
- `enki/utils/scaffolding.py` — Prompt building with levels
- `enki_stage2b_semantic_evaluator.py` — Optional evaluator stage
- Test suite + documentation

### Backward Compatibility
✅ v2.0 is fully backward compatible with v1.0
- Run with `--max-scaffolding-level 0` to get v1.0 behavior
- Run without `--evaluator-model` to skip semantic scoring
- Default settings are v1.0-compatible

---

## Estimated Effort

| Phase | Task | Hours | Who |
|-------|------|-------|-----|
| 1 | Utilities | 4-6 | Claude Code |
| 2 | Core pipeline | 8-10 | Claude Code |
| 3 | Analysis updates | 4-6 | Claude Code |
| 4 | Testing | 4-6 | Manual + Claude Code |
| 5 | Deployment | 2-4 | Manual |
| **Total** | | **22-32** | |

---

*Implementation roadmap complete. Ready to begin Phase 1.*
