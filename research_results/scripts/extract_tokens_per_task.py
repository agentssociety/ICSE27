"""
Token and Latency Extraction — Per Task, Per Phase
====================================================

For each run (project_N, essay_K):
  1. Parse run.log using the existing paper.log_analysis.token_parser
  2. Get total tokens (input + output) and wall-clock duration per phase
  3. Divide by task count for that run → per-task rates
  4. Export raw per-run data to data/tokens/

Then aggregate across the 3 essays per project:
  - mean ± std of per-task token rate per phase
  - mean ± std of per-task latency (seconds) per phase
  - max per-task value per phase (worst-case upper bound)

Output:
  data/tokens/P{N}E{K}_tokens.json   — raw per-run data
  summaries/rq2_tokens_per_task.json — aggregated mean ± std
  summaries/rq2_latency_per_task.json — aggregated mean ± std

Usage (from repo root):
  python -m research_results.scripts.extract_tokens_per_task
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from paper.log_analysis.phases import Phase, PHASE_INFO, PHASE_ORDER
from paper.log_analysis.token_parser import parse_tokens, aggregate_by_phase, aggregate_duration_by_phase
from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT, RESULTS_ROOT

DATA_DIR     = RESULTS_ROOT / "data" / "tokens"
SUMMARY_DIR  = RESULTS_ROOT / "summaries"


# ── per-run extraction ────────────────────────────────────────────────────────

def extract_run(run_id) -> dict:
    """
    Parse one run.log and return per-phase per-task token and duration data.
    """
    token_log   = parse_tokens(run_id.log_path)
    phase_toks  = aggregate_by_phase(token_log)
    phase_durs  = aggregate_duration_by_phase(token_log)
    wall_s      = token_log.project_wall_clock()
    n_tasks     = run_id.task_count()

    phases = []
    for ph in PHASE_ORDER:
        tok  = phase_toks.get(ph)
        dur  = phase_durs.get(ph)
        total_tok = tok.total     if tok  else 0
        total_in  = tok.total_in  if tok  else 0
        total_out = tok.total_out if tok  else 0
        dur_s     = dur.total     if dur  else 0.0
        step_cnt  = dur.count     if dur  else 0

        # per-task normalisation: divide by number of tasks in this run
        per_task_tok  = round(total_tok  / n_tasks, 2) if n_tasks else 0.0
        per_task_in   = round(total_in   / n_tasks, 2) if n_tasks else 0.0
        per_task_out  = round(total_out  / n_tasks, 2) if n_tasks else 0.0
        per_task_dur  = round(dur_s      / n_tasks, 2) if n_tasks else 0.0

        phases.append({
            "phase":          ph.value,
            "label":          PHASE_INFO[ph].label,
            "n_tasks":        n_tasks,
            "step_count":     step_cnt,
            # absolute totals for this run
            "total_in":       total_in,
            "total_out":      total_out,
            "total_tokens":   total_tok,
            "total_dur_s":    round(dur_s, 2),
            # per-task rates (main comparison unit)
            "per_task_in":    per_task_in,
            "per_task_out":   per_task_out,
            "per_task_tokens": per_task_tok,
            "per_task_dur_s": per_task_dur,
        })

    return {
        "run_id":           str(run_id),
        "project":          run_id.project,
        "essay":            run_id.essay,
        "n_tasks":          n_tasks,
        "wall_clock_s":     round(wall_s, 2),
        "wall_clock_per_task_s": round(wall_s / n_tasks, 2) if n_tasks else 0.0,
        "phases":           phases,
    }


# ── statistics helpers ────────────────────────────────────────────────────────

def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0

def _std(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = _mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))

def _max(vals: list[float]) -> float:
    return max(vals) if vals else 0.0


# ── per-project aggregation ───────────────────────────────────────────────────

def aggregate_project(project_id: int, runs: list[dict]) -> dict:
    """
    Compute mean ± std across essays for one project.
    Returns one row per phase with mean, std, max of per-task rates.
    """
    phases = []
    for ph in PHASE_ORDER:
        # collect per-task values across all 3 essays
        tok_vals  = [next((p["per_task_tokens"] for p in r["phases"] if p["phase"] == ph.value), 0.0) for r in runs]
        in_vals   = [next((p["per_task_in"]     for p in r["phases"] if p["phase"] == ph.value), 0.0) for r in runs]
        out_vals  = [next((p["per_task_out"]     for p in r["phases"] if p["phase"] == ph.value), 0.0) for r in runs]
        dur_vals  = [next((p["per_task_dur_s"]   for p in r["phases"] if p["phase"] == ph.value), 0.0) for r in runs]

        phases.append({
            "phase": ph.value,
            "label": PHASE_INFO[ph].label,
            "per_task_tokens": {
                "mean": round(_mean(tok_vals), 1),
                "std":  round(_std(tok_vals),  1),
                "max":  round(_max(tok_vals),  1),
                "values": [round(v, 1) for v in tok_vals],
            },
            "per_task_input": {
                "mean": round(_mean(in_vals), 1),
                "std":  round(_std(in_vals),  1),
                "max":  round(_max(in_vals),  1),
                "values": [round(v, 1) for v in in_vals],
            },
            "per_task_output": {
                "mean": round(_mean(out_vals), 1),
                "std":  round(_std(out_vals),  1),
                "max":  round(_max(out_vals),  1),
                "values": [round(v, 1) for v in out_vals],
            },
            "per_task_dur_s": {
                "mean": round(_mean(dur_vals), 2),
                "std":  round(_std(dur_vals),  2),
                "max":  round(_max(dur_vals),  2),
                "values": [round(v, 2) for v in dur_vals],
            },
        })

    wall_vals = [r["wall_clock_per_task_s"] for r in runs]
    return {
        "project_id":         project_id,
        "n_essays":           len(runs),
        "wall_clock_per_task_s": {
            "mean":   round(_mean(wall_vals), 2),
            "std":    round(_std(wall_vals),  2),
            "max":    round(_max(wall_vals),  2),
            "values": [round(v, 2) for v in wall_vals],
        },
        "phases": phases,
    }


# ── main ─────────────────────────────────────────────────────────────────────

def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Token & Latency Extraction (per task, per phase) ===\n")

    # Step 1: extract each run
    all_run_data: dict[str, dict] = {}
    for run_id in ALL_RUNS:
        print(f"  Parsing {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_tokens.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"done  (wall={data['wall_clock_s']}s, tasks={data['n_tasks']})")

    # Step 2: aggregate per project → mean ± std across 3 essays
    token_summary  = []
    latency_summary = []

    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs = [all_run_data[str(r)] for r in run_ids]
        proj_agg = aggregate_project(project_id, runs)

        token_entry = {
            "project_id": project_id,
            "n_essays":   proj_agg["n_essays"],
            "phases": [
                {
                    "phase": ph["phase"],
                    "label": ph["label"],
                    **{k: ph[k] for k in ("per_task_tokens", "per_task_input", "per_task_output")},
                }
                for ph in proj_agg["phases"]
            ],
        }
        latency_entry = {
            "project_id": project_id,
            "n_essays":   proj_agg["n_essays"],
            "wall_clock_per_task_s": proj_agg["wall_clock_per_task_s"],
            "phases": [
                {
                    "phase": ph["phase"],
                    "label": ph["label"],
                    "per_task_dur_s": ph["per_task_dur_s"],
                }
                for ph in proj_agg["phases"]
            ],
        }
        token_summary.append(token_entry)
        latency_summary.append(latency_entry)

    # Step 3: cross-project summary (mean across all projects)
    def _cross_project_phase(summaries: list[dict], field: str) -> list[dict]:
        cross = []
        for ph in PHASE_ORDER:
            all_means = []
            all_stds  = []
            for proj in summaries:
                ph_entry = next((p for p in proj["phases"] if p["phase"] == ph.value), None)
                if ph_entry and field in ph_entry:
                    all_means.append(ph_entry[field]["mean"])
                    all_stds.append(ph_entry[field]["std"])
            cross.append({
                "phase":  ph.value,
                "label":  PHASE_INFO[ph].label,
                "cross_project_mean": round(_mean(all_means), 1),
                "cross_project_std":  round(_mean(all_stds), 1),
            })
        return cross

    tok_out = {
        "metric":       "tokens_per_task",
        "description":  (
            "Per-task token consumption per SDLC phase. "
            "Computed as total phase tokens / task count per run, "
            "then mean ± std across 3 essay seeds per project."
        ),
        "unit":         "tokens",
        "projects":     token_summary,
        "cross_project_total_tokens": _cross_project_phase(token_summary, "per_task_tokens"),
    }
    lat_out = {
        "metric":       "latency_per_task",
        "description":  (
            "Per-task wall-clock latency per SDLC phase. "
            "Computed as total phase step-time / task count per run, "
            "then mean ± std across 3 essay seeds per project. "
            "Note: phase step-times may sum to >100% of wall-clock because "
            "nested agent steps overlap parent steps."
        ),
        "unit":         "seconds",
        "projects":     latency_summary,
        "cross_project_latency": _cross_project_phase(latency_summary, "per_task_dur_s"),
    }

    (SUMMARY_DIR / "rq2_tokens_per_task.json").write_text(
        json.dumps(tok_out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (SUMMARY_DIR / "rq2_latency_per_task.json").write_text(
        json.dumps(lat_out, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("\n  Summaries written:")
    print("    summaries/rq2_tokens_per_task.json")
    print("    summaries/rq2_latency_per_task.json")


if __name__ == "__main__":
    run()
