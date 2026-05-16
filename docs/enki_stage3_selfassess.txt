#!/usr/bin/env python3
"""
Enki — Model Evaluation Suite
Stage 3: Model Self-Assessment

Evaluates a model's self-awareness of its own coding capabilities.

Enki is the Sumerian god of wisdom and knowledge.
This stage evaluates whether models can accurately assess their own wisdom/capability.

Part of the three-stage evaluation pipeline:
  Stage 1: Frontier models synthesize project skeleton (manual)
  Stage 2: Local model decomposes skeleton into atomic tasks (eval_coding_decompose.py)
  Stage 3: Local model self-assesses its own capability (this script)
  Stage 4: Analysis and registry integration (analyze_coding_audit.py)

Usage:
  python eval_coding_selfassess.py \
    --model gemma4:26b \
    --decomposition decomposition_gemma4.json \
    --host http://localhost:11434 \
    --output selfassess_gemma4.json

Requirements:
  pip install requests

The decomposition input should be valid JSON output from eval_coding_decompose.py
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import requests


# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

DEFAULT_TEMPERATURE = 0.5  # Same as decomposition
TIMEOUT_SECONDS = 300


# ─────────────────────────────────────────────
# Ollama Client
# ─────────────────────────────────────────────

def chat(
    host: str,
    model: str,
    messages: List[Dict],
    temperature: float = DEFAULT_TEMPERATURE,
    timeout: int = TIMEOUT_SECONDS,
) -> dict:
    """Call Ollama chat API."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    resp = requests.post(f"{host}/api/chat", json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def load_json_file(path: str) -> dict:
    """Load JSON file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(p.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────
# Self-Assessment Prompt Template
# ─────────────────────────────────────────────

def build_selfassess_prompt(decomposition: dict) -> str:
    """Build self-assessment prompt from decomposition."""
    decomposition_json = json.dumps(decomposition, indent=2)
    
    return f"""You are a code-generating AI model evaluating your own capabilities.

You have just completed a task decomposition for a software project. Now you must assess:
**If you were asked to execute each atomic task, what would you produce?**

For each major task category in the decomposition, answer these questions:

