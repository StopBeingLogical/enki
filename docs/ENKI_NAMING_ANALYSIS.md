# Coding Decomposition Test Suite — Identity & Naming Analysis
**Per:** identity-naming-v1.0  
**Date:** April 13, 2026  
**Status:** Naming recommendations ready

---

## Domain Classification

**The test suite is SOFTWARE** (Sumerian naming root)

### Reasoning

| Criterion | Analysis |
|-----------|----------|
| **Form** | Python scripts + JSON analysis tools |
| **Purpose** | Codebases, scripts, and standalone applications |
| **Persistence** | Runs independently; not ephemeral layer |
| **Role** | Model evaluation and capability auditing |

→ **Domain: SOFTWARE** → **Root: Sumerian**

---

## What Gets Named (vs. What Doesn't)

Per the naming guide: *"No unique names for ephemeral layers (Foreman/Workbee); these use derived IDs."*

### Framework Level (Gets a Name)

The suite as a whole is a **standalone software system**:
- Scripts that run independently
- Persistent role: model evaluation and capability auditing
- Not ephemeral; reused across many audits

**Recommendation:** Name the framework itself

### Component Level (Use Descriptive Names, Not Mythological)

Individual scripts are **tools within the framework**:
- `eval_coding_decompose.py` — Does one thing (decomposition)
- `eval_coding_selfassess.py` — Does one thing (self-assessment)
- `analyze_coding_audit.py` — Does one thing (analysis)

