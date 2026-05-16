# Enki — Quick Reference & Testing Checklist
**Name:** Enki (Sumerian: god of wisdom and knowledge)  
**Domain:** Software (per identity-naming-v1.0)  
**Version:** v1.0 (v2.0 design complete, implementation ready)  
**Date:** April 13-14, 2026  
**Status:** v1.0 Complete, v2.0 Architected

---

## Quick Reference Card

### One-Liner Commands

```bash
# Full Enki audit, single model
python eval_coding_decompose.py --model gemma4:26b --skeleton project_skeleton_stock_trading.json --output enki_decomposition_gemma4.json && \
python eval_coding_selfassess.py --model gemma4:26b --decomposition enki_decomposition_gemma4.json --output enki_selfassess_gemma4.json && \
python analyze_coding_audit.py --decomposition enki_decomposition_gemma4.json --selfassess enki_selfassess_gemma4.json --output enki_audit_report_gemma4.json --registry-entry enki_registry_gemma4.json

# Compare two models (Enki)
python analyze_coding_audit.py \
  --decomposition enki_decomposition_gemma4.json \
  --selfassess enki_selfassess_gemma4.json \
  --output enki_audit_report_gemma4.json \
  --compare-with enki_audit_report_llama2.json
```

### Key Metrics at a Glance

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| **Task Granularity** | 60-70% in 1-4hr | <50% or >80% | <30% or >90% |
| **Assumptions** | < 3 | 3-5 | > 5 |
| **Questions Asked** | > 3 | 1-3 | 0 |
| **Overall Confidence** | 3-4/5 | 2-3 or 4-5 | 1 or 5 |
| **Risk Areas** | > 3 | 2-3 | < 2 |
| **Composite Score** | > 3.5 | 2.5-3.5 | < 2.5 |

### Interpreting Results in 30 Seconds

```
Excellent (4.0+):        ✓ Use for coding decomposition tasks
Good (3.0-4.0):          ⚠ Acceptable, but review output
Borderline (2.0-3.0):    ✗ Not recommended without heavy review
Poor (< 2.0):            ✗ Model unsuitable for this task
```

---

## Testing Checklist

### Pre-Flight (Before Running Audits)

- [ ] Ollama running: `curl http://localhost:11434/api/tags`
- [ ] Model available: Check that target model is installed
- [ ] Python 3.9+: `python --version`
- [ ] Dependencies: `pip list | grep requests`
- [ ] Skeleton file exists: `ls -la project_skeleton_stock_trading.json`
- [ ] Scripts are executable: `ls -la eval_*.py analyze_*.py`

### Test Run (Quick Validation)

**Estimated time: 5-10 minutes**

```bash
# 1. Quick test of Enki Stage 2 (decomposition)
python eval_coding_decompose.py --model gemma4:26b --skeleton project_skeleton_stock_trading.json --output enki_test_decomposition.json

# Expected output:
#   ✓ "Decomposition succeeded"
#   ✓ Metrics printed (total tasks, granularity dist, confidence)
#   ✓ JSON file created with decomposition data
```

- [ ] Decomposition script runs without error
- [ ] JSON output is valid: `python -m json.tool enki_test_decomposition.json > /dev/null`
- [ ] Metrics look reasonable (5+ tasks, mostly 1-4 hours)

```bash
# 2. Quick test of Enki Stage 3 (self-assessment)
python eval_coding_selfassess.py --model gemma4:26b --decomposition enki_test_decomposition.json --output enki_test_selfassess.json

# Expected output:
#   ✓ "Self-assessment succeeded"
#   ✓ Confidence per category printed
#   ✓ JSON file created
```

- [ ] Self-assessment script runs without error
- [ ] JSON output is valid
- [ ] Confidence scores are 1-5 range

```bash
# 3. Quick test of Enki Stage 4 (analysis)
python analyze_coding_audit.py --decomposition enki_test_decomposition.json --selfassess enki_test_selfassess.json --output enki_test_audit_report.json --registry-entry enki_test_registry.json

# Expected output:
#   ✓ Comprehensive report printed
#   ✓ Key findings listed
#   ✓ JSON files created
```

- [ ] Analysis script runs without error
- [ ] Audit report includes key findings
- [ ] Registry entry looks correct

### Full Audit (Production Run)

**Estimated time: 5 minutes per model**

**Gemma 4 26B:**
```bash
python eval_coding_decompose.py --model gemma4:26b --skeleton project_skeleton_stock_trading.json --output enki_decomposition_gemma4.json
python eval_coding_selfassess.py --model gemma4:26b --decomposition enki_decomposition_gemma4.json --output enki_selfassess_gemma4.json
python analyze_coding_audit.py --decomposition enki_decomposition_gemma4.json --selfassess enki_selfassess_gemma4.json --output enki_audit_report_gemma4.json --registry-entry enki_registry_gemma4.json
```

- [ ] All three scripts complete without errors
- [ ] Three JSON files created (decomposition, selfassess, audit_report)
- [ ] Composite score printed
- [ ] Key findings look reasonable

