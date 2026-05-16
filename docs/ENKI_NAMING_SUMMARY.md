# Enki — Naming Implementation Summary
**Date:** April 14, 2026  
**Status:** ✅ Complete  
**Identity:** Software (Sumerian domain per identity-naming-v1.0)

---

## What Changed

All files have been updated to use **Enki** as the official framework name for the model evaluation suite.

### Framework Identity

**Name:** Enki  
**Etymology:** Sumerian god of wisdom, knowledge, and deep understanding  
**Domain:** Software (per identity-naming-v1.0)  
**Purpose:** Model capability evaluation and auditing  

---

## File Updates

### Documentation

| File | Changes |
|------|---------|
| `MANIFEST.md` | ✅ Title updated; branded as "Enki — Model Evaluation Suite" |
| `CODING_DECOMPOSITION_SUITE_README.md` | ✅ Title updated; Enki branding throughout; example filenames use `enki_` prefix |
| `QUICK_REFERENCE.md` | ✅ Title updated; Enki branding; examples use `enki_` prefix |
| `NAMING_ANALYSIS.md` | ✅ New document; explains Enki naming choice per identity-naming-v1.0 |
| `ENKI_NAMING_SUMMARY.md` | ✅ This document |

### Python Scripts

Each script updated with Enki header docstring:

| Script | Header Updated | Enki Stage |
|--------|-----------------|-----------|
| `eval_coding_decompose.py` | ✅ | Stage 2: Decomposition |
| `eval_coding_selfassess.py` | ✅ | Stage 3: Self-Assessment |
| `analyze_coding_audit.py` | ✅ | Stage 4: Analysis & Registry |

### Output Filenames

Examples updated throughout documentation:

**Old naming:**
```
decomposition_gemma4.json
selfassess_gemma4.json
audit_report_gemma4.json
registry_gemma4.json
```

**New naming (Enki):**
```
enki_decomposition_gemma4.json
enki_selfassess_gemma4.json
enki_audit_report_gemma4.json
enki_registry_gemma4.json
```

---

## Usage Examples Updated

### Quick Start

```bash
# Enki Stage 2 (Decomposition)
python eval_coding_decompose.py \
  --model gemma4:26b \
  --skeleton project_skeleton_stock_trading.json \
  --output enki_decomposition_gemma4.json

# Enki Stage 3 (Self-Assessment)
python eval_coding_selfassess.py \
  --model gemma4:26b \
  --decomposition enki_decomposition_gemma4.json \
  --output enki_selfassess_gemma4.json

# Enki Stage 4 (Analysis)
python analyze_coding_audit.py \
  --decomposition enki_decomposition_gemma4.json \
  --selfassess enki_selfassess_gemma4.json \
  --output enki_audit_report_gemma4.json \
  --registry-entry enki_registry_gemma4.json
```

### Comparison

```bash
python analyze_coding_audit.py \
  --decomposition enki_decomposition_gemma4.json \
  --selfassess enki_selfassess_gemma4.json \
  --output enki_audit_report_gemma4.json \
  --compare-with enki_audit_report_llama2.json
```

---

## Architecture: Enki Four-Stage Pipeline

```
Enki Stage 1: Frontier Model Sketch (Manual)
  Input: User intent ("Build a stock trading simulator...")
  Output: project_skeleton.json
  
  ↓
  
Enki Stage 2: Local Model Decomposition (eval_coding_decompose.py)
  Input: project_skeleton.json
  Output: enki_decomposition_[model].json
  Measures: Task granularity, assumptions, dependencies
  
  ↓
  
Enki Stage 3: Model Self-Assessment (eval_coding_selfassess.py)
  Input: enki_decomposition_[model].json
  Output: enki_selfassess_[model].json
  Measures: Per-category confidence, capability boundaries, risk areas
  
  ↓
  
Enki Stage 4: Analysis & Registry (analyze_coding_audit.py)
  Input: enki_decomposition_[model].json + enki_selfassess_[model].json
  Output: enki_audit_report_[model].json + enki_registry_[model].json
  Measures: Composite score, key findings, comparison (optional)
```

---

## Identity Compliance

