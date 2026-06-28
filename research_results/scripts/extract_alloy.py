"""
Alloy Formal Specification Verification Rate — RQ2 System-Level Confidence
===========================================================================

For each run (project_N, essay_K):
  1. Count .als spec files (one per task)
  2. Parse run.log for "verified successfully" / "failed" patterns
     (Alloy check results emitted by the verify_all_specifications tool)
  3. Scan each .als file for [[INVALID_BLOCK_MARKER]] — inserted by the
     pipeline when a code block could not be fixed after max retries.
     Such blocks are commented out with `--` and left with a marker comment.
     A spec file containing any INVALID_BLOCK_MARKER is counted as FAILED
     (the agent could not fix the spec; it remains partially disabled).
  4. Compute verification rate = verified / total_specs

The fallback rule (assume pass if no failure logged) is overridden by the
INVALID_BLOCK_MARKER scan: a file with a marker is always a failure even if
the log shows no explicit failure message.

Aggregate per project: mean ± std across 3 essays.

Output:
  data/quality/P{N}E{K}_alloy.json      — raw per-run data
  summaries/rq2_alloy_verification.json — aggregated mean ± std

Usage (from repo root):
  python -m research_results.scripts.extract_alloy
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT, RESULTS_ROOT

DATA_DIR    = RESULTS_ROOT / "data" / "quality"
SUMMARY_DIR = RESULTS_ROOT / "summaries"

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mABCDEFGHJKLMSTfhinrsu]")

# Patterns from verify_all_specifications output in run.log
_ALLOY_OK_RE      = re.compile(r"Spec\s+.*?\.als.*?verified\s+successfully", re.I)
_ALLOY_FAIL_RE    = re.compile(r"Spec\s+.*?\.als.*?(failed|error|invalid)", re.I)
_ALLOY_TOOL_RE    = re.compile(r"verify_all_specifications.*?(\d+)/(\d+)\s+spec", re.I)
# Broader pattern: alloy check lines
_ALLOY_CHECK_RE   = re.compile(r"alloy.*?(pass|ok|verified|fail|error)", re.I)
_SPEC_VERIFIED_RE = re.compile(r"(\d+)\s+spec.*?verified", re.I)
_SPEC_RESULT_RE   = re.compile(
    r"formal[_\s]spec.*?result.*?(\d+)/(\d+)", re.I
)
# The verify output format: "All N specifications verified" or "N/M verified"
_ALL_VERIFIED_RE  = re.compile(r"[Aa]ll\s+(\d+)\s+spec.*?verified", re.I)
_PARTIAL_VERIF_RE = re.compile(r"(\d+)\s*/\s*(\d+)\s+spec.*?verif", re.I)
_ALLOY_ASSERT_RE  = re.compile(r"(?:PASS|FAIL)\s*\(Alloy", re.I)


_INVALID_MARKER = "[[INVALID_BLOCK_MARKER]]"


def _clean(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _count_invalid_blocks(als_path: Path) -> int:
    """Count INVALID_BLOCK_MARKER occurrences in a .als file.

    The pipeline inserts this marker when a code block could not be fixed
    after exhausting the retry budget, then comments out the broken block.
    Each occurrence = one pred/assert/check block that remains disabled.
    """
    try:
        text = als_path.read_text(encoding="utf-8", errors="replace")
        return text.count(_INVALID_MARKER)
    except OSError:
        return 0


def extract_run(run_id) -> dict:
    als_paths    = run_id.alloy_paths
    n_spec_files = len(als_paths)

    # --- Static scan: count specs with any INVALID_BLOCK_MARKER ---
    commented_specs: list[str] = []
    for p in als_paths:
        if _count_invalid_blocks(p) > 0:
            commented_specs.append(p.name)
    n_commented = len(commented_specs)

    # Parse run.log for alloy verification outcomes
    text = _clean(run_id.log_path.read_text(encoding="utf-8", errors="replace"))

    verified = 0
    failed   = 0

    # Strategy 1: look for "All N specifications verified" summary lines
    for m in _ALL_VERIFIED_RE.finditer(text):
        v = int(m.group(1))
        verified = max(verified, v)

    # Strategy 2: look for "N/M specifications verified" patterns
    for m in _PARTIAL_VERIF_RE.finditer(text):
        v, tot = int(m.group(1)), int(m.group(2))
        verified = max(verified, v)
        failed   = max(failed, tot - v)

    # Strategy 3: count individual spec ok/fail lines
    if verified == 0:
        ok_n    = len(_ALLOY_OK_RE.findall(text))
        fail_n  = len(_ALLOY_FAIL_RE.findall(text))
        if ok_n > 0 or fail_n > 0:
            verified = ok_n
            failed   = fail_n

    # Fallback: if we see no verification output but have spec files,
    # check if the log contains a formal spec phase at all
    spec_phase_present = "formal_spec" in text.lower() or "alloy" in text.lower()

    # If n_spec_files is known and no failures detected, assume all passed
    # (the system only proceeds if specs pass; explicit failures are logged)
    if verified == 0 and n_spec_files > 0 and spec_phase_present and failed == 0:
        verified = n_spec_files

    total_specs = max(n_spec_files, verified + failed)

    # Override with static scan: specs with INVALID_BLOCK_MARKER are failures
    # even if the log did not record an explicit failure.  A commented block
    # means the agent gave up and left the spec partially disabled.
    if n_commented > 0:
        # n_commented specs are definitely failed; adjust verified downward
        failed   = max(failed, n_commented)
        verified = max(0, total_specs - failed)

    verif_rate = round(verified / total_specs, 4) if total_specs else 0.0

    return {
        "run_id":            str(run_id),
        "project":           run_id.project,
        "essay":             run_id.essay,
        "n_tasks":           run_id.task_count(),
        "spec_files":        n_spec_files,
        "verified_specs":    verified,
        "failed_specs":      failed,
        "total_specs":       total_specs,
        "verification_rate": verif_rate,
        # Specs where the agent commented out blocks it could not fix
        "n_commented_block_specs": n_commented,
        "commented_block_specs":   commented_specs,
    }


# ── stats helpers ─────────────────────────────────────────────────────────────

def _mean(v: list[float]) -> float: return sum(v) / len(v) if v else 0.0
def _std(v: list[float]) -> float:
    if len(v) < 2: return 0.0
    m = _mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))

def _stat(vals: list[float], decimals: int = 4) -> dict:
    return {
        "mean":   round(_mean(vals),   decimals),
        "std":    round(_std(vals),    decimals),
        "values": [round(v, decimals) for v in vals],
    }


# ── main ─────────────────────────────────────────────────────────────────────

def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Alloy Specification Verification Extraction ===\n")

    all_run_data: dict[str, dict] = {}
    for run_id in ALL_RUNS:
        print(f"  Checking {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_alloy.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        commented_note = (
            f", {data['n_commented_block_specs']} spec(s) with commented blocks"
            if data["n_commented_block_specs"] else ""
        )
        print(
            f"done  ({data['verified_specs']}/{data['total_specs']} verified, "
            f"rate={data['verification_rate']:.0%}{commented_note})"
        )

    projects_summary = []
    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs  = [all_run_data[str(r)] for r in run_ids]
        rates = [r["verification_rate"] for r in runs]
        total = [float(r["total_specs"])    for r in runs]
        verif = [float(r["verified_specs"]) for r in runs]
        projects_summary.append({
            "project_id":        project_id,
            "n_essays":          len(runs),
            "verification_rate": _stat(rates, 4),
            "total_specs":       _stat(total, 1),
            "verified_specs":    _stat(verif, 1),
        })

    # Cross-run totals
    all_total     = sum(r["total_specs"]              for r in all_run_data.values())
    all_verif     = sum(r["verified_specs"]           for r in all_run_data.values())
    all_commented = sum(r["n_commented_block_specs"]  for r in all_run_data.values())

    output = {
        "metric":       "rq2_alloy_verification",
        "description":  (
            "Alloy formal specification verification rate. "
            "Each task produces one .als spec file; the verify_all_specifications "
            "tool runs Alloy's SAT solver to check all assert/check commands. "
            "Rate = verified_specs / total_specs per run. "
            "A spec is counted as FAILED if (a) the log records an explicit failure, "
            "OR (b) the file contains [[INVALID_BLOCK_MARKER]] — a marker the pipeline "
            "inserts when a code block could not be fixed after max retries and was "
            "commented out. Such specs remain partially disabled; the agent gave up. "
            "Values reported as mean ± std across 3 essay seeds per project."
        ),
        "projects":      projects_summary,
        "cross_run_aggregate": {
            "total_runs":              len(ALL_RUNS),
            "total_specs":             all_total,
            "verified_specs":          all_verif,
            "failed_specs":            all_total - all_verif,
            "specs_with_commented_blocks": all_commented,
            "overall_rate":            round(all_verif / all_total, 4) if all_total else 0.0,
        },
    }

    (SUMMARY_DIR / "rq2_alloy_verification.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Summary written: summaries/rq2_alloy_verification.json")


if __name__ == "__main__":
    run()
