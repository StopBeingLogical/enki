#!/usr/bin/env python3
"""
Enki — Model Evaluation Suite
Stage 2: Project Decomposition

Evaluates how well a local model can break down a project skeleton into atomic tasks.

Enki is the Sumerian god of wisdom, knowledge, and deep understanding.
This suite evaluates the wisdom and capability of local language models.

Part of the three-stage evaluation pipeline:
  Stage 1: Frontier models synthesize project skeleton (manual)
  Stage 2: Local model decomposes skeleton into atomic tasks (this script)
  Stage 3: Local model self-assesses its own capability (eval_coding_selfassess.py)
  Stage 4: Analysis and registry integration (analyze_coding_audit.py)

Usage:
  python eval_coding_decompose.py \
    --model gemma4:26b \
    --skeleton project_skeleton.json \
    --host http://localhost:11434 \
    --output decomposition_gemma4.json

Requirements:
  pip install requests

The skeleton input should be valid JSON with:
  - title
  - architecture
  - modules (list of module names)
  - tech_stack (object)
  - assumptions (list)
  - critical_decisions (list)
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

DEFAULT_TEMPERATURE = 0.5  # Lower than conversational; want more reproducible decomposition
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
# Decomposition Prompt Template
# ─────────────────────────────────────────────

def build_decomposition_prompt(skeleton: dict) -> str:
    """Build the decomposition prompt from a project skeleton."""
    skeleton_json = json.dumps(skeleton, indent=2)
    return f"""You are an expert software architect decomposing a project specification into atomic tasks.

# Your Task

Given the project skeleton below, you must:

1. **For each module**, list all sub-modules or major components
2. **For each sub-module**, create atomic tasks — each completable in 1-4 hours by a skilled engineer
3. **For each task**, identify dependencies (which prior tasks must complete first)
4. **Surface assumptions** — what is the model assuming without asking?
5. **Estimate effort** — how many hours for each task?

## Output Format

Generate a valid JSON object with this structure:

{{
  "project_title": "...",
  "module_decomposition": {{
    "module_name": {{
      "description": "...",
      "sub_modules": ["...", "..."],
      "atomic_tasks": [
        {{
          "id": "MOD_001",
          "name": "Task name",
          "description": "What this task accomplishes",
          "estimated_hours": 2,
          "dependencies": ["MOD_prev"],
          "task_type": "backend_api | database | frontend | testing | devops | business_logic",
          "inputs": ["What this task takes as input"],
          "outputs": ["What this task produces"]
        }}
      ]
    }}
  }},
  "cross_module_dependencies": {{
    "MOD_001": ["MOD_010", "MOD_020"]
  }},
  "milestones": [
    {{
      "name": "MVP data layer",
      "target_hours": 8,
      "blocking_tasks": ["MOD_001", "MOD_002"]
    }}
  ],
  "unstated_assumptions": [
    "List any assumptions you made without asking the user"
  ],
  "questions_you_should_have_asked": [
    "If you identified ambiguities, list clarifying questions here"
  ],
  "estimated_total_hours": 40,
  "confidence_in_decomposition": 4
}}

## Project Skeleton

```json
{skeleton_json}
```

---

## Scoring Guidance

As you decompose, think about:
- **Task granularity**: Are your atomic tasks between 1-4 hours? (target: 65% in range)
- **Dependency accuracy**: Did you miss any dependencies? Did you create false ones?
- **Assumption surfacing**: Did you identify where the spec is ambiguous?
- **Effort realism**: Are your hour estimates reasonable for the task complexity?

