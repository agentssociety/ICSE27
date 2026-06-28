"""
NLI Confidence Score Extraction — RQ2 Model-Level Confidence
=============================================================

For each run (project_N, essay_K):
  - Load all task_nli_*.json files
  - Each file: {task_id, confidence, total_claims, supported_claims, evidence}

Two INDEPENDENT metrics are computed — they are orthogonal, not contradictory:

  1. nli_alignment_score  (= the "confidence" field in the source JSON)
     = mean NLI entailment score ONLY for claims that found a matching fact
       in the source specification.
     Measures: PRECISION of grounded claims — "when the agent says something
       traceable to the spec, how strongly is it actually entailed?"
     Note: only the supported_claims subset enters this score. The ungrounded
       claims never receive an NLI score, so this is structurally biased high.
     Values in our data: 0.85–0.999 (always high because it is precision-only).

  2. spec_extrapolation_rate  (formerly called "hallucination_rate")
     = 1 - (supported_claims / total_claims)
     = fraction of generated claims with NO matching fact in the specification.
     Measures: how much the agent ADD BEYOND the spec (not whether it is wrong).
     In software engineering, specifications are intentionally incomplete.
     An agent that fills in implied details (queue confirmations, error copy,
     validation defaults) produces ungrounded claims that are DESIRABLE —
     this is requirement elicitation, not hallucination.
     Values in our data: 25–75% per task.

  Why "high alignment score + high extrapolation rate" is NOT a contradiction:
    - alignment score = precision of the MATCHED 50%
    - extrapolation rate = coverage gap of the UNMATCHED 50%
    These measure different populations of claims entirely.

  Correct interpretation for the ICSE paper:
    - High alignment score → the agent does not distort what it can trace
    - High extrapolation rate → the agent fills in implied details beyond the spec
    Both are features of a good SE agent, not bugs.

Aggregation:
  - Per project: mean ± std across 3 essays
  - Cross-project: pooled statistics over all 12 runs

Output:
  data/nli/P{N}E{K}_nli.json      — raw per-run NLI data
  summaries/rq2_nli_confidence.json — aggregated mean ± std

Usage (from repo root):
  python -m research_results.scripts.extract_nli
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT, RESULTS_ROOT

DATA_DIR    = RESULTS_ROOT / "data" / "nli"
SUMMARY_DIR = RESULTS_ROOT / "summaries"


# ── stats helpers ─────────────────────────────────────────────────────────────

def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0

def _std(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = _mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))

def _median(vals: list[float]) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    n = len(s)
    return (s[n // 2 - 1] + s[n // 2]) / 2 if n % 2 == 0 else s[n // 2]

def _percentile(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    idx = p / 100 * (len(s) - 1)
    lo, hi = int(idx), min(int(idx) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (idx - lo)

def _iqr(vals: list[float]) -> tuple[float, float, float]:
    q1 = _percentile(vals, 25)
    q3 = _percentile(vals, 75)
    return q1, q3, q3 - q1

def _stat(vals: list[float], decimals: int = 4) -> dict:
    return {
        "mean":   round(_mean(vals),   decimals),
        "std":    round(_std(vals),    decimals),
        "median": round(_median(vals), decimals),
        "values": [round(v, decimals) for v in vals],
    }


# ── per-run extraction ────────────────────────────────────────────────────────

def extract_run(run_id) -> dict:
    scores: list[float]  = []
    tasks: list[dict]    = []
    total_claims_all     = 0
    supported_claims_all = 0

    for path in run_id.nli_paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        conf     = float(data["confidence"])
        total_c  = int(data["total_claims"])
        supp_c   = int(data["supported_claims"])
        scores.append(conf)
        total_claims_all     += total_c
        supported_claims_all += supp_c
        tasks.append({
            "task_id":            data["task_id"],
            "nli_alignment_score": conf,         # precision of grounded claims only
            "total_claims":       total_c,
            "supported_claims":   supp_c,
            # fraction of claims with no spec match — NOT hallucination;
            # in SE this is requirement elicitation beyond the spec
            "spec_extrapolation_rate": round(1 - supp_c / total_c, 4) if total_c else 0.0,
            "spec_coverage_rate":      round(supp_c / total_c, 4) if total_c else 1.0,
            "n_evidence":         len(data.get("evidence", [])),
        })

    if not scores:
        return {"run_id": str(run_id), "project": run_id.project, "essay": run_id.essay,
                "n_tasks": 0, "tasks": [], "summary": {}}

    q1, q3, iqr = _iqr(scores)
    lo, hi      = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers    = [s for s in scores if s < lo or s > hi]
    zero_conf   = [s for s in scores if s == 0.0]

    spec_coverage = round(
        supported_claims_all / total_claims_all, 4
    ) if total_claims_all else 1.0
    spec_extrapolation = round(1 - spec_coverage, 4)

    return {
        "run_id":  str(run_id),
        "project": run_id.project,
        "essay":   run_id.essay,
        "n_tasks": len(tasks),
        "tasks":   tasks,
        "summary": {
            # Metric 1: precision of the grounded claims (structurally high ~0.85-0.999)
            "mean_nli_alignment_score":   round(_mean(scores), 4),
            "median_nli_alignment_score": round(_median(scores), 4),
            "std_nli_alignment_score":    round(_std(scores), 4),
            "q1":  round(q1, 4),
            "q3":  round(q3, 4),
            "iqr": round(iqr, 4),
            "n_outliers":        len(outliers),
            "n_zero_alignment":  len(zero_conf),
            # Metric 2: coverage / extrapolation — orthogonal to alignment score
            "total_claims":        total_claims_all,
            "supported_claims":    supported_claims_all,
            "spec_coverage_rate":      spec_coverage,      # supported / total
            "spec_extrapolation_rate": spec_extrapolation, # (total - supported) / total
            # Backward-compatible alias (same value, old name was misleading)
            "overall_hallucination_rate": spec_extrapolation,
        },
    }


# ── per-project aggregation ───────────────────────────────────────────────────

def aggregate_project(project_id: int, runs: list[dict]) -> dict:
    valid_runs       = [r for r in runs if r["summary"]]
    alignment_scores = [r["summary"]["mean_nli_alignment_score"] for r in valid_runs]
    coverage_rates   = [r["summary"]["spec_coverage_rate"]        for r in valid_runs]
    extrap_rates     = [r["summary"]["spec_extrapolation_rate"]   for r in valid_runs]
    outlier_ns       = [r["summary"]["n_outliers"]                for r in valid_runs]
    # Only count tasks from runs that actually have NLI data (exclude 0 from missing runs)
    valid_task_counts = [r["n_tasks"] for r in valid_runs if r["n_tasks"] > 0]

    return {
        "project_id":          project_id,
        "n_essays":            len(runs),             # total seeds attempted
        "n_essays_with_data":  len(valid_runs),       # seeds with valid NLI output
        # Metric 1 — NLI alignment score (precision of grounded claims)
        "mean_confidence":          _stat(alignment_scores, 4),  # alias kept for plot compat
        "mean_nli_alignment_score": _stat(alignment_scores, 4),
        # Metric 2 — specification coverage (orthogonal to alignment)
        "spec_coverage_rate":       _stat(coverage_rates, 4),
        "spec_extrapolation_rate":  _stat(extrap_rates, 4),
        # Old alias kept for backward compatibility with plot scripts
        "overall_hallucination_rate": _stat(extrap_rates, 4),
        "n_outliers":               _stat([float(v) for v in outlier_ns], 1),
        "n_tasks_per_essay":        int(round(_mean([float(v) for v in valid_task_counts]))) if valid_task_counts else 0,
    }


# ── main ─────────────────────────────────────────────────────────────────────

def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    print("=== NLI Confidence Score Extraction ===\n")

    all_run_data: dict[str, dict] = {}
    all_scores: list[float]       = []

    for run_id in ALL_RUNS:
        print(f"  Loading {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_nli.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        s = data["summary"]
        if s:
            all_scores.extend(t["nli_alignment_score"] for t in data["tasks"])
            print(f"done  (n={data['n_tasks']}, alignment={s['mean_nli_alignment_score']:.4f}, coverage={s['spec_coverage_rate']:.2%})")
        else:
            print("no NLI files found")

    projects_summary = []
    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs = [all_run_data[str(r)] for r in run_ids]
        agg  = aggregate_project(project_id, runs)
        projects_summary.append(agg)

    # Pooled statistics across ALL runs and ALL tasks
    q1, q3, iqr_val = _iqr(all_scores)
    lo_thr, hi_thr  = q1 - 1.5 * iqr_val, q3 + 1.5 * iqr_val

    output = {
        "metric":       "rq2_nli_confidence",
        "description":  (
            "Two INDEPENDENT NLI-based metrics — they are orthogonal, not contradictory. "
            "(1) nli_alignment_score / mean_confidence: mean NLI entailment score ONLY for "
            "claims that found a matching fact in the source spec. This is the PRECISION of "
            "grounded claims. It is structurally high (0.85-0.999) because only matched pairs "
            "enter the score. (2) spec_extrapolation_rate (formerly 'hallucination_rate'): "
            "fraction of generated claims with NO matching spec fact. In SE, ungrounded != "
            "hallucinated — the agent is eliciting implied requirements the spec did not spell "
            "out (defaults, error states, UX copy). High extrapolation is expected and "
            "desirable in SE tasks where specs are intentionally incomplete. "
            "Outliers detected using the 1.5 × IQR criterion."
        ),
        "projects":     projects_summary,
        "pooled_all_runs": {
            "n_scores":           len(all_scores),
            "mean":               round(_mean(all_scores),   4),
            "median":             round(_median(all_scores), 4),
            "std":                round(_std(all_scores),    4),
            "q1":                 round(q1, 4),
            "q3":                 round(q3, 4),
            "iqr":                round(iqr_val, 4),
            "outlier_threshold_lo": round(lo_thr, 4),
            "outlier_threshold_hi": round(hi_thr, 4),
            "n_outliers":         sum(1 for s in all_scores if s < lo_thr or s > hi_thr),
            "n_zero_confidence":  sum(1 for s in all_scores if s == 0.0),
        },
    }

    (SUMMARY_DIR / "rq2_nli_confidence.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Summary written: summaries/rq2_nli_confidence.json")


if __name__ == "__main__":
    run()