**Recommendation:** Keep descriptive names for scripts (they're functional components, not standalone systems)

### Output Level (Use Derived IDs)

Audit results are **ephemeral instances**:
- `decomposition_gemma4.json` — Result of one run
- `selfassess_gemma4.json` — Result of one run
- `audit_report_gemma4.json` — Result of one run

**Recommendation:** Keep timestamp/model-based IDs (not mythological names)

---

## Naming Options for the Framework

If you want to name the **framework itself** (the software system that does model auditing):

### Option A: Single Sumerian Name (Minimal Approach)

**Name the framework:** Pick ONE Sumerian name for the entire suite

Examples of Sumerian deities/concepts:
- **Enki** — God of wisdom, knowledge, and water. *"Enki audits and evaluates models."*
- **Nisaba** — Goddess of writing, wisdom, and accounting. *"Nisaba measures and records model capability."*
- **Ninhursag** — Mother earth; associated with creation and assessment. *"Ninhursag brings models into being by assessing them."*
- **Utu** — God of justice and truth. *"Utu reveals true model capability."*

**Usage:**
```
The Enki evaluation suite
  → eval_coding_decompose.py
  → eval_coding_selfassess.py
  → analyze_coding_audit.py
```

**Advantage:** Clean, single identity. Mirrors how "Concierge" names the main system.

---

### Option B: Sumerian Names for Each Script (Modular Approach)

Name each script individually with Sumerian names reflecting its function:

| Script | Role | Sumerian Mapping | Name Option |
|--------|------|------------------|-------------|
| `eval_coding_decompose.py` | Breaks down (separates) | Division, components | **Kesh** (assembly, component) |
| `eval_coding_selfassess.py` | Model looks inward | Self-knowledge, introspection | **Namtar** (destiny, self-knowledge) |
| `analyze_coding_audit.py` | Judges and records | Judgment, measurement | **Nanshe** (justice, divination) |

**Usage:**
```
Kesh — Project decomposition
Namtar — Model self-assessment
Nanshe — Audit analysis and judgment
```

**Advantage:** Each tool has semantic identity. Clear role mapping.

**Disadvantage:** More complex; loses cohesion as "one system."

---

### Option C: Sumerian Name + Descriptive English (Hybrid)

Keep descriptive names but prepend Sumerian names:

```
Enki-Decompose (decomposition stage)
Enki-Selfassess (self-assessment stage)
Enki-Analyze (analysis stage)
```

**Advantage:** Mythological identity + functional clarity

**Disadvantage:** Verbose; may be unnecessary

---

## Recommendation

### **Primary Recommendation: Option A (Single Sumerian Name)**

**The framework is named:** **ENKI**

**Rationale:**
- Enki = god of wisdom, knowledge, deep understanding
- Perfectly aligned with "evaluating model wisdom and capability"
- Single identity mirrors Concierge's naming approach (one name for the system)
- Scales cleanly if you add more evaluation suites later (Enki for model evaluation, Nisaba for documentation evaluation, etc.)

**Usage:**
```
ENKI — The Model Evaluation Suite
  Stage 2: eval_coding_decompose.py (decomposition)
  Stage 3: eval_coding_selfassess.py (self-assessment)
  Stage 4: analyze_coding_audit.py (aggregation & analysis)

Example output:
  enki_audit_gemma4_20260413.json
  enki_registry_gemma4.json
  enki_comparison_gemma_vs_llama.json
```

### **Alternative: Option B (Modular Names)**

If you want **each script to have a distinct identity**:

**Kesh** — Decomposition  
**Namtar** — Self-Assessment  
**Nanshe** — Analysis  

**Reasoning:** These form a **three-stage pipeline** with distinct responsibilities, so they could each have names. This parallels Concierge's five-layer architecture (Bit, Planner, Router, Foreman, Workbee).

**Usage:**
```
kesh_decomposition_gemma4.json
namtar_selfassess_gemma4.json
nanshe_audit_report_gemma4.json
```

---

## Implementation

### If You Choose ENKI (Recommended)

Update documentation and output filenames:

```bash
# Script header comment
"""
ENKI — The Model Evaluation Suite
Stage 2: Project Decomposition

Evaluates how well local models can break down software projects.
"""

# Output files
enki_decomposition_[model].json
enki_selfassess_[model].json
enki_audit_report_[model].json
enki_registry_[model].json
```

### If You Choose Modular (Kesh/Namtar/Nanshe)

```bash
# Script files (keep names for clarity)
eval_coding_decompose.py       # KESH
eval_coding_selfassess.py      # NAMTAR
analyze_coding_audit.py        # NANSHE

# Output files
kesh_decomposition_[model].json
namtar_selfassess_[model].json
nanshe_audit_[model].json
```

---

## Alignment with identity-naming-v1.0

### Domain: ✅ SOFTWARE (Sumerian)

- Scripts are codebases/standalone applications
- Persistent role (model evaluation)
- Not ephemeral (reused across audits)

### Invariant Compliance: ✅

- ✅ Named for the **role** (model evaluation), not hardware specs
- ✅ Names persist across runs
- ✅ Respects "no unique names for ephemeral outputs" (audit results use derived IDs, not mythological names)

### Categorical Recognition: ✅

- Sumerian name immediately identifies as **software/tool**
- Distinguishable from hardware (Greek/Latin), writing (Egyptian)
- Fits within Concierge ecosystem

---

## Decision Matrix

| Approach | Pros | Cons | Recommendation |
|----------|------|------|-----------------|
| **ENKI (single)** | Clean, cohesive, scalable | Less granular | ⭐ PRIMARY |
| **Kesh/Namtar/Nanshe** | Semantic clarity, layer parallelism | More complex, verbose | ALTERNATIVE |
| **Keep descriptive names** | No change needed, clear | Violates naming convention | NOT RECOMMENDED |

---

## Final Recommendation

**Name the framework: ENKI**

This gives the test suite:
- ✅ Proper Sumerian identity (software domain)
- ✅ Semantic alignment (god of wisdom/capability)
- ✅ Compliance with identity-naming-v1.0
- ✅ Scalability (more evaluation suites can follow)
- ✅ Clean integration with Concierge ecosystem

---

## Changelog

- **2026-04-14:** v1.0 Naming analysis. Recommended ENKI as framework name, compliance with identity-naming-v1.0.

---

*Naming analysis complete. Ready to implement.*
