# ENKI v2.0: ARCHITECTURE REVISION & SCAFFOLDING SEED

**Date:** April 2026
**Domain:** Software (Enki Framework)
**Target:** Claude Code (or equivalent AI Dev Assistant)
**Purpose:** This document serves as the master seed for the v2.0 "Scaffolding & Resilience" pass of the Enki Model Evaluation Suite. It contains the red-team critique of the v1.0 baseline and strict architectural requirements for the v2.0 rebuild.

---

## PART 1: RED-TEAM CRITIQUE OF v1.0 (THE "GOTCHAS")
*Context for Claude: Address the following vulnerabilities present in the current v1.0 implementation.*

### 1. Methodological Flaws
* **The Self-Assessment Paradox ("Marking its own homework"):** Small/weak models (e.g., 7B) often suffer from the Dunning-Kruger effect, generating garbage decompositions but rating their confidence highly (4-5/5). Highly capable, aligned models (e.g., 70B) tend to be cautious and penalize themselves. Currently, the system might favor a confident but incompetent model over a cautious expert.
* **Metric Gamification (Shape vs. Substance):** Stage 2 measures task granularity by counting tasks in the 1-4 hour bucket. A model can game this by outputting 30 useless tasks (e.g., "Write one line of code") estimated at 2 hours each. It scores perfectly on granularity, but the decomposition is semantically useless. We are measuring structure, not substance.

### 2. Pipeline Fragility
* **The Strict JSON Domino Effect:** In v1.0, a failure to generate valid JSON in Stage 2 (e.g., wrapping it in markdown backticks) completely crashes the script. Because the pipeline is tightly coupled, a Stage 2 crash prevents Stage 3 (Self-Assessment) from running. We conflate a formatting failure with a total capability failure, losing valuable self-assessment calibration data.
* **Context Window Exhaustion (Silent Truncation):** Decomposing large skeletons results in massive, highly-nested JSON outputs. Local models often hit default `num_predict` limits mid-generation and stop. The resulting truncated string fails `json.loads()`, which the suite falsely logs as an "instruction following failure" rather than a token limit exhaustion.
* **Synchronous Timeouts:** Hardcoding `TIMEOUT_SECONDS = 300` fails when testing heavier models (70B) on consumer hardware or CPU offloading, causing false-negative evaluations due to timeout crashes.

---

## PART 2: BUILD INSTRUCTIONS FOR v2.0 (SCAFFOLDING PASS)
*Context for Claude: Implement the following structural changes to the Enki codebase to support Scaffolding and Semantic Evaluation.*

### Requirement 2.1: Implement an "Evaluator Model" (LLM-as-a-Judge)
Shift from pure structural counting to semantic grading.
* **Action:** Introduce a new parameter `--evaluator-model` (targeting a heavy/frontier model like Llama-3-70B or an external API).
* **Logic:** Instead of just counting the length of the `unstated_assumptions` array, pass the Stage 2 output to the Evaluator Model to grade the *reasonableness* and *semantic quality* of the decomposition on a 1-5 scale.
* **Integration:** Update `analyze_coding_audit.py` to factor this semantic score into the final composite score.

### Requirement 2.2: Decouple the Pipeline & Implement JSON Auto-Repair
Separate formatting adherence from decomposition capability.
* **Action:** Implement a `clean_json_output()` utility function that strips markdown fences (e.g., ```json ... ```) and attempts basic regex repairs before passing to `json.loads()`.
* **Logic:** If the raw output fails to parse, try the repaired output. If the repaired output parses successfully, **flag the model for a "Strict Formatting Penalty"** in the registry, but *allow the pipeline to continue* to Stage 3.
* **Result:** We get to keep the Stage 3 self-assessment data even if the model is slightly bad at formatting.

### Requirement 2.3: API Resilience Controls
Hardened parameters for local execution.
* **Temperature Override:** Change `DEFAULT_TEMPERATURE` for Stage 2 from `0.5` to `0.1` (or `0.0`) to heavily reduce structural hallucinations during strict JSON schema generation. Keep Stage 3 slightly higher if conversational insight is needed.
* **Dynamic Token Limits:** Update the Ollama API payload to explicitly pass `num_predict: 8192` (or higher) in the `options` dictionary to prevent silent truncation.
* **Adjustable Timeouts:** Allow the timeout to be passed as a CLI argument (`--timeout`), defaulting to at least `600` seconds.

### Requirement 2.4: Multi-Tiered Scaffolding Logic (The Core v2.0 Feature)
Build dynamic retry logic into the pipeline to test scaffolding theories.
* **Action:** If a model fails to produce a valid decomposition on the "Zero-Shot" pass, implement an automatic retry sequence:
    1.  **Level 1 (Zero-Shot):** The v1.0 prompt.
    2.  **Level 2 (Few-Shot/Schema):** If Level 1 fails structurally, retry the prompt by appending an explicit output schema structure and a 1-shot example.
    3.  **Level 3 (CoT Trigger):** If Level 2 fails, append "Think step-by-step before generating the JSON."
* **Logging:** The final output `audit_report` MUST record the `scaffolding_level_required` (0, 1, or 2) to achieve a valid output. This data is critical for the Concierge Router to know how much context it needs to prepend when deploying this model in production.
