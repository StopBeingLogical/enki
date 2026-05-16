# Enki — Session Seed & Instructions

**Project:** Enki v1.0 (Production) + v2.0 (Architected)  
**Status:** v1.0 complete; v2.0 implementation ready  
**Maintenance:** Changelog system in `.changelog/UNRELEASED.md`

---

## Session Start Checklist

When you start a session on Enki:

1. **Load project context** (3 min)
   - Read `README.md` (quick-start guide)
   - Read `docs/ENKI_QUICK_REFERENCE.md` if implementing

2. **Check for changelog updates** (1 min)
   - Ask: "Should I consolidate pending changelog entries from `.changelog/UNRELEASED.md` into the appropriate CHANGELOG.md files?"
   - If yes: move one-liners to their destination files and reset UNRELEASED.md
   - If no: continue

3. **Navigate by task**
   - **v1.0 usage:** See `docs/ENKI_GUIDE.md` and `docs/ENKI_QUICK_REFERENCE.md`
   - **v2.0 implementation:** Start with `docs/ENKI_V2_SUMMARY.md` (5 min), then `docs/ENKI_V2_ARCHITECTURE.md` (25 min)

---

## Changelog Maintenance

**Location:** `.changelog/UNRELEASED.md` (working file), `**/CHANGELOG.md` (committed files)

**When making changes:**
- Add one-liners to `.changelog/UNRELEASED.md` under the relevant section
- At session start, I'll ask if you want to consolidate entries
- Before committing, I'll move entries to the appropriate CHANGELOG.md files

---

## Key Information

### Enki v1.0 (Production-Ready)
- Three-stage pipeline: Decompose → Self-Assess → Analyze
- Fully implemented in `src/`
- Comprehensive documentation in `docs/`
- Use: `python src/enki_stage2_decompose.py --model <name> --skeleton <skeleton.json>`

### Enki v2.0 (Architected, Ready to Build)
- Four major improvements:
  1. **Semantic Evaluation** — LLM-as-judge grades decomposition quality
  2. **Decoupled Pipeline** — JSON auto-repair, continues on formatting errors
  3. **Infrastructure Resilience** — Configurable timeouts, token limits, temperature
  4. **Scaffolding Discovery** — Auto-retry with few-shot → CoT if needed

- Implementation roadmap: 22–32 hours across 5 phases
- 100% backward compatible with v1.0
- See `docs/ENKI_V2_IMPLEMENTATION_ROADMAP.md` for detailed phases

### Integration with Concierge
- Enki is used to evaluate models for Concierge's Bit layer (interactive chat interface)
- Model selection research: `../concierge/docs/research/bit-model-selection/`
- Enki is a general-purpose tool, not Concierge-specific

---

## Quick Links

| I want to... | Go to... |
|---|---|
| Use Enki v1.0 | `docs/ENKI_GUIDE.md` |
| Quick reference | `docs/ENKI_QUICK_REFERENCE.md` |
| Understand v2.0 | `docs/ENKI_V2_SUMMARY.md` |
| Implement v2.0 | `docs/ENKI_V2_IMPLEMENTATION_ROADMAP.md` |
| See current status | `CHANGELOG.md` |

---

## Repository & Contact

**Parent:** `~/nextcloud/Mneme/code/enki/`  
**Related:** Concierge project at `../concierge/`  
**Last updated:** April 22, 2026
