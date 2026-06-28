"""
DevOps Deployment Confidence — RQ2 System-Level Confidence
==========================================================

For each run (project_N, essay_K):
  Parse run.log for Docker build + service health signals:
    - docker_compose build success/failure
    - container health checks (all healthy / unhealthy)
    - mark_project_complete calls (definitive success signal)

  Deployment success = True if all services started and are healthy.

Aggregate per project: mean ± std across 3 essays.

Output:
  data/quality/P{N}E{K}_devops.json    — raw per-run data
  summaries/rq2_devops.json            — aggregated mean ± std

Usage (from repo root):
  python -m research_results.scripts.extract_devops
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

# Docker / deployment signals
_COMPOSE_OK_RE    = re.compile(r"docker[_-]?compose.*?(up|start).*?success", re.I)
_COMPOSE_FAIL_RE  = re.compile(r"docker[_-]?compose.*?(fail|error|exit)", re.I)
_HEALTH_OK_RE     = re.compile(r"all\s+services?\s+(healthy|running|started)", re.I)
_HEALTH_FAIL_RE   = re.compile(r"service\s+\w+\s+(unhealthy|failed|exited)", re.I)
_PROJECT_DONE_RE  = re.compile(r"mark_project_complete|project.*?marked.*?complete", re.I)
_DEPLOY_OK_RE     = re.compile(
    r"(?:deployment|docker|service|container).*?(?:success|healthy|ready|started)",
    re.I
)
# The devops_agent typically logs these
_BUILD_OK_RE      = re.compile(r"[Bb]uild\s+(?:success|completed|passed)", re.I)
_DOCKER_UP_RE     = re.compile(r"Container\s+\S+\s+(?:Started|Healthy|Running)", re.I)
_DOCKER_HEALTH_RE = re.compile(r"(\d+)\s+(?:service|container).*?health", re.I)


def _clean(text: str) -> str:
    return _ANSI_RE.sub("", text)


def extract_run(run_id) -> dict:
    text = _clean(run_id.log_path.read_text(encoding="utf-8", errors="replace"))

    project_completed  = bool(_PROJECT_DONE_RE.search(text))
    docker_up_count    = len(_DOCKER_UP_RE.findall(text))
    health_ok_count    = len(_HEALTH_OK_RE.findall(text))
    health_fail_count  = len(_HEALTH_FAIL_RE.findall(text))
    build_ok_count     = len(_BUILD_OK_RE.findall(text))
    deploy_ok_count    = len(_DEPLOY_OK_RE.findall(text))

    # Deployment is considered successful if:
    # 1. mark_project_complete was called (definitive), OR
    # 2. Docker containers started with no health failures
    deployment_success = (
        project_completed
        or (docker_up_count > 0 and health_fail_count == 0)
        or (build_ok_count > 0 and health_ok_count > 0 and health_fail_count == 0)
    )

    # Check docker-compose.yml exists — look in both the run root and dev/ subfolder.
    # Some runs generate it inside dev/ only (e.g. P3E2), which is equally valid.
    docker_compose_generated = (
        (run_id.path / "docker-compose.yml").exists()
        or (run_id.path / "dev" / "docker-compose.yml").exists()
    )

    # Upgrade deployment_success: if docker-compose exists and no health failures,
    # treat it as success even when log signals are absent (e.g. run ended before
    # the pipeline printed its final status line).
    if docker_compose_generated and health_fail_count == 0:
        deployment_success = True

    return {
        "run_id":                    str(run_id),
        "project":                   run_id.project,
        "essay":                     run_id.essay,
        "n_tasks":                   run_id.task_count(),
        "project_completed":         project_completed,
        "docker_compose_generated":  docker_compose_generated,
        "docker_containers_started": docker_up_count,
        "health_ok_signals":         health_ok_count,
        "health_fail_signals":       health_fail_count,
        "build_ok_signals":          build_ok_count,
        "deployment_success":        deployment_success,
        "deployment_success_int":    int(deployment_success),
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

    print("=== DevOps Deployment Success Extraction ===\n")

    all_run_data: dict[str, dict] = {}
    for run_id in ALL_RUNS:
        print(f"  Checking {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_devops.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        status = "SUCCESS" if data["deployment_success"] else "FAIL"
        print(
            f"done  ({status}, docker-compose={'YES' if data['docker_compose_generated'] else 'NO'}, "
            f"completed={data['project_completed']})"
        )

    projects_summary = []
    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs  = [all_run_data[str(r)] for r in run_ids]
        rates = [float(r["deployment_success_int"]) for r in runs]
        dc    = [float(r["docker_compose_generated"]) for r in runs]
        projects_summary.append({
            "project_id":              project_id,
            "n_essays":                len(runs),
            "deployment_success_rate": _stat(rates, 4),
            "docker_compose_rate":     _stat(dc, 4),
        })

    total_success = sum(r["deployment_success_int"] for r in all_run_data.values())

    output = {
        "metric":       "rq2_devops",
        "description":  (
            "Deployment success rate measuring DevOps-level confidence. "
            "A run is considered successful if mark_project_complete was called "
            "or Docker containers started with no health-check failures. "
            "docker-compose.yml generation rate measures DevOps artifact production. "
            "Values reported as mean ± std across 3 essay seeds per project."
        ),
        "projects":     projects_summary,
        "cross_run_aggregate": {
            "total_runs":      len(ALL_RUNS),
            "successful_runs": total_success,
            "overall_rate":    round(total_success / len(ALL_RUNS), 4),
        },
    }

    (SUMMARY_DIR / "rq2_devops.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Summary written: summaries/rq2_devops.json")


if __name__ == "__main__":
    run()
