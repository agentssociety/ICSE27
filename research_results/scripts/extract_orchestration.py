"""
RQ1b Orchestration Metric Extraction — Coordination Quality
============================================================

For each run (project_N, essay_K), compute:
  - Pipeline steps (total execution blocks)
  - Phase back-tracks  (backward transitions in SDLC phase order)
  - Phase re-entries   (times the pipeline left a phase and returned to it)
  - Orchestration overhead (% of steps classified as ORCHESTRATION)
  - SM delegation events (Scrum Master → sub-agent calls)
  - Re-delegation events (same sub-agent called >1 time for same phase)
  - Escalation zone (% of steps that are in an escalated failure window)
  - SR, PL, DS as defined in the paper

SR (Self-fix Rate)  = N_fixed / N_incidents
PL (Path Linearity) = (N_steps - N_backtracks) / N_steps
DS (Delegation Stability) = (N_delegations - N_redelegations) / N_delegations

For each project: mean ± std across 3 essays.

Output:
  data/orchestration/P{N}E{K}_orch.json  — raw per-run metrics
  summaries/rq1b_coordination.json       — aggregated mean ± std per project

Usage (from repo root):
  python -m research_results.scripts.extract_orchestration
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from paper.log_analysis.phases import Phase, PHASE_INFO, PHASE_ORDER
from paper.log_analysis.token_parser import parse_tokens
from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT, RESULTS_ROOT
from research_results.scripts.extract_errors import _analyse_log

DATA_DIR    = RESULTS_ROOT / "data" / "orchestration"
SUMMARY_DIR = RESULTS_ROOT / "summaries"

CANONICAL_RANK = {p: i for i, p in enumerate(PHASE_ORDER)}

# Sub-agents callable by the Scrum Master (delegation events)
SUB_AGENTS = {
    "developer_agent", "frontend_agent", "devops_agent",
    "project_manager_agent", "package_design_agent",
    "user_story_backlog_agent", "formal_specification_agent",
    "uml_diagram_generation_agent", "semi_formal_requirement_agent",
}
SM_AGENTS = {"__root__", "scrum_master_agent"}


# ── per-run extraction ────────────────────────────────────────────────────────

def extract_run(run_id) -> dict:
    token_log = parse_tokens(run_id.log_path)
    blocks    = token_log.blocks
    wall_s    = token_log.project_wall_clock()
    n_steps   = len(blocks)

    # ── back-tracks ───────────────────────────────────────────────────────────
    backtracks = 0
    last_rank  = -1
    for eb in blocks:
        ph = eb.block.phase
        if ph == Phase.ORCHESTRATION:
            continue
        r = CANONICAL_RANK[ph]
        if last_rank >= 0 and r < last_rank:
            backtracks += 1
        last_rank = r

    # ── phase re-entries ──────────────────────────────────────────────────────
    # Count only true re-entries: leave a phase, then return to it later.
    # Consecutive blocks in the same phase are a single visit, not re-entries.
    seen_ph, last_ph, reentry = set(), None, 0
    for eb in blocks:
        ph = eb.block.phase
        if ph == Phase.ORCHESTRATION:
            continue
        if ph != last_ph:
            if ph in seen_ph:
                reentry += 1
            seen_ph.add(ph)
            last_ph = ph

    # ── orchestration overhead ────────────────────────────────────────────────
    orch_n   = sum(1 for eb in blocks if eb.block.phase == Phase.ORCHESTRATION)
    orch_pct = round(100 * orch_n / n_steps, 1) if n_steps else 0.0

    # ── delegation events ─────────────────────────────────────────────────────
    delegations: list[tuple[str, str]] = []   # (phase, sub_agent)
    for eb in blocks:
        if eb.agent_session in SM_AGENTS:
            for call in eb.block.calls:
                if call in SUB_AGENTS:
                    delegations.append((eb.block.phase.value, call))

    deleg_counter = Counter(delegations)
    n_delegations  = len(delegations)
    n_redelegations = sum(v - 1 for v in deleg_counter.values() if v > 1)

    # ── error metrics (via incident analysis) ────────────────────────────────
    pa          = _analyse_log(run_id.log_path, run_id.project)
    incidents   = pa.incidents
    total_err   = len(incidents)
    fixed_n     = sum(1 for i in incidents if i.outcome == "FAIL_FIXED")
    esc_n       = sum(1 for i in incidents if i.outcome == "FAIL_ESCALATED")

    # ── escalation zone: % steps in escalated failure window ─────────────────
    # A step is "in escalation zone" if it occurs between a FAIL_ESCALATED
    # incident and the next explicit SM escalation (re-delegation after failure).
    # Approximation: we count steps where the nearest prior incident was escalated.
    esc_lines = {i.line_num for i in incidents if i.outcome == "FAIL_ESCALATED"}
    block_lines = [eb.block.line_start for eb in blocks]
    esc_zone_steps = 0
    for bline in block_lines:
        prior_esc = [l for l in esc_lines if l < bline]
        if prior_esc:
            # check no fixed incident between latest esc and this block
            latest_esc = max(prior_esc)
            fixed_after = any(
                i.line_num > latest_esc and i.line_num < bline
                and i.outcome == "FAIL_FIXED"
                for i in incidents
            )
            if not fixed_after:
                esc_zone_steps += 1
    esc_pct = round(100 * esc_zone_steps / n_steps, 1) if n_steps else 0.0

    # ── paper metrics ─────────────────────────────────────────────────────────
    sr = round(100 * fixed_n / total_err, 1)      if total_err  else 100.0
    pl = round((n_steps - backtracks) / n_steps, 4) if n_steps  else 1.0
    ds = round((n_delegations - n_redelegations) / n_delegations, 4) if n_delegations else 1.0

    return {
        "run_id":              str(run_id),
        "project":             run_id.project,
        "essay":               run_id.essay,
        "n_tasks":             run_id.task_count(),
        "wall_clock_s":        round(wall_s, 2),
        "wall_clock_min":      round(wall_s / 60, 1),
        # Execution dynamics
        "pipeline_steps":      n_steps,
        "phase_backtracks":    backtracks,
        "phase_reentries":     reentry,
        "orch_overhead_pct":   orch_pct,
        # Delegation quality
        "sm_delegations":      n_delegations,
        "redelegations":       n_redelegations,
        "escalation_zone_pct": esc_pct,
        # Recovery behavior
        "total_incidents":     total_err,
        "escalated_incidents": esc_n,
        "self_fix_rate_sr":    sr,
        # Paper metrics
        "SR":  sr,
        "PL":  pl,
        "DS":  ds,
    }


# ── stats helpers ─────────────────────────────────────────────────────────────

def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0

def _std(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = _mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))

def _stat(vals: list[float], decimals: int = 1) -> dict:
    return {
        "mean":   round(_mean(vals), decimals),
        "std":    round(_std(vals),  decimals),
        "values": [round(v, decimals) for v in vals],
    }


# ── per-project aggregation ───────────────────────────────────────────────────

def aggregate_project(project_id: int, runs: list[dict]) -> dict:
    def _f(key: str, dec: int = 1) -> dict:
        return _stat([float(r[key]) for r in runs], decimals=dec)

    return {
        "project_id":            project_id,
        "n_essays":              len(runs),
        # Execution dynamics (Table RQ1b)
        "pipeline_steps":        _f("pipeline_steps", 0),
        "phase_backtracks":      _f("phase_backtracks", 0),
        "phase_reentries":       _f("phase_reentries", 0),
        "orch_overhead_pct":     _f("orch_overhead_pct", 1),
        # Delegation quality
        "sm_delegations":        _f("sm_delegations", 0),
        "redelegations":         _f("redelegations", 0),
        "escalation_zone_pct":   _f("escalation_zone_pct", 1),
        # Recovery behavior
        "total_incidents":       _f("total_incidents", 0),
        "escalated_incidents":   _f("escalated_incidents", 0),
        "self_fix_rate_sr":      _f("self_fix_rate_sr", 1),
        "wall_clock_min":        _f("wall_clock_min", 1),
        # Paper metrics
        "SR": _f("SR", 1),
        "PL": _f("PL", 3),
        "DS": _f("DS", 3),
    }


# ── formatted table helper (for README / console) ────────────────────────────

def format_table_row(proj_agg: dict) -> str:
    def _cell(d: dict) -> str:
        return f"{d['mean']} ± {d['std']}"

    p = proj_agg["project_id"]
    return (
        f"  Project {p}:  "
        f"steps={_cell(proj_agg['pipeline_steps'])}  "
        f"backtracks={_cell(proj_agg['phase_backtracks'])}  "
        f"SR={_cell(proj_agg['SR'])}%  "
        f"PL={_cell(proj_agg['PL'])}  "
        f"DS={_cell(proj_agg['DS'])}"
    )


# ── main ─────────────────────────────────────────────────────────────────────

def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Orchestration Metric Extraction (RQ1b Coordination) ===\n")

    all_run_data: dict[str, dict] = {}
    for run_id in ALL_RUNS:
        print(f"  Parsing {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_orch.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(
            f"done  (steps={data['pipeline_steps']}, "
            f"SR={data['SR']}%, PL={data['PL']:.3f}, DS={data['DS']:.3f})"
        )

    projects_summary = []
    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs = [all_run_data[str(r)] for r in run_ids]
        agg  = aggregate_project(project_id, runs)
        projects_summary.append(agg)
        print(format_table_row(agg))

    output = {
        "metric":      "rq1b_coordination",
        "description": (
            "Orchestration quality metrics across all runs (6 projects: 4×3 seeds + 2×1 seed). "
            "SR = N_fixed / N_incidents (Self-fix Rate, reported as %). "
            "PL = (N_steps - N_backtracks) / N_steps (Path Linearity, 0–1). "
            "DS = (N_delegations - N_redelegations) / N_delegations (Delegation Stability, 0–1). "
            "Values reported as mean ± std across 3 essay seeds per project."
        ),
        "projects": projects_summary,
    }

    (SUMMARY_DIR / "rq1b_coordination.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Summary written: summaries/rq1b_coordination.json")


if __name__ == "__main__":
    run()
