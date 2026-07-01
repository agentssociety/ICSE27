"""
Code-Level Hallucination — MetaGPT Comparison
==============================================
Applies the same AST-based orphan-route + unused-import scanner used
for AgentsSociety to MetaGPT's generated Python files.

P5 MetaGPT is excluded (no Python code generated, only task-description
filenames). P1 uses a nested subfolder path.

Usage:
    python -m research_results.scripts.metagpt_hallucination
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from research_results.scripts.extract_hallucination import _scan_backend
from research_results.scripts.paths import EXPERIMENTS, RESULTS_ROOT

SUMMARY_DIR = RESULTS_ROOT / "summaries"

METAGPT_CODE: dict[int, Path] = {
    1: EXPERIMENTS / "project_1 (metagpt)" / "hospital_triage_queue" / "hospital_triage_queue",
    2: EXPERIMENTS / "project_2 (metagpt)" / "blood_bank_inventory_manager",
    3: EXPERIMENTS / "project_3 (metagpt)" / "airport_runway_scheduling",
    4: EXPERIMENTS / "project_4 (metagpt)" / "atm_withdrawal_safety_backend",
    # 5 excluded: no Python code
    6: EXPERIMENTS / "project_6 (metagpt)" / "community_social_network",
}

# AS summary for comparison (live from rq2_hallucination.json)
AS_SUMMARY_PATH = SUMMARY_DIR / "rq2_hallucination.json"


def run() -> None:
    print("=== MetaGPT Code-Level Hallucination Scan ===\n")

    results = {}
    total_orphans = 0
    total_unused  = 0
    total_files   = 0

    for pid, code_dir in sorted(METAGPT_CODE.items()):
        data = _scan_backend(code_dir)
        results[pid] = data
        total_orphans += data["orphan_routes"]
        total_unused  += data["unused_imports"]
        total_files   += data["files_scanned"]
        print(
            f"  P{pid} ({code_dir.name}): "
            f"files={data['files_scanned']}, "
            f"routes={data['total_routes']}, "
            f"orphan_routes={data['orphan_routes']}, "
            f"unused_imports={data['unused_imports']}"
        )

    n_projects = len(METAGPT_CODE)
    print(f"\n  Totals across {n_projects} projects (P5 excluded — no code):")
    print(f"    files scanned  : {total_files}")
    print(f"    orphan routes  : {total_orphans}")
    print(f"    unused imports : {total_unused}")
    print(f"    per-project mean orphan routes  : {total_orphans / n_projects:.1f}")
    print(f"    per-project mean unused imports : {total_unused  / n_projects:.1f}")

    # Compare with AS
    if AS_SUMMARY_PATH.exists():
        as_data = json.loads(AS_SUMMARY_PATH.read_text(encoding="utf-8"))
        as_orphans = [p["orphan_routes"]["mean"] for p in as_data["projects"]]
        as_unused  = [p["unused_imports"]["mean"] for p in as_data["projects"]]
        print(f"\n  AgentsSociety (all 6 projects, mean across seeds per project):")
        print(f"    mean orphan routes  : {sum(as_orphans)/len(as_orphans):.2f}")
        print(f"    mean unused imports : {sum(as_unused)/len(as_unused):.2f}")

    # Write summary JSON
    summary = {
        "metric": "metagpt_code_hallucination",
        "description": (
            "AST-based orphan-route and unused-import detection applied to "
            "MetaGPT generated Python code. Same protocol as AS extract_hallucination.py. "
            "P5 excluded (no Python files generated). Values are per-project totals "
            "(each MG project has exactly one run)."
        ),
        "projects": {
            f"P{pid}": {
                "code_dir": str(code_dir),
                "files_scanned":  results[pid]["files_scanned"],
                "total_routes":   results[pid]["total_routes"],
                "orphan_routes":  results[pid]["orphan_routes"],
                "unused_imports": results[pid]["unused_imports"],
            }
            for pid, code_dir in METAGPT_CODE.items()
        },
        "cross_project_mean": {
            "orphan_routes":  round(total_orphans / n_projects, 2),
            "unused_imports": round(total_unused  / n_projects, 2),
        },
    }
    out_path = SUMMARY_DIR / "metagpt_hallucination.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Written: {out_path}")


if __name__ == "__main__":
    run()
