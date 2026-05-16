================================================================================
ENKI — UPDATED & NEW FILES ONLY
================================================================================

Date: April 14, 2026
Contents: v1.0 files with v2.0 updates + v2.0 design documents

================================================================================
WHAT'S IN THIS EXPORT
================================================================================

UPDATED v1.0 FILES (3 files):
  - ENKI_GUIDE.md (updated with v2.0 appendix)
  - ENKI_MANIFEST.md (updated with v2.0 section)
  - ENKI_QUICK_REFERENCE.md (updated with v2.0 version history)

NEW v2.0 DESIGN DOCUMENTS (4 files):
  - ENKI_V2_SUMMARY.md (START HERE for v2.0)
  - ENKI_V2_ARCHITECTURE.md (technical design)
  - ENKI_V2_IMPLEMENTATION_ROADMAP.md (build plan)
  - ENKI_ROADMAP_INDEX.txt (quick reference)

Total: 7 files, 114 KB

================================================================================
WHAT CHANGED IN v1.0 FILES
================================================================================

ENKI_GUIDE.md:
  + Added "Appendix: ENKI v2.0 — The Resilience Pass" section
  + Explains 4 vulnerabilities addressed by v2.0
  + Links to v2.0 design documents

ENKI_MANIFEST.md:
  + Updated header to show v1.0 complete + v2.0 architected
  + Added "Enki v2.0 — The Resilience Pass" conclusion section
  + Lists v2.0 design documents and new features

ENKI_QUICK_REFERENCE.md:
  + Updated header with version info
  + Added v2.0 to version history table
  + Added "Next: Enki v2.0" section

================================================================================
HOW TO USE THESE FILES
================================================================================

1. INTEGRATE UPDATED FILES:
   Replace your existing v1.0 files with the updated versions:
   - ENKI_GUIDE.md
   - ENKI_MANIFEST.md
   - ENKI_QUICK_REFERENCE.md

2. ADD NEW v2.0 DOCUMENTS:
   Add the v2.0 design documents to your project:
   - ENKI_V2_SUMMARY.md
   - ENKI_V2_ARCHITECTURE.md
   - ENKI_V2_IMPLEMENTATION_ROADMAP.md
   - ENKI_ROADMAP_INDEX.txt

3. READ v2.0 DESIGN (Optional):
   To understand v2.0 improvements, read in order:
   - ENKI_V2_SUMMARY.md (5 min)
   - ENKI_V2_ARCHITECTURE.md (25 min)
   - ENKI_V2_IMPLEMENTATION_ROADMAP.md (20 min)

================================================================================
v1.0 vs v2.0
================================================================================

v1.0: COMPLETE & PRODUCTION-READY
  ✅ Three-stage pipeline (decompose → self-assess → analyze)
  ✅ All code implemented
  ✅ Ready to use immediately

v2.0: ARCHITECTED & READY TO BUILD
  📐 Four major improvements designed
  📐 Implementation roadmap complete (22-32 hours)
  📐 100% backward compatible with v1.0
  ⏳ Code not yet written (but fully specified)

================================================================================
THE FOUR v2.0 IMPROVEMENTS
================================================================================

1. SEMANTIC EVALUATION
   Problem:  Metrics are gameable (count tasks, not quality)
   Solution: LLM-as-judge grades decomposition quality
   Impact:   Catches useless micro-tasks

2. DECOUPLED PIPELINE
   Problem:  JSON error crashes entire pipeline
   Solution: JSON auto-repair + continue stages
   Impact:   Formatting issues ≠ capability issues

3. INFRASTRUCTURE RESILIENCE
   Problem:  Hardcoded timeouts fail on slow hardware
   Solution: Configurable timeouts, token limits, temperature
   Impact:   Fair comparison across hardware

4. SCAFFOLDING DISCOVERY
   Problem:  Models marked unsuitable if they need scaffolding
   Solution: Auto-retry with few-shot → CoT if needed
   Impact:   Discover what each model needs

================================================================================
QUICK START FOR v2.0
================================================================================

To understand v2.0:
  1. Read ENKI_V2_SUMMARY.md (5 minutes)
  2. Read ENKI_V2_ARCHITECTURE.md (25 minutes)
  3. Read ENKI_V2_IMPLEMENTATION_ROADMAP.md (20 minutes)

To implement v2.0:
  1. Understand the design above
  2. Follow Phase 1-5 in ENKI_V2_IMPLEMENTATION_ROADMAP.md
  3. Estimated effort: 22-32 hours

v2.0 is 100% backward compatible with v1.0:
  - All features are optional
  - Run with --max-scaffolding-level 0 to get v1.0 behavior
  - Run without --evaluator-model to use v1.0 scoring

================================================================================
FILE MANIFEST
================================================================================

Updated (replace your existing files):
  ✎ ENKI_GUIDE.md (22 KB)
  ✎ ENKI_MANIFEST.md (17 KB)
  ✎ ENKI_QUICK_REFERENCE.md (14 KB)

New (add to your project):
  + ENKI_V2_SUMMARY.md (12 KB)
  + ENKI_V2_ARCHITECTURE.md (18 KB)
  + ENKI_V2_IMPLEMENTATION_ROADMAP.md (14 KB)
  + ENKI_ROADMAP_INDEX.txt (11 KB)

Total: 7 files, 114 KB

================================================================================
INTEGRATION STEPS
================================================================================

In your project directory where you have v1.0 files:

1. Backup originals (optional):
   cp ENKI_GUIDE.md ENKI_GUIDE.md.bak
   cp ENKI_MANIFEST.md ENKI_MANIFEST.md.bak
   cp ENKI_QUICK_REFERENCE.md ENKI_QUICK_REFERENCE.md.bak

2. Replace updated files:
   cp ENKI_GUIDE.md <your_project>/
   cp ENKI_MANIFEST.md <your_project>/
   cp ENKI_QUICK_REFERENCE.md <your_project>/

3. Add new v2.0 documents:
   cp ENKI_V2_*.md <your_project>/
   cp ENKI_ROADMAP_INDEX.txt <your_project>/

4. Done! Your project now has:
   - v1.0 ready to use (unchanged, just docs updated)
   - v2.0 design documents for future implementation

================================================================================
QUESTIONS?
================================================================================

Read the documents in this order:
  1. ENKI_V2_SUMMARY.md (what's new, why it matters)
  2. ENKI_V2_ARCHITECTURE.md (how it works)
  3. ENKI_V2_IMPLEMENTATION_ROADMAP.md (how to build it)

All questions should be answered in these three documents.

================================================================================
Created: April 14, 2026
Ready to integrate: Yes
================================================================================