1. **Can you produce working, production-ready code?** (Yes/No/Partial)
2. **What assumptions must hold for your code to work?** (e.g., "Flask installed", "database exists")
3. **What would you need to assume about inputs/outputs?**
4. **What tests would you skip or struggle with?**
5. **What external constraints (APIs, libraries, runtime) would block you?**
6. **Overall confidence: 1-5** (1 = wouldn't work, 5 = confident it works immediately)

## Task Categories to Assess

- **REST API endpoints**: Can you write Flask/FastAPI routes with correct HTTP verbs?
- **Database schema**: Can you write SQL DDL with proper indexes, constraints, foreign keys?
- **Business logic**: Can you implement stateful calculations, state machines, financial logic?
- **Web UI**: Can you write HTML/CSS/JavaScript for interactive pages?
- **Testing**: Can you write unit tests, integration tests, mocks?
- **DevOps/Deployment**: Can you write Docker files, CI/CD configs, deployment scripts?

## Decomposition You Produced

```json
{decomposition_json}
```

---

## Your Assessment Output

Generate a valid JSON object with this structure:

{{
  "self_assessment_by_category": {{
    "rest_api_endpoints": {{
      "can_produce_working_code": "yes" | "partial" | "no",
      "confidence": 4,
      "assumptions": [
        "Framework: Flask or FastAPI",
        "HTTP knowledge assumed in caller"
      ],
      "input_assumptions": ["Request body is valid JSON"],
      "output_assumptions": ["Caller expects JSON response"],
      "tests_would_skip": ["Security testing (rate limiting, CORS)"],
      "blocking_constraints": [],
      "reasoning": "I can write basic CRUD endpoints, but..."
    }},
    "database_schema": {{
      "can_produce_working_code": "partial",
      "confidence": 3,
      "assumptions": ["PostgreSQL dialect", "Migrations handled externally"],
      "input_assumptions": [],
      "output_assumptions": ["Schema is normalized to 3NF"],
      "tests_would_skip": ["Concurrent transaction testing"],
      "blocking_constraints": ["Complex denormalization strategies"],
      "reasoning": "..."
    }},
    "business_logic": {{
      "can_produce_working_code": "yes" | "partial" | "no",
      "confidence": 3,
      "assumptions": [],
      "input_assumptions": [],
      "output_assumptions": [],
      "tests_would_skip": [],
      "blocking_constraints": [],
      "reasoning": ""
    }},
    "web_ui": {{
      "can_produce_working_code": "partial" | "no",
      "confidence": 2,
      "assumptions": [],
      "input_assumptions": [],
      "output_assumptions": [],
      "tests_would_skip": [],
      "blocking_constraints": ["Complex CSS layouts", "Browser compatibility"],
      "reasoning": ""
    }},
    "testing": {{
      "can_produce_working_code": "yes" | "partial",
      "confidence": 3,
      "assumptions": [],
      "input_assumptions": [],
      "output_assumptions": [],
      "tests_would_skip": ["Load testing", "Chaos engineering"],
      "blocking_constraints": [],
      "reasoning": ""
    }},
    "devops_deployment": {{
      "can_produce_working_code": "partial" | "no",
      "confidence": 2,
      "assumptions": [],
      "input_assumptions": [],
      "output_assumptions": [],
      "tests_would_skip": [],
      "blocking_constraints": ["Kubernetes orchestration", "Multi-cloud deployment"],
      "reasoning": ""
    }}
  }},
  "overall_project_confidence": 3,
  "biggest_risk_areas": [
    "Category name and why",
    "Example: 'Database schema — concurrent transactions and optimistic locking'",
    "Example: 'DevOps — Kubernetes is beyond my training'"
  ],
  "capability_boundaries": {{
    "can_do": [
      "Write CRUD REST APIs",
      "Basic SQL schemas",
      "Unit tests with mocks"
    ],
    "partial": [
      "Complex business logic",
      "Performance optimization",
      "Web UI styling"
    ],
    "cannot_do": [
      "Advanced DevOps (Kubernetes, multi-cloud)",
      "Complex system architecture decisions",
      "Security hardening"
    ]
  }},
  "recommendations_for_safer_usage": [
    "Pair with human code review for any API endpoints",
    "Use for scaffolding only, refine by human before production",
    "Test generated code with comprehensive test suite"
  ]
}}

---

## Scoring Guidance

Think carefully about:
- **Calibration**: Is your confidence realistic? Do your estimates match actual code quality?
- **Honesty**: Are you identifying your real limitations, or being overly optimistic?
- **Specificity**: Can you point to *why* you'd struggle with category X?
- **Boundary clarity**: Can you articulate where you'd need human help?

Generate ONLY valid JSON. No preamble. No markdown fences. Output the JSON object directly.
"""


# ─────────────────────────────────────────────
# Self-Assessment Execution
# ─────────────────────────────────────────────

def run_selfassess(
    host: str,
    model: str,
    decomposition: dict,
) -> Dict[str, Any]:
    """Run self-assessment evaluation."""
    
    prompt = build_selfassess_prompt(decomposition)
    
    messages = [{"role": "user", "content": prompt}]
    
    print(f"  Sending self-assessment prompt ({len(prompt)} chars)...", end="", flush=True)
    start = time.time()
    
    try:
        resp = chat(host, model, messages, temperature=DEFAULT_TEMPERATURE)
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API call failed: {str(e)}",
            "error_type": "api_error",
        }
    
    elapsed = time.time() - start
    print(f" done ({elapsed:.1f}s)")
    
    raw_content = resp.get("message", {}).get("content", "")
    
    # Try to parse JSON from response
    assessment_data = None
    parse_error = None
    
    try:
        assessment_data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        # Try to extract from markdown
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_content, re.DOTALL)
        if json_match:
            try:
                assessment_data = json.loads(json_match.group(1))
            except json.JSONDecodeError as e2:
                parse_error = f"Markdown JSON parse failed: {str(e2)}"
        else:
            # Extract by braces
            start_idx = raw_content.find('{')
            if start_idx >= 0:
                end_idx = raw_content.rfind('}')
                if end_idx > start_idx:
                    try:
                        assessment_data = json.loads(raw_content[start_idx:end_idx+1])
                    except json.JSONDecodeError as e3:
                        parse_error = f"Brace extraction parse failed: {str(e3)}"
            if not assessment_data:
                parse_error = f"No JSON found: {str(e)}"
    
    return {
        "success": assessment_data is not None,
        "assessment": assessment_data,
        "raw_response": raw_content,
        "parse_error": parse_error,
        "elapsed_seconds": elapsed,
    }


# ─────────────────────────────────────────────
# Metrics Extraction
# ─────────────────────────────────────────────

def extract_metrics(assessment: dict) -> dict:
    """Extract metrics from self-assessment."""
    metrics = {
        "overall_confidence": assessment.get("overall_project_confidence", 0),
        "confidence_by_category": {},
        "capability_summary": {
            "can_do_count": len(assessment.get("capability_boundaries", {}).get("can_do", [])),
            "partial_count": len(assessment.get("capability_boundaries", {}).get("partial", [])),
            "cannot_do_count": len(assessment.get("capability_boundaries", {}).get("cannot_do", [])),
        },
        "risk_areas_count": len(assessment.get("biggest_risk_areas", [])),
    }
    
    # Extract per-category confidence
    for category, data in assessment.get("self_assessment_by_category", {}).items():
        metrics["confidence_by_category"][category] = {
            "confidence": data.get("confidence", 0),
            "can_produce": data.get("can_produce_working_code", "unknown"),
            "blocking_constraints": len(data.get("blocking_constraints", [])),
        }
    
    return metrics


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Coding self-assessment evaluation — Stage 3 of three-stage audit"
    )
    parser.add_argument("--model", required=True, help="Ollama model name (e.g., gemma4:26b)")
    parser.add_argument("--decomposition", required=True, help="Path to decomposition JSON from Stage 2")
    parser.add_argument("--host", default="http://localhost:11434", help="Ollama host URL")
    parser.add_argument("--output", default=None, help="Save results to JSON file")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help="Model temperature")
    args = parser.parse_args()
    
    # Load decomposition
    print(f"Loading decomposition from {args.decomposition}...", end="", flush=True)
    try:
        decomposition_result = load_json_file(args.decomposition)
        # Extract the actual decomposition from the result wrapper
        if "decomposition_result" in decomposition_result:
            decomposition = decomposition_result["decomposition_result"].get("decomposition")
        else:
            decomposition = decomposition_result
        
        if not decomposition:
            print("\nERROR: No decomposition data found in file")
            sys.exit(1)
        print(" done")
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\nERROR: Invalid JSON: {e}")
        sys.exit(1)
    
    print(f"\nCoding Self-Assessment Audit")
    print(f"Model         : {args.model}")
    print(f"Decomposition : {decomposition.get('project_title', 'Untitled')}")
    print(f"Host          : {args.host}")
    print(f"{'='*60}\n")
    
    # Run self-assessment
    print("Running self-assessment...", flush=True)
    result = run_selfassess(args.host, args.model, decomposition)
    
    # Aggregate results
    all_results = {
        "model": args.model,
        "host": args.host,
        "project_title": decomposition.get("project_title", "Untitled"),
        "selfassess_result": result,
    }
    
    if result["success"]:
        print("✓ Self-assessment succeeded")
        metrics = extract_metrics(result["assessment"])
        all_results["metrics"] = metrics
        
        print(f"\n{'='*60}")
        print(f"SELF-ASSESSMENT METRICS")
        print(f"{'='*60}")
        print(f"Overall project confidence : {metrics['overall_confidence']}/5")
        print(f"Risk areas identified      : {metrics['risk_areas_count']}")
        print(f"Can reliably do            : {metrics['capability_summary']['can_do_count']}")
        print(f"Can do partially           : {metrics['capability_summary']['partial_count']}")
        print(f"Cannot do                  : {metrics['capability_summary']['cannot_do_count']}")
        
        print(f"\nPer-Category Confidence:")
        for category, cat_metrics in metrics["confidence_by_category"].items():
            conf = cat_metrics["confidence"]
            status = cat_metrics["can_produce"]
            blocks = cat_metrics["blocking_constraints"]
            print(f"  {category:20s} : {conf}/5 ({status:7s}) [{blocks} blocking constraints]")
    else:
        print(f"✗ Self-assessment failed: {result.get('error', 'Unknown error')}")
        print(f"  Parse error: {result.get('parse_error', 'N/A')}")
    
    # Save results
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps(all_results, indent=2))
        print(f"\n✓ Results saved to {args.output}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