**Llama 2 70B (Optional):**
```bash
python eval_coding_decompose.py --model llama2:70b --skeleton project_skeleton_stock_trading.json --output enki_decomposition_llama2.json
python eval_coding_selfassess.py --model llama2:70b --decomposition enki_decomposition_llama2.json --output enki_selfassess_llama2.json
python analyze_coding_audit.py --decomposition enki_decomposition_llama2.json --selfassess enki_selfassess_llama2.json --output enki_audit_report_llama2.json --registry-entry enki_registry_llama2.json
```

- [ ] Llama audit completes successfully
- [ ] Scores comparable to Gemma (or show clear difference)

### Comparison (Optional)

```bash
python analyze_coding_audit.py \
  --decomposition decomposition_gemma4.json \
  --selfassess selfassess_gemma4.json \
  --output audit_report_gemma4.json \
  --compare-with audit_report_llama2.json
```

- [ ] Comparison runs without error
- [ ] Side-by-side metrics shown
- [ ] Winner for each category identified

### Spot-Check Validation (Recommended)

Pick 3-5 tasks from the decomposition that scored high on the model's self-confidence. Test them:

**Example Task:**
```
From decomposition:
{
  "id": "BACKEND_001",
  "name": "Implement FastAPI authentication endpoints",
  "estimated_hours": 2,
  "can_produce": "yes",
  "confidence": 4
}
```

**Test:**
```bash
# Ask the model to execute the task
ollama run gemma4:26b "Implement FastAPI authentication endpoints (JWT-based) 
with the following requirements: 
1. POST /auth/register - create new user
2. POST /auth/login - return JWT token
3. Middleware to verify tokens on protected routes
4. Error handling for invalid tokens
Include example code."
```

- [ ] Model produces code
- [ ] Code appears functional (syntax correct, logic sound)
- [ ] Code addresses all requirements
- [ ] If code works → validates high confidence claim
- [ ] If code fails → indicates overconfidence in self-assessment

### Data Validation

```bash
# Verify all JSON files are valid
for f in decomposition_*.json selfassess_*.json audit_report_*.json registry_*.json; do
  echo "Checking $f..."
  python -m json.tool "$f" > /dev/null && echo "  ✓ Valid" || echo "  ✗ Invalid JSON"
done
```

- [ ] All JSON files valid
- [ ] No parse errors in output
- [ ] All required fields present in each JSON

### Results Summary Template

After running Enki audits, fill in this summary:

```
ENKI AUDIT RESULTS SUMMARY
==========================

Model Tested: [gemma4:26b / llama2:70b / other]
Skeleton: Stock Trading Simulator
Date: [date]
Total Runtime: [time]

METRICS:
  Composite Score: [X.X/5.0]
  Task Granularity: [X%] in target range
  Assumptions: [N] (target < 3)
  Questions Asked: [N] (target > 3)
  Overall Confidence: [X/5]

KEY FINDINGS:
  ✓ [Finding 1]
  ⚠ [Finding 2]
  ✗ [Finding 3]

RECOMMENDATION:
  [ ] Use in Concierge Router (score > 3.5)
  [ ] Use with caution (score 2.5-3.5)
  [ ] Don't use (score < 2.5)

NEXT STEPS:
  [ ] Compare with other models
  [ ] Run spot-check validation on 5 tasks
  [ ] Update model registry
  [ ] Feed into Router selection logic
```

---

## Troubleshooting Checklist

### Script Fails at Startup

- [ ] Ollama running: `curl -v http://localhost:11434/api/tags`
- [ ] Model installed: `ollama list | grep gemma`
- [ ] Python path correct: `which python`
- [ ] Requirements installed: `pip list | grep requests`

### Model Response Doesn't Parse as JSON

- [ ] Check model is responding at all: `ollama run gemma4:26b "hello"`
- [ ] Try manually lowering temperature: `--temperature 0.3`
- [ ] Try increasing timeout: `--timeout 600`
- [ ] Check Ollama logs: `cat ~/.ollama/logs`

### Task Granularity Looks Wrong

- [ ] If all tasks > 8hr: Skeleton too complex? Try simpler test case
- [ ] If all tasks < 1hr: Skeleton too simple? Try more complex case
- [ ] If bimodal (many < 1hr AND many > 8hr): Decomposition quality issue
  - Clarify skeleton requirements
  - Test with different model
  - Consider scaffold/system prompt adjustment

### Self-Assessment Doesn't Make Sense

- [ ] Confidence 5/5 with "cannot_do" items: Model is miscalibrated
- [ ] All confidence 1/5: Model is underconfident or confused
- [ ] No risk areas identified: Model may be overconfident
- [ ] Risk areas don't match decomposition tasks: Model misunderstood prompt

### Comparison Shows Identical Scores

- [ ] Are you comparing different models? Check filenames
- [ ] Are you comparing same skeleton? Check input files
- [ ] Are both models even installed? `ollama list`
- [ ] If everything is identical: Normal behavior, both models decompose similarly

