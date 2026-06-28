"""
RQ1a Error Incident Extraction — Autonomy Metrics
===================================================

For each run (project_N, essay_K):
  1. Parse run.log to detect all error incidents
  2. Classify each as FAIL_FIXED (autonomous recovery) or FAIL_ESCALATED (blocked)
  3. Compute Self-fix Rate (SR) = fixed / total

For each project, compute mean ± std across 3 essays for:
  - total incidents
  - escalated (unresolved)
  - self-fix rate SR
  - pipeline steps (total execution blocks)
  - wall-clock time

Output:
  data/errors/P{N}E{K}_errors.json    — raw per-run incident lists
  summaries/rq1a_autonomy.json        — aggregated mean ± std per project

Usage (from repo root):
  python -m research_results.scripts.extract_errors
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from paper.log_analysis.phases import Phase, PHASE_INFO, PHASE_ORDER
from paper.log_analysis.token_parser import parse_tokens
from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT, RESULTS_ROOT

# Reuse lower-level functions from the paper module (bypass the hardcoded path in analyse_project)
from paper.log_analysis.error_analysis import (
    _parse_lines, _detect_incidents, _count_pass_blocks,
    ProjectAnalysis, ErrorIncident, FAIL_FIXED, FAIL_ESCALATED, PASS
)

DATA_DIR    = RESULTS_ROOT / "data" / "errors"
SUMMARY_DIR = RESULTS_ROOT / "summaries"

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mABCDEFGHJKLMSTfhinrsu]")


# ── per-run extraction ────────────────────────────────────────────────────────

def _analyse_log(log_path: Path, project_id: int) -> ProjectAnalysis:
    """Parse a run.log at an arbitrary path (bypasses hardcoded path in analyse_project)."""
    raw_lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    lines     = _parse_lines(log_path)
    incidents = _detect_incidents(lines, raw_lines, project_id)
    pa        = ProjectAnalysis(project_id=project_id, incidents=incidents)
    pass_counts = _count_pass_blocks(log_path, incidents)
    for phase, cnt in pass_counts.items():
        for _ in range(cnt):
            pa.block_outcomes.append((0, phase, PASS))
    return pa


def extract_run(run_id) -> dict:
    """
    Extract all error incidents from one run.log.
    """
    pa        = _analyse_log(run_id.log_path, run_id.project)
    incidents = pa.incidents

    total    = len(incidents)
    fixed    = sum(1 for i in incidents if i.outcome == FAIL_FIXED)
    escalated = sum(1 for i in incidents if i.outcome == FAIL_ESCALATED)
    sr       = round(fixed / total * 100, 1) if total else 100.0

    # Parse total step count from token log
    token_log  = parse_tokens(run_id.log_path)
    n_steps    = len(token_log.blocks)
    wall_s     = token_log.project_wall_clock()

    # Phase distribution of incidents
    by_phase = defaultdict(lambda: {"fixed": 0, "escalated": 0})
    for inc in incidents:
        key = inc.phase.value
        if inc.outcome == FAIL_FIXED:
            by_phase[key]["fixed"] += 1
        else:
            by_phase[key]["escalated"] += 1

    return {
        "run_id":         str(run_id),
        "project":        run_id.project,
        "essay":          run_id.essay,
        "n_tasks":        run_id.task_count(),
        "wall_clock_s":   round(wall_s, 2),
        "pipeline_steps": n_steps,
        "total_incidents": total,
        "fixed_incidents": fixed,
        "escalated_incidents": escalated,
        "self_fix_rate_pct": sr,
        "by_phase": {
            ph.value: by_phase[ph.value]
            for ph in PHASE_ORDER
            if ph.value in by_phase
        },
        "incidents": [
            {
                "line_num":   inc.line_num,
                "timestamp":  inc.timestamp,
                "phase":      inc.phase.value,
                "error_type": inc.error_type,
                "outcome":    inc.outcome,
                "message":    inc.message[:200],
            }
            for inc in incidents
        ],
    }


# ── stats helpers ─────────────────────────────────────────────────────────────

def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0

def _std(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = _mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def _stat(vals: list[float]) -> dict:
    return {
        "mean":   round(_mean(vals), 2),
        "std":    round(_std(vals), 2),
        "values": [round(v, 2) for v in vals],
    }


# ── per-project aggregation ───────────────────────────────────────────────────

def aggregate_project(project_id: int, runs: list[dict]) -> dict:
    steps    = [r["pipeline_steps"]      for r in runs]
    total    = [r["total_incidents"]     for r in runs]
    fixed    = [r["fixed_incidents"]     for r in runs]
    esc      = [r["escalated_incidents"] for r in runs]
    sr       = [r["self_fix_rate_pct"]   for r in runs]
    wall     = [r["wall_clock_s"]        for r in runs]

    # phase incident breakdown — mean ± std
    phase_stats = {}
    for ph in PHASE_ORDER:
        ph_fixed = [r["by_phase"].get(ph.value, {}).get("fixed", 0)     for r in runs]
        ph_esc   = [r["by_phase"].get(ph.value, {}).get("escalated", 0) for r in runs]
        if any(v > 0 for v in ph_fixed + ph_esc):
            phase_stats[ph.value] = {
                "label":     PHASE_INFO[ph].label,
                "fixed":     _stat([float(v) for v in ph_fixed]),
                "escalated": _stat([float(v) for v in ph_esc]),
            }

    return {
        "project_id":           project_id,
        "n_essays":             len(runs),
        "pipeline_steps":       _stat([float(v) for v in steps]),
        "total_incidents":      _stat([float(v) for v in total]),
        "fixed_incidents":      _stat([float(v) for v in fixed]),
        "escalated_incidents":  _stat([float(v) for v in esc]),
        "self_fix_rate_pct":    _stat(sr),
        "wall_clock_s":         _stat([float(v) for v in wall]),
        "by_phase":             phase_stats,
    }


# ── main ─────────────────────────────────────────────────────────────────────

def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Error Incident Extraction (RQ1a Autonomy) ===\n")

    all_run_data: dict[str, dict] = {}
    for run_id in ALL_RUNS:
        print(f"  Parsing {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_errors.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        sr_str = f"{data['self_fix_rate_pct']}%"
        print(f"done  (incidents={data['total_incidents']}, SR={sr_str})")

    # aggregate
    projects_summary = []
    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs = [all_run_data[str(r)] for r in run_ids]
        agg  = aggregate_project(project_id, runs)
        projects_summary.append(agg)

    # cross-project aggregate
    all_total   = [r["total_incidents"]     for p in all_run_data.values() for r in [p]]
    all_esc     = [r["escalated_incidents"] for p in all_run_data.values() for r in [p]]
    all_sr      = [r["self_fix_rate_pct"]   for p in all_run_data.values() for r in [p]]
    all_steps   = [r["pipeline_steps"]      for p in all_run_data.values() for r in [p]]

    total_incidents_all = sum(all_total)
    total_fixed_all     = sum(r["fixed_incidents"] for r in all_run_data.values())
    total_esc_all       = sum(all_esc)

    output = {
        "metric":      "rq1a_autonomy",
        "description": (
            "Error incident analysis across all 12 runs (4 projects × 3 seeds). "
            "SR = fixed / total incidents. "
            "Values reported as mean ± std across 3 essay seeds per project."
        ),
        "projects": projects_summary,
        "cross_run_aggregate": {
            "total_runs":      len(ALL_RUNS),
            "total_incidents": total_incidents_all,
            "total_fixed":     total_fixed_all,
            "total_escalated": total_esc_all,
            "overall_sr_pct":  round(total_fixed_all / total_incidents_all * 100, 1)
                               if total_incidents_all else 100.0,
        },
    }

    (SUMMARY_DIR / "rq1a_autonomy.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Summary written: summaries/rq1a_autonomy.json")


if __name__ == "__main__":
    run()