Per **identity-naming-v1.0**:

✅ **Domain:** Software (Sumerian cultural root)  
✅ **Purpose:** Codebases, scripts, and standalone applications  
✅ **Persistence:** Persistent role (model evaluation), not ephemeral  
✅ **Role-based naming:** Named for the role (model evaluation), not hardware specs  
✅ **Immediate categorical recognition:** Sumerian name identifies as software tool  
✅ **Scalability:** Can expand to Nisaba (documentation evaluation), etc.  

---

## Integration with Concierge

Enki generates Concierge model registry entries in the format:

```yaml
# In Concierge's model_registry.yaml

models:
  gemma4:26b:
    enki_audit_score: 3.5
    enki_decomposition: 3.8/5
    enki_self_awareness: 3.2/5
    enki_strengths: [accurate_granularity, identifies_ambiguities]
    enki_weaknesses: [many_assumptions]
    enki_best_for: [task_decomposition, dependency_analysis]
    enki_avoid_for: [ambiguous_specs]
```

Concierge Router uses these to select the best model for decomposition work.

---

## What Stays the Same

The following elements remain unchanged:

- **Script functionality:** Scripts work exactly as before
- **Input/output formats:** JSON structure unchanged
- **Metrics and scoring:** Same calculation logic
- **Reference skeleton:** `project_skeleton_stock_trading.json` unchanged
- **Command syntax:** Only example filenames changed in documentation

**No code changes required to any of the three scripts.** Only documentation and output filename examples were updated.

---

## Directory Structure (Recommended)

```
concierge/eval_framework/
├── README.md                           # Enki guide
├── QUICK_REFERENCE.md                  # Enki quick card
├── NAMING_ANALYSIS.md                  # Enki naming rationale
├── MANIFEST.md                         # Enki manifest
├── ENKI_NAMING_SUMMARY.md              # This document
│
├── eval_coding_decompose.py            # Enki Stage 2
├── eval_coding_selfassess.py           # Enki Stage 3
├── analyze_coding_audit.py             # Enki Stage 4
│
├── templates/
│   └── project_skeleton_stock_trading.json
│
├── results/
│   ├── enki_decomposition_gemma4.json
│   ├── enki_selfassess_gemma4.json
│   ├── enki_audit_report_gemma4.json
│   ├── enki_registry_gemma4.json
│   ├── enki_decomposition_llama2.json
│   ├── enki_selfassess_llama2.json
│   ├── enki_audit_report_llama2.json
│   ├── enki_registry_llama2.json
│   └── enki_comparison_gemma_vs_llama.json
│
└── registry/
    └── model_registry.yaml             # Concierge integration
```

---

## Migration Checklist

If you're updating from old naming to Enki:

- [ ] Read NAMING_ANALYSIS.md to understand the choice
- [ ] Update any scripts referencing old filenames to use `enki_` prefix
- [ ] Update Concierge Router configuration if needed
- [ ] Create enki_results/ directory for output files
- [ ] Run first Enki audit on baseline model (Gemma 4 26B)
- [ ] Verify output filenames have `enki_` prefix
- [ ] Add Enki audit results to Concierge model registry
- [ ] Document Enki in your project's naming guide

---

## Next Steps

1. **Deploy Enki:** Use scripts in your evaluation workflow
2. **Run baseline audit:** Execute on Gemma 4 26B and Llama 2 70B
3. **Review results:** Check `enki_audit_report_*.json` files
4. **Update registry:** Add `enki_registry_*.json` entries to Concierge
5. **Iterate:** Test on additional models as they become available

---

## Support

- **Full guide:** See CODING_DECOMPOSITION_SUITE_README.md
- **Quick reference:** See QUICK_REFERENCE.md
- **Naming rationale:** See NAMING_ANALYSIS.md
- **Manifest:** See MANIFEST.md

---

## Version History

| Date | Version | Status | Event |
|------|---------|--------|-------|
| 2026-04-13 | v1.0 | Complete | Initial release (unnamed) |
| 2026-04-14 | v1.0-enki | Complete | Enki naming implementation |

---

*Enki naming implementation complete. All files updated and ready to deploy.*
