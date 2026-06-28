"""
Canonical path resolution for all 12 experiment runs.

Run layout: experiments/project_{N} (essay {K})/
  - run.log
  - task_nli_*.json
  - task_implementation_order.json
  - formal_spec_*.als
  - dev/   (backend implementation)
  - frontend/

Projects: 1–4  |  Essays: 1–3  (3 seeds per project)
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent.parent
EXPERIMENTS  = REPO_ROOT / "experiments"
RESULTS_ROOT = Path(__file__).parent.parent

PROJECTS = [1, 2, 3, 4]
ESSAYS   = [1, 2, 3]


@dataclass(frozen=True)
class RunID:
    project: int   # 1-4
    essay:   int   # 1-3

    def __str__(self) -> str:
        return f"P{self.project}E{self.essay}"

    @property
    def folder_name(self) -> str:
        return f"project_{self.project} (essay {self.essay})"

    @property
    def path(self) -> Path:
        return EXPERIMENTS / self.folder_name

    @property
    def log_path(self) -> Path:
        return self.path / "run.log"

    @property
    def task_order_path(self) -> Path:
        return self.path / "task_implementation_order.json"

    @property
    def nli_paths(self) -> list[Path]:
        # Only return NLI files for tasks in the current task_implementation_order.json.
        # Stale files from earlier runs (different task IDs) are excluded to avoid
        # inflating task counts (e.g., P2E1 has a stale task_nli_19.json from a prior run).
        all_paths = sorted(self.path.glob("task_nli_*.json"))
        if not self.task_order_path.exists():
            return all_paths
        try:
            valid_ids = set(json.loads(self.task_order_path.read_text(encoding="utf-8")))
            return [p for p in all_paths if int(p.stem.rsplit("_", 1)[-1]) in valid_ids]
        except (json.JSONDecodeError, ValueError):
            return all_paths

    @property
    def alloy_paths(self) -> list[Path]:
        return sorted(self.path.glob("formal_spec_*.als"))

    @property
    def dev_path(self) -> Path:
        return self.path / "dev"

    @property
    def frontend_path(self) -> Path:
        return self.path / "frontend"

    def task_count(self) -> int:
        p = self.task_order_path
        if not p.exists():
            return 0
        d = json.loads(p.read_text(encoding="utf-8"))
        return len(d) if isinstance(d, list) else len(d.get("order", []))

    def exists(self) -> bool:
        return self.log_path.exists()


ALL_RUNS: list[RunID] = [
    RunID(project=p, essay=e)
    for p in PROJECTS
    for e in ESSAYS
    if RunID(project=p, essay=e).exists()
]

# Grouped by project: {project_id: [RunID, RunID, RunID]}
RUNS_BY_PROJECT: dict[int, list[RunID]] = {}
for run in ALL_RUNS:
    RUNS_BY_PROJECT.setdefault(run.project, []).append(run)
