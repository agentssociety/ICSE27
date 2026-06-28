"""
Test Pass Rate Extraction — RQ2 Implementation-Level Confidence
===============================================================

For each run (project_N, essay_K):
  Parse run.log for pytest result lines to get:
    - Backend:  passed / failed / skipped (unit + integration)
    - Frontend: passed / failed / skipped (jest/vitest)

  Pass rate = passed / (passed + failed)  [skipped excluded from denominator]

Aggregate per project: mean ± std across 3 essays.

Output:
  data/quality/P{N}E{K}_tests.json    — raw per-run data
  summaries/rq2_test_passrate.json    — aggregated mean ± std

Usage (from repo root):
  python -m research_results.scripts.extract_tests
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

# Pytest summary line: "X passed, Y failed, Z skipped in N.Ns"
_PYTEST_SUMMARY_RE = re.compile(
    r"=+\s*((?:\d+\s+\w+(?:,\s*)?)+)\s+in\s+[\d.]+s\s*=+"
)
_PYTEST_COUNT_RE   = re.compile(r"(\d+)\s+(passed|failed|skipped|error|warning)", re.I)

# Frontend test summary: jest/vitest
_JEST_SUMMARY_RE   = re.compile(
    r"Tests?:\s+(?:(\d+)\s+failed,\s*)?(\d+)\s+passed(?:,\s*(\d+)\s+total)?", re.I
)
_VITEST_SUMMARY_RE = re.compile(
    r"(\d+)\s+passed\s*\|\s*(\d+)\s+failed", re.I
)


def _clean(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _parse_pytest_results(text: str) -> tuple[int, int, int]:
    """Return (passed, failed, skipped) from the LAST pytest summary line."""
    passed = failed = skipped = 0
    for m in _PYTEST_SUMMARY_RE.finditer(text):
        block = m.group(1)
        counts = {kw: int(n) for n, kw in _PYTEST_COUNT_RE.findall(block)}
        passed  = counts.get("passed",  0)
        failed  = counts.get("failed",  0)
        skipped = counts.get("skipped", 0)
    return passed, failed, skipped


def _parse_frontend_results(text: str) -> tuple[int, int, int]:
    """Return (passed, failed, skipped) from frontend test summary."""
    passed = failed = skipped = 0
    for m in _JEST_SUMMARY_RE.finditer(text):
        failed  = int(m.group(1) or 0)
        passed  = int(m.group(2) or 0)
    for m in _VITEST_SUMMARY_RE.finditer(text):
        passed = int(m.group(1))
        failed = int(m.group(2))
    return passed, failed, skipped


def extract_run(run_id) -> dict:
    text = _clean(run_id.log_path.read_text(encoding="utf-8", errors="replace"))

    # Backend: parse from run.log (pytest output)
    be_passed, be_failed, be_skipped = _parse_pytest_results(text)

    # Frontend: look for jest/vitest output in run.log
    fe_passed, fe_failed, fe_skipped = _parse_frontend_results(text)

    # Also check frontend/.test_results.json if it exists
    fe_results_path = run_id.frontend_path / ".test_results.json"
    if fe_results_path.exists():
        try:
            fe_data = json.loads(fe_results_path.read_text(encoding="utf-8"))
            fe_passed  = fe_data.get("passed",  fe_passed)
            fe_failed  = fe_data.get("failed",  fe_failed)
            fe_skipped = fe_data.get("skipped", fe_skipped)
        except Exception:
            pass

    def _rate(p: int, f: int) -> float:
        total = p + f
        return round(p / total, 4) if total else 1.0  # no tests = treat as pass

    be_rate = _rate(be_passed, be_failed)
    fe_rate = _rate(fe_passed, fe_failed)
    combined_passed  = be_passed  + fe_passed
    combined_failed  = be_failed  + fe_failed
    combined_skipped = be_skipped + fe_skipped
    combined_rate    = _rate(combined_passed, combined_failed)

    return {
        "run_id":   str(run_id),
        "project":  run_id.project,
        "essay":    run_id.essay,
        "n_tasks":  run_id.task_count(),
        "backend": {
            "passed":   be_passed,
            "failed":   be_failed,
            "skipped":  be_skipped,
            "pass_rate": be_rate,
        },
        "frontend": {
            "passed":   fe_passed,
            "failed":   fe_failed,
            "skipped":  fe_skipped,
            "pass_rate": fe_rate,
        },
        "combined": {
            "passed":   combined_passed,
            "failed":   combined_failed,
            "skipped":  combined_skipped,
            "pass_rate": combined_rate,
        },
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

    print("=== Test Pass Rate Extraction ===\n")

    all_run_data: dict[str, dict] = {}
    for run_id in ALL_RUNS:
        print(f"  Parsing {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_tests.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        be = data["backend"]
        fe = data["frontend"]
        print(
            f"done  (backend: {be['passed']}P/{be['failed']}F/{be['skipped']}S "
            f"rate={be['pass_rate']:.1%}; "
            f"frontend: {fe['passed']}P/{fe['failed']}F rate={fe['pass_rate']:.1%})"
        )

    projects_summary = []
    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs = [all_run_data[str(r)] for r in run_ids]

        be_rates = [r["backend"]["pass_rate"]  for r in runs]
        fe_rates = [r["frontend"]["pass_rate"] for r in runs]
        co_rates = [r["combined"]["pass_rate"] for r in runs]

        projects_summary.append({
            "project_id": project_id,
            "n_essays":   len(runs),
            "backend_pass_rate":  _stat(be_rates, 4),
            "frontend_pass_rate": _stat(fe_rates, 4),
            "combined_pass_rate": _stat(co_rates, 4),
            "backend_passed_mean":  round(_mean([float(r["backend"]["passed"])  for r in runs]), 1),
            "backend_failed_mean":  round(_mean([float(r["backend"]["failed"])  for r in runs]), 1),
            "backend_skipped_mean": round(_mean([float(r["backend"]["skipped"]) for r in runs]), 1),
        })

    output = {
        "metric":       "rq2_test_passrate",
        "description":  (
            "Automated test pass rates measuring implementation-level confidence. "
            "Backend: pytest unit + integration tests. "
            "Frontend: jest/vitest component tests. "
            "Pass rate = passed / (passed + failed); skipped tests are excluded. "
            "Values reported as mean ± std across 3 essay seeds per project."
        ),
        "projects": projects_summary,
    }

    (SUMMARY_DIR / "rq2_test_passrate.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Summary written: summaries/rq2_test_passrate.json")


if __name__ == "__main__":
    run()
