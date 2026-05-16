#!/usr/bin/env python3
"""
Enki — Model Evaluation Suite
Stage 4: Analysis & Registry Integration

Aggregates and analyzes results from decomposition and self-assessment stages.
Produces comprehensive audit reports and Concierge model registry entries.

Enki is the Sumerian god of wisdom and knowledge.
This stage synthesizes insights about model capability into actionable registry entries.

Part of the three-stage evaluation pipeline:
  Stage 1: Frontier models synthesize project skeleton (manual)
  Stage 2: Local model decomposes skeleton into atomic tasks (eval_coding_decompose.py)
  Stage 3: Local model self-assesses its own capability (eval_coding_selfassess.py)
  Stage 4: Analysis and registry integration (this script)

Usage:
  python analyze_coding_audit.py \
    --decomposition decomposition_gemma4.json \
    --selfassess selfassess_gemma4.json \
    --output audit_report_gemma4.json

Optional:
  --skeleton project_skeleton.json (for reference/validation)
  --compare-with model2_audit_report.json (to compare two models side-by-side)

Requirements:
  pip install requests (for stats calculations)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────

def load_json_file(path: str) -> dict:
    """Load JSON file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(p.read_text(encoding="utf-8"))


def calculate_statistics(values: List[float]) -> dict:
    """Calculate basic statistics for a list of values."""
    if not values:
        return {"mean": 0, "median": 0, "min": 0, "max": 0, "count": 0}
    
    sorted_vals = sorted(values)
    count = len(sorted_vals)
    mean = sum(sorted_vals) / count
    median = sorted_vals[count // 2] if count % 2 == 1 else (sorted_vals[count // 2 - 1] + sorted_vals[count // 2]) / 2
    
    return {
        "count": count,
        "mean": round(mean, 2),
        "median": round(median, 2),
        "min": round(sorted_vals[0], 2),
        "max": round(sorted_vals[-1], 2),
    }


# ─────────────────────────────────────────────
# Decomposition Analysis
# ─────────────────────────────────────────────

def analyze_decomposition(decomp_data: dict) -> dict:
    """Analyze decomposition results."""
    
    decomposition = decomp_data.get("decomposition_result", {}).get("decomposition", {})
    if not decomposition:
        return {"success": False, "error": "No decomposition data"}
    
    analysis = {
        "model": decomp_data.get("model", "unknown"),
        "skeleton": decomp_data.get("skeleton_title", "unknown"),
        "decomposition_analysis": {},
    }
    
    # Task collection
    all_tasks = []
    task_hours = []
    dependency_counts = []
    
    for module_name, module_data in decomposition.get("module_decomposition", {}).items():
        for task in module_data.get("atomic_tasks", []):
            all_tasks.append(task)
            hours = task.get("estimated_hours", 0)
            task_hours.append(hours)
            deps = len(task.get("dependencies", []))
            dependency_counts.append(deps)
    
    # Task granularity
    granularity = {
        "total_tasks": len(all_tasks),
        "hours_statistics": calculate_statistics(task_hours),
        "distribution": {
            "under_1hr": len([h for h in task_hours if h < 1]),
            "1_to_4hr": len([h for h in task_hours if 1 <= h <= 4]),
            "4_to_8hr": len([h for h in task_hours if 4 < h <= 8]),
            "over_8hr": len([h for h in task_hours if h > 8]),
        },
        "total_estimated_hours": sum(task_hours),
    }
    
    # Add percentages
    total = granularity["total_tasks"]
    if total > 0:
        for key in granularity["distribution"]:
            count = granularity["distribution"][key]
            pct = round((count / total) * 100, 1)
            granularity[f"{key}_pct"] = pct
    
    analysis["decomposition_analysis"]["task_granularity"] = granularity
    
    # Dependency analysis
    analysis["decomposition_analysis"]["dependency_analysis"] = {
        "tasks_with_dependencies": len([d for d in dependency_counts if d > 0]),
        "tasks_without_dependencies": len([d for d in dependency_counts if d == 0]),
        "average_dependencies_per_task": round(sum(dependency_counts) / len(dependency_counts), 2) if dependency_counts else 0,
        "max_dependencies": max(dependency_counts) if dependency_counts else 0,
    }
    
    # Assumptions and questions
    analysis["decomposition_analysis"]["assumptions_and_questions"] = {
        "unstated_assumptions": decomposition.get("unstated_assumptions", []),
        "assumptions_count": len(decomposition.get("unstated_assumptions", [])),
        "questions_should_have_asked": decomposition.get("questions_you_should_have_asked", []),
        "questions_count": len(decomposition.get("questions_you_should_have_asked", [])),
    }
    
    # Model confidence
    analysis["decomposition_analysis"]["model_confidence"] = decomposition.get("confidence_in_decomposition", 0)
    
    # Milestones
    analysis["decomposition_analysis"]["milestones"] = decomposition.get("milestones", [])
    
    return analysis


# ─────────────────────────────────────────────
# Self-Assessment Analysis
# ─────────────────────────────────────────────

def analyze_selfassess(selfassess_data: dict) -> dict:
    """Analyze self-assessment results."""
    
    assessment = selfassess_data.get("selfassess_result", {}).get("assessment", {})
    if not assessment:
        return {"success": False, "error": "No assessment data"}
    
    analysis = {
        "model": selfassess_data.get("model", "unknown"),
        "project": selfassess_data.get("project_title", "unknown"),
        "selfassess_analysis": {},
    }
    
    # Overall confidence
    analysis["selfassess_analysis"]["overall_confidence"] = assessment.get("overall_project_confidence", 0)
    
    # Per-category analysis
    categories = {}
    confidence_scores = []
    
    for category, cat_data in assessment.get("self_assessment_by_category", {}).items():
        confidence = cat_data.get("confidence", 0)
        confidence_scores.append(confidence)
        
        categories[category] = {
            "confidence": confidence,
            "can_produce_code": cat_data.get("can_produce_working_code", "unknown"),
            "assumptions": len(cat_data.get("assumptions", [])),
            "blocking_constraints": len(cat_data.get("blocking_constraints", [])),
            "blocking_constraint_list": cat_data.get("blocking_constraints", []),
            "tests_would_skip": cat_data.get("tests_would_skip", []),
        }
    
    analysis["selfassess_analysis"]["by_category"] = categories
    analysis["selfassess_analysis"]["average_category_confidence"] = round(
        sum(confidence_scores) / len(confidence_scores), 2
    ) if confidence_scores else 0
    
    # Capability boundaries
    capabilities = assessment.get("capability_boundaries", {})
    analysis["selfassess_analysis"]["capability_boundaries"] = {
        "can_do": capabilities.get("can_do", []),
        "partial": capabilities.get("partial", []),
        "cannot_do": capabilities.get("cannot_do", []),
        "summary": f"{len(capabilities.get('can_do', []))} can_do, {len(capabilities.get('partial', []))} partial, {len(capabilities.get('cannot_do', []))} cannot_do",
    }
    
    # Risk areas
    analysis["selfassess_analysis"]["risk_areas"] = {
        "count": len(assessment.get("biggest_risk_areas", [])),
        "areas": assessment.get("biggest_risk_areas", []),
    }
    
    # Recommendations
    analysis["selfassess_analysis"]["recommendations"] = assessment.get("recommendations_for_safer_usage", [])
    
    return analysis


# ─────────────────────────────────────────────
# Comprehensive Report
# ─────────────────────────────────────────────

def build_comprehensive_report(
    decomp_analysis: dict,
    selfassess_analysis: dict,
) -> dict:
    """Build comprehensive audit report."""
    
    report = {
        "audit_type": "comprehensive_coding_audit",
        "model": decomp_analysis.get("model", selfassess_analysis.get("model", "unknown")),
        "project": decomp_analysis.get("skeleton", selfassess_analysis.get("project", "unknown")),
        "decomposition": decomp_analysis,
        "self_assessment": selfassess_analysis,
    }
    
    # Calculate overall scores
    decomp_granularity = decomp_analysis.get("decomposition_analysis", {}).get("task_granularity", {})
    granularity_score = decomp_granularity.get("1_to_4hr_pct", 0) / 100  # 0-1 scale
    
    # Penalize extreme granularity
    if decomp_granularity.get("under_1hr_pct", 0) > 30:
        granularity_score *= 0.8
    if decomp_granularity.get("over_8hr_pct", 0) > 20:
        granularity_score *= 0.8
    
    selfassess_confidence = selfassess_analysis.get("selfassess_analysis", {}).get("overall_confidence", 0) / 5
    
    # Composite score (0-1)
    composite_score = round((granularity_score * 0.5 + selfassess_confidence * 0.5) * 5, 2)
    
    report["overall_scores"] = {
        "task_granularity_score": round(granularity_score * 5, 2),
        "self_awareness_score": round(selfassess_confidence * 5, 2),
        "composite_score": composite_score,
        "notes": "Granularity heavily weighted on 1-4 hour target. Self-awareness evaluated on realistic confidence.",
    }
    
    # Key findings
    findings = []
    
    # Granularity finding
    target_pct = decomp_granularity.get("1_to_4hr_pct", 0)
    if target_pct >= 65:
        findings.append(f"✓ Task granularity excellent: {target_pct}% in target 1-4 hour range")
    elif target_pct >= 50:
        findings.append(f"⚠ Task granularity acceptable: {target_pct}% in target range (aim for 65%+)")
    else:
        findings.append(f"✗ Task granularity too coarse/fine: only {target_pct}% in target range")
    
    # Assumption finding
    assumption_count = decomp_analysis.get("decomposition_analysis", {}).get("assumptions_and_questions", {}).get("assumptions_count", 0)
    if assumption_count <= 2:
        findings.append(f"✓ Few unstated assumptions: {assumption_count} (good)")
    elif assumption_count <= 5:
        findings.append(f"⚠ Moderate assumptions: {assumption_count} (reasonable for complex project)")
    else:
        findings.append(f"✗ Many assumptions: {assumption_count} (model should have asked clarifying questions)")
    
    # Dependency finding
    total_tasks = decomp_analysis.get("decomposition_analysis", {}).get("task_granularity", {}).get("total_tasks", 0)
    tasks_with_deps = decomp_analysis.get("decomposition_analysis", {}).get("dependency_analysis", {}).get("tasks_with_dependencies", 0)
    if total_tasks > 0:
        dep_pct = (tasks_with_deps / total_tasks) * 100
        if dep_pct >= 70:
            findings.append(f"✓ Good dependency coverage: {dep_pct:.0f}% of tasks have explicit dependencies")
        else:
            findings.append(f"⚠ Sparse dependency graph: {dep_pct:.0f}% have dependencies (may indicate missing structure)")
    
    # Self-awareness finding
    avg_confidence = selfassess_analysis.get("selfassess_analysis", {}).get("average_category_confidence", 0)
    cannot_do_count = len(selfassess_analysis.get("selfassess_analysis", {}).get("capability_boundaries", {}).get("cannot_do", []))
    
    if avg_confidence >= 3.5 and cannot_do_count >= 2:
        findings.append(f"✓ Good self-awareness: realistic confidence ({avg_confidence}/5) with identified limitations")
    elif avg_confidence <= 2.5:
        findings.append(f"⚠ Low model confidence: {avg_confidence}/5 (realistic? consider smaller projects)")
    else:
        findings.append(f"⚠ Mixed self-awareness: confidence {avg_confidence}/5, {cannot_do_count} clear limitation areas")
    
    report["key_findings"] = findings
    
    return report


# ─────────────────────────────────────────────
# Model Registry Entry
# ─────────────────────────────────────────────

def build_registry_entry(report: dict) -> dict:
    """Build Concierge model registry entry from audit report."""
    
    model = report.get("model", "unknown")
    composite = report.get("overall_scores", {}).get("composite_score", 0)
    
    # Extract key metrics
    decomp = report.get("decomposition", {}).get("decomposition_analysis", {})
    selfassess = report.get("self_assessment", {}).get("selfassess_analysis", {})
    
    registry_entry = {
        "model": model,
        "category": "coding_decomposition",
        "audit_score": composite,
        "audit_date": "2026-04-13",  # TODO: use actual date
        "test_results": {
            "task_granularity": decomp.get("task_granularity", {}).get("1_to_4hr_pct", 0),
            "dependency_coverage": decomp.get("dependency_analysis", {}).get("tasks_with_dependencies", 0),
            "assumption_awareness": 5 - min(decomp.get("assumptions_and_questions", {}).get("assumptions_count", 0), 5),
            "self_awareness": selfassess.get("overall_confidence", 0),
        },
        "strengths": [],
        "weaknesses": [],
        "best_for": [
            "breaking down projects into tasks",
            "generating task dependencies",
        ],
        "avoid_for": [
            "highly ambiguous requirements",
            "novel/cutting-edge architectures",
        ],
    }
    
    # Populate strengths/weaknesses based on metrics
    granularity_pct = decomp.get("task_granularity", {}).get("1_to_4hr_pct", 0)
    if granularity_pct >= 65:
        registry_entry["strengths"].append("accurate_task_granularity")
    else:
        registry_entry["weaknesses"].append("coarse_or_fine_decomposition")
    
    assumption_count = decomp.get("assumptions_and_questions", {}).get("assumptions_count", 0)
    if assumption_count <= 2:
        registry_entry["strengths"].append("low_assumption_count")
    else:
        registry_entry["weaknesses"].append("many_unstated_assumptions")
    
    question_count = decomp.get("assumptions_and_questions", {}).get("questions_count", 0)
    if question_count >= 3:
        registry_entry["strengths"].append("identifies_ambiguities")
    else:
        registry_entry["weaknesses"].append("fails_to_ask_clarifying_questions")
    
    confidence = selfassess.get("overall_confidence", 0)
    if confidence >= 3.5:
        registry_entry["strengths"].append("realistic_self_assessment")
    else:
        registry_entry["weaknesses"].append("overly_pessimistic_or_unrealistic")
    
    return registry_entry


# ─────────────────────────────────────────────
# Comparison Analysis
# ─────────────────────────────────────────────

def compare_reports(report1: dict, report2: dict) -> dict:
    """Compare two audit reports side-by-side."""
    
    comparison = {
        "model_a": report1.get("model", "unknown"),
        "model_b": report2.get("model", "unknown"),
        "comparison": {},
    }
    
    # Task granularity comparison
    gran_a = report1.get("decomposition", {}).get("decomposition_analysis", {}).get("task_granularity", {})
    gran_b = report2.get("decomposition", {}).get("decomposition_analysis", {}).get("task_granularity", {})
    
    comparison["comparison"]["task_granularity"] = {
        "model_a": {
            "total_tasks": gran_a.get("total_tasks", 0),
            "target_pct": gran_a.get("1_to_4hr_pct", 0),
            "avg_hours": gran_a.get("hours_statistics", {}).get("mean", 0),
        },
        "model_b": {
            "total_tasks": gran_b.get("total_tasks", 0),
            "target_pct": gran_b.get("1_to_4hr_pct", 0),
            "avg_hours": gran_b.get("hours_statistics", {}).get("mean", 0),
        },
        "winner": "model_a" if gran_a.get("1_to_4hr_pct", 0) > gran_b.get("1_to_4hr_pct", 0) else "model_b",
    }
    
    # Self-awareness comparison
    sa_a = report1.get("self_assessment", {}).get("selfassess_analysis", {}).get("overall_confidence", 0)
    sa_b = report2.get("self_assessment", {}).get("selfassess_analysis", {}).get("overall_confidence", 0)
    
    comparison["comparison"]["self_awareness"] = {
        "model_a": sa_a,
        "model_b": sa_b,
        "winner": "model_a" if sa_a > sa_b else "model_b",
    }
    
    # Overall score comparison
    score_a = report1.get("overall_scores", {}).get("composite_score", 0)
    score_b = report2.get("overall_scores", {}).get("composite_score", 0)
    
    comparison["comparison"]["overall_score"] = {
        "model_a": score_a,
        "model_b": score_b,
        "winner": "model_a" if score_a > score_b else "model_b",
    }
    
    return comparison


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Analyze coding audit results")
    parser.add_argument("--decomposition", required=True, help="Decomposition JSON from Stage 2")
    parser.add_argument("--selfassess", required=True, help="Self-assessment JSON from Stage 3")
    parser.add_argument("--skeleton", default=None, help="Optional reference skeleton JSON")
    parser.add_argument("--output", default=None, help="Save comprehensive report to JSON")
    parser.add_argument("--registry-entry", default=None, help="Save Concierge registry entry to JSON")
    parser.add_argument("--compare-with", default=None, help="Compare with another model's audit report")
    args = parser.parse_args()
    
    # Load decomposition
    print("Loading audit results...", end="", flush=True)
    try:
        decomp_data = load_json_file(args.decomposition)
        selfassess_data = load_json_file(args.selfassess)
        print(" done")
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\nERROR: Invalid JSON: {e}")
        sys.exit(1)
    
    # Analyze
    print("Analyzing decomposition...", end="", flush=True)
    decomp_analysis = analyze_decomposition(decomp_data)
    print(" done")
    
    print("Analyzing self-assessment...", end="", flush=True)
    selfassess_analysis = analyze_selfassess(selfassess_data)
    print(" done")
    
    print("Building comprehensive report...", end="", flush=True)
    report = build_comprehensive_report(decomp_analysis, selfassess_analysis)
    print(" done")
    
    model = report.get("model", "unknown")
    composite = report.get("overall_scores", {}).get("composite_score", 0)
    
    print(f"\n{'='*60}")
    print(f"AUDIT REPORT: {model}")
    print(f"{'='*60}")
    print(f"Composite Score       : {composite}/5.0")
    print(f"Task Granularity      : {report.get('overall_scores', {}).get('task_granularity_score', 'N/A')}/5.0")
    print(f"Self-Awareness        : {report.get('overall_scores', {}).get('self_awareness_score', 'N/A')}/5.0")
    
    print(f"\nKey Findings:")
    for finding in report.get("key_findings", []):
        print(f"  {finding}")
    
    # Save comprehensive report
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps(report, indent=2))
        print(f"\n✓ Comprehensive report saved to {args.output}")
    
    # Save registry entry
    if args.registry_entry:
        registry = build_registry_entry(report)
        registry_path = Path(args.registry_entry)
        registry_path.write_text(json.dumps(registry, indent=2))
        print(f"✓ Registry entry saved to {args.registry_entry}")
        
        print(f"\nRegistry Entry Summary:")
        print(f"  Model: {registry.get('model')}")
        print(f"  Score: {registry.get('audit_score')}/5")
        print(f"  Best for: {', '.join(registry.get('best_for', []))}")
        print(f"  Avoid for: {', '.join(registry.get('avoid_for', []))}")
    
    # Comparison
    if args.compare_with:
        print(f"\nLoading comparison report from {args.compare_with}...", end="", flush=True)
        try:
            other_report = load_json_file(args.compare_with)
            print(" done")
            
            print("Computing comparison...", end="", flush=True)
            comparison = compare_reports(report, other_report)
            print(" done")
            
            model_a = comparison.get("model_a", "Model A")
            model_b = comparison.get("model_b", "Model B")
            
            print(f"\n{'='*60}")
            print(f"COMPARISON: {model_a} vs {model_b}")
            print(f"{'='*60}")
            
            gran_cmp = comparison.get("comparison", {}).get("task_granularity", {})
            print(f"Task Granularity:")
            print(f"  {model_a}: {gran_cmp.get('model_a', {}).get('target_pct', 0)}% in target range")
            print(f"  {model_b}: {gran_cmp.get('model_b', {}).get('target_pct', 0)}% in target range")
            print(f"  Winner: {gran_cmp.get('winner', '?')}")
            
            sa_cmp = comparison.get("comparison", {}).get("self_awareness", {})
            print(f"\nSelf-Awareness:")
            print(f"  {model_a}: {sa_cmp.get('model_a', 0)}/5")
            print(f"  {model_b}: {sa_cmp.get('model_b', 0)}/5")
            print(f"  Winner: {sa_cmp.get('winner', '?')}")
            
            score_cmp = comparison.get("comparison", {}).get("overall_score", {})
            print(f"\nOverall Score:")
            print(f"  {model_a}: {score_cmp.get('model_a', 0)}/5")
            print(f"  {model_b}: {score_cmp.get('model_b', 0)}/5")
            print(f"  Winner: {score_cmp.get('winner', '?')}")
            
            # Save comparison
            comparison_path = Path(args.output.replace(".json", "_comparison.json"))
            comparison_path.write_text(json.dumps(comparison, indent=2))
            print(f"\n✓ Comparison saved to {comparison_path}")
        except FileNotFoundError as e:
            print(f"\nERROR: Comparison report not found: {e}")
        except json.JSONDecodeError as e:
            print(f"\nERROR: Invalid comparison report: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