Generate ONLY valid JSON. No preamble. No markdown fences. Output the JSON object directly.
"""


# ─────────────────────────────────────────────
# Decomposition Execution
# ─────────────────────────────────────────────

def run_decomposition(
    host: str,
    model: str,
    skeleton: dict,
) -> Dict[str, Any]:
    """Run the decomposition audit on a skeleton."""
    
    prompt = build_decomposition_prompt(skeleton)
    
    messages = [{"role": "user", "content": prompt}]
    
    print(f"  Sending decomposition prompt ({len(prompt)} chars)...", end="", flush=True)
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
    decomposition_data = None
    parse_error = None
    
    # First, try direct JSON parse
    try:
        decomposition_data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        # Try to extract JSON from markdown fences or other delimiters
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_content, re.DOTALL)
        if json_match:
            try:
                decomposition_data = json.loads(json_match.group(1))
            except json.JSONDecodeError as e2:
                parse_error = f"Markdown-fenced JSON parse failed: {str(e2)}"
        else:
            # Try to find JSON object by looking for opening/closing braces
            start_idx = raw_content.find('{')
            if start_idx >= 0:
                end_idx = raw_content.rfind('}')
                if end_idx > start_idx:
                    try:
                        decomposition_data = json.loads(raw_content[start_idx:end_idx+1])
                    except json.JSONDecodeError as e3:
                        parse_error = f"Extracted JSON parse failed: {str(e3)}"
            if not decomposition_data:
                parse_error = f"No JSON found in response: {str(e)}"
    
    return {
        "success": decomposition_data is not None,
        "decomposition": decomposition_data,
        "raw_response": raw_content,
        "parse_error": parse_error,
        "elapsed_seconds": elapsed,
    }


# ─────────────────────────────────────────────
# Metrics Extraction
# ─────────────────────────────────────────────

def extract_metrics(decomposition: dict) -> dict:
    """Extract metrics from a successful decomposition."""
    metrics = {
        "total_tasks": 0,
        "task_granularity_distribution": {
            "under_1hr": 0,
            "1_to_4hr": 0,
            "4_to_8hr": 0,
            "over_8hr": 0,
        },
        "estimated_total_hours": decomposition.get("estimated_total_hours", 0),
        "modules_count": len(decomposition.get("module_decomposition", {})),
        "assumptions_count": len(decomposition.get("unstated_assumptions", [])),
        "questions_count": len(decomposition.get("questions_you_should_have_asked", [])),
        "confidence": decomposition.get("confidence_in_decomposition", 0),
    }
    
    # Count tasks and granularity
    for module_data in decomposition.get("module_decomposition", {}).values():
        for task in module_data.get("atomic_tasks", []):
            metrics["total_tasks"] += 1
            hours = task.get("estimated_hours", 0)
            if hours < 1:
                metrics["task_granularity_distribution"]["under_1hr"] += 1
            elif hours <= 4:
                metrics["task_granularity_distribution"]["1_to_4hr"] += 1
            elif hours <= 8:
                metrics["task_granularity_distribution"]["4_to_8hr"] += 1
            else:
                metrics["task_granularity_distribution"]["over_8hr"] += 1
    
    # Calculate distribution percentages
    if metrics["total_tasks"] > 0:
        for key in metrics["task_granularity_distribution"]:
            pct = (metrics["task_granularity_distribution"][key] / metrics["total_tasks"]) * 100
            metrics[f"{key}_pct"] = round(pct, 1)
    
    return metrics


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Coding decomposition evaluation — Stage 2 of three-stage audit"
    )
    parser.add_argument("--model", required=True, help="Ollama model name (e.g., gemma4:26b)")
    parser.add_argument("--skeleton", required=True, help="Path to project skeleton JSON")
    parser.add_argument("--host", default="http://localhost:11434", help="Ollama host URL")
    parser.add_argument("--output", default=None, help="Save results to JSON file")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help="Model temperature")
    args = parser.parse_args()
    
    # Load skeleton
    print(f"Loading skeleton from {args.skeleton}...", end="", flush=True)
    try:
        skeleton = load_json_file(args.skeleton)
        print(" done")
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\nERROR: Invalid JSON in skeleton: {e}")
        sys.exit(1)
    
    print(f"\nCoding Decomposition Audit")
    print(f"Model    : {args.model}")
    print(f"Skeleton : {skeleton.get('title', 'Untitled')}")
    print(f"Host     : {args.host}")
    print(f"{'='*60}\n")
    
    # Run decomposition
    print("Running decomposition...", flush=True)
    result = run_decomposition(args.host, args.model, skeleton)
    
    # Aggregate results
    all_results = {
        "model": args.model,
        "host": args.host,
        "skeleton_title": skeleton.get("title", "Untitled"),
        "decomposition_result": result,
    }
    
    if result["success"]:
        print("✓ Decomposition succeeded")
        metrics = extract_metrics(result["decomposition"])
        all_results["metrics"] = metrics
        
        print(f"\n{'='*60}")
        print(f"DECOMPOSITION METRICS")
        print(f"{'='*60}")
        print(f"Total tasks generated     : {metrics['total_tasks']}")
        print(f"Total estimated hours     : {metrics['estimated_total_hours']}")
        print(f"Modules decomposed        : {metrics['modules_count']}")
        print(f"Assumptions surfaced      : {metrics['assumptions_count']}")
        print(f"Clarifying questions      : {metrics['questions_count']}")
        print(f"Model's self-confidence   : {metrics['confidence']}/5")
        
        print(f"\nTask Granularity Distribution:")
        dist = metrics["task_granularity_distribution"]
        print(f"  < 1 hour      : {dist['under_1hr']:3d} tasks ({metrics.get('under_1hr_pct', 0):.1f}%)")
        print(f"  1-4 hours     : {dist['1_to_4hr']:3d} tasks ({metrics.get('1_to_4hr_pct', 0):.1f}%) [TARGET RANGE]")
        print(f"  4-8 hours     : {dist['4_to_8hr']:3d} tasks ({metrics.get('4_to_8hr_pct', 0):.1f}%)")
        print(f"  > 8 hours     : {dist['over_8hr']:3d} tasks ({metrics.get('over_8hr_pct', 0):.1f}%)")
        
        if metrics.get("1_to_4hr_pct", 0) >= 60:
            print(f"\n✓ Granularity is in target range (60%+ in 1-4 hour band)")
        else:
            print(f"\n⚠ Granularity may be too coarse or too fine")
    else:
        print(f"✗ Decomposition failed: {result.get('error', 'Unknown error')}")
        print(f"  Parse error: {result.get('parse_error', 'N/A')}")
    
    # Save results
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps(all_results, indent=2))
        print(f"\n✓ Results saved to {args.output}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