---

## Performance Benchmarks

Expected runtime on typical hardware:

| Model | Decomposition | Self-Assessment | Analysis | Total |
|-------|---------------|-----------------|----------|-------|
| Gemma 4 26B | 30-45s | 30-45s | 2-3s | ~2 min |
| Llama 2 70B | 60-90s | 60-90s | 2-3s | ~3-4 min |
| Mistral 7B | 20-30s | 20-30s | 2-3s | ~1-2 min |

(Times vary by hardware, Ollama configuration, network latency)

---

## File Manifest

### Scripts (Ready to Run)
- `eval_coding_decompose.py` — Stage 2: Decomposition
- `eval_coding_selfassess.py` — Stage 3: Self-Assessment
- `analyze_coding_audit.py` — Stage 4: Analysis & Registry

### Data
- `project_skeleton_stock_trading.json` — Test skeleton (ready to use)

### Documentation
- `CODING_DECOMPOSITION_SUITE_README.md` — Full guide (this directory)
- `QUICK_REFERENCE.md` — Quick reference (this file)

### Generated Output (After Running)
- `decomposition_[model].json` — Task decomposition results
- `selfassess_[model].json` — Self-assessment results
- `audit_report_[model].json` — Comprehensive audit report
- `registry_[model].json` — Concierge model registry entry

---

## Integration Checklist

Once audits are complete, integrate results into Concierge:

- [ ] Read audit_report_[model].json
- [ ] Understand strengths/weaknesses
- [ ] Create registry_[model].json entry
- [ ] Add to Concierge's model_registry.yaml
- [ ] Update Router's model selection logic
- [ ] Test Router with real decomposition tasks
- [ ] Document findings in project notes

---

## Common Questions

**Q: How often should I re-run audits?**  
A: When testing new models, new versions of models, or after modifying prompts. Once per model is usually sufficient unless you make significant changes.

**Q: Should I test on multiple skeletons?**  
A: Recommended. Test on at least 2-3 different projects to see if results are generalizable. Stock trading simulator is good baseline; add a web app skeleton and an infrastructure/DevOps skeleton.

**Q: What if all models score < 3.0?**  
A: Local models may not be suitable for decomposition tasks. Try:
  1. Smaller, more specific test case
  2. Better-structured skeleton (less ambiguous)
  3. System prompt/scaffolding to guide model
  4. Frontier model (Claude, Gemini) for baseline comparison

**Q: How do I use results in Concierge?**  
A: Router uses model registry to select which model to use for decomposition based on task requirements. High granularity score → use for fine-grained task lists. High self-awareness → use for risk assessment.

**Q: Can I run multiple audits in parallel?**  
A: Yes, if you have multiple Ollama instances or multiple GPUs. Just point to different hosts with `--host`.

---

## Deployment Checklist

Ready to deploy this suite to production use:

- [ ] All three scripts tested and working
- [ ] Sample audit completed (decomposition + selfassess + analysis)
- [ ] Results reviewed and understood
- [ ] Model registry entries created
- [ ] Documentation read
- [ ] Quick reference printed/bookmarked
- [ ] Spot-check validation done (optional but recommended)
- [ ] Concierge Router updated with registry entries
- [ ] Team members trained on how to run audits

---

## Support & Iteration

**If results look off:**
1. Check troubleshooting checklist above
2. Review CODING_DECOMPOSITION_SUITE_README.md for detailed guidance
3. Run spot-check validation on 5 tasks
4. Compare with frontier model baseline (Claude/Gemini)
5. Consider adjusting prompts or skeletons

**If you want to improve results:**
1. Create additional test skeletons in different domains
2. Experiment with system prompts or few-shot examples
3. Test different temperature settings (0.3 = deterministic, 0.7 = creative)
4. Compare local model results to frontier baselines
5. Iterate scaffold/prompt based on findings

---

## Version History

| Date | Status | Changes |
|------|--------|---------|
| 2026-04-13 | v1.0 Complete | Initial release: all 3 scripts + analysis + documentation |
| 2026-04-14 | v2.0 Architected | Red-team critique + resilience/scaffolding design complete; implementation roadmap ready |

---

## Next: Enki v2.0

v1.0 is production-ready. v2.0 design is complete and ready to implement.

**See:** `ENKI_V2_SUMMARY.md`, `ENKI_V2_ARCHITECTURE.md`, `ENKI_V2_IMPLEMENTATION_ROADMAP.md`

v2.0 adds:
- ✅ Semantic evaluation (LLM-as-judge)
- ✅ JSON auto-repair (pipeline resilience)
- ✅ Configurable infrastructure (timeouts, tokens)
- ✅ Scaffolding discovery (auto-retry with few-shot, CoT)

**Backward compatible:** Run v2.0 like v1.0 with optional flags.

---

*v1.0 is complete and ready to deploy. v2.0 roadmap is complete and ready to build. Start with Quick Reference above, then refer to full README for details.*
