# Enki — Model Evaluation Framework

**Version:** v1.0 (Production) + v2.0 (Architected) | **Last Updated:** April 2026

Enki is a systematic model evaluation framework for assessing LLM capabilities through structured decomposition, self-assessment, and semantic analysis. Originally designed to evaluate models for Concierge, it's a general-purpose tool applicable to any LLM testing scenario.

## Quick Start

### What Enki Does

Enki runs models through a three-stage pipeline:

1. **Decompose** — Break a complex task into subtasks. Grades on granularity and reasoning.
2. **Self-Assess** — Model evaluates its own decomposition. Detects overconfidence.
3. **Analyze** — Comprehensive audit comparing model output against rubric.

**Output:** Structured report with metrics, recommendations, and registry entry for model tracking.

### Try It

```bash
python src/enki_stage2_decompose.py --model <model-name> --skeleton docs/project_skeleton_stock_trading.json
python src/enki_stage3_selfassess.py --model <model-name> --decomposition <output.json>
python src/enki_stage4_analyze.py --decomposition <output.json> --selfassess <selfassess.json>
```

See `docs/ENKI_QUICK_REFERENCE.md` for examples and metric interpretation.

## Documentation

| Document | Purpose |
|----------|---------|
| `docs/ENKI_GUIDE.md` | Complete user guide with examples |
| `docs/ENKI_MANIFEST.md` | What's included, feature checklist |
| `docs/ENKI_V2_SUMMARY.md` | What's new in v2.0 (semantic eval, resilience improvements) |
| `docs/ENKI_V2_ARCHITECTURE.md` | v2.0 technical design and implementation details |
| `docs/ENKI_V2_IMPLEMENTATION_ROADMAP.md` | Step-by-step build plan for v2.0 (22–32 hours) |

**Start here:** `ENKI_V2_SUMMARY.md` (5 min) → `ENKI_GUIDE.md` (detailed walkthrough)

## Status

| Version | Status | Notes |
|---------|--------|-------|
| **v1.0** | ✅ Production Ready | Three-stage pipeline, fully implemented, deployable now |
| **v2.0** | 📐 Architected | Design complete; adds semantic evaluation, JSON resilience, configurable timeouts, scaffolding discovery. Backward compatible. |

## Integration with Concierge

Enki is used by Concierge to evaluate candidate models for the Bit layer (interactive chat interface). See `../concierge/docs/research/bit-model-selection/` for model evaluation results and methodology.

## Key Features

- **v1.0:** Structured decomposition pipeline, confidence scoring, granularity metrics
- **v2.0 (designed):** LLM-as-judge semantic grading, JSON auto-repair, hardware-agnostic timeouts, multi-tiered scaffolding, failure classification

## License

Personal research project. See parent Concierge project for license information.
