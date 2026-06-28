"""
Code-Level Hallucination Extraction — RQ2 Groundedness
========================================================

For each run (project_N, essay_K):
  Detect structural hallucinations in generated backend/frontend code:
    1. Orphan routes      — API routes with no corresponding service/handler
    2. Schema mismatches  — frontend types inconsistent with backend DTOs
    3. Unused imports     — import statements for modules never used in the file

  Also extract task-level hallucination from NLI files:
    - ungrounded_rate = 1 - (supported_claims / total_claims) per task
    - mean ungrounded rate per run

Aggregate per project: mean ± std across 3 essays.

Output:
  data/hallucination/P{N}E{K}_halluc.json     — raw per-run data
  summaries/rq2_hallucination.json            — aggregated mean ± std

Usage (from repo root):
  python -m research_results.scripts.extract_hallucination
"""
from __future__ import annotations

import ast
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT, RESULTS_ROOT

DATA_DIR    = RESULTS_ROOT / "data" / "hallucination"
SUMMARY_DIR = RESULTS_ROOT / "summaries"

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mABCDEFGHJKLMSTfhinrsu]")

# Router definition patterns (FastAPI)
_ROUTE_RE     = re.compile(
    r'@(?:router|app)\.(?:get|post|put|patch|delete|head|options)\s*\(\s*["\']([^"\']+)["\']',
)
# Function/class definition
_FUNC_RE      = re.compile(r'^(?:def|async def|class)\s+(\w+)', re.M)
# Import statements
_IMPORT_RE    = re.compile(r'^(?:import\s+(\S+)|from\s+(\S+)\s+import\s+(.+))$', re.M)
# TypeScript interface/type field
_TS_FIELD_RE  = re.compile(r'(\w+)\s*[?:]?\s*:\s*([^;,\n]+)')
# Python DTO field (Pydantic)
_PY_FIELD_RE  = re.compile(r'(\w+)\s*:\s*([^\n=]+?)(?:\s*=|\n)')

# Fields to ignore in schema comparison
_SKIP_FIELDS  = {"id", "created_at", "updated_at", "deleted_at", "model_config",
                 "class_validators", "Config"}

if hasattr(sys, "stdlib_module_names"):
    _STDLIB = sys.stdlib_module_names
else:
    _STDLIB = {
        "abc", "ast", "asyncio", "builtins", "collections", "contextlib",
        "copy", "dataclasses", "datetime", "enum", "functools", "hashlib",
        "http", "importlib", "io", "itertools", "json", "logging", "math",
        "operator", "os", "pathlib", "pickle", "re", "shutil", "signal",
        "socket", "sqlite3", "string", "struct", "subprocess", "sys",
        "tempfile", "threading", "time", "traceback", "types", "typing",
        "unittest", "urllib", "uuid", "warnings", "__future__",
        "typing_extensions",
    }


# ── code analysis ─────────────────────────────────────────────────────────────

def _detect_unused_imports(py_src: str) -> list[str]:
    """Detect imported names not used in the body."""
    try:
        tree = ast.parse(py_src)
    except SyntaxError:
        return []

    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != "*":
                    imported.add(alias.asname or alias.name)

    # Names used in the file body
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                used.add(node.value.id)

    return [n for n in imported if n not in used and n not in _STDLIB]


def _scan_backend(dev_path: Path) -> dict:
    """Scan backend generated code for hallucination patterns."""
    if not dev_path.exists():
        return {"orphan_routes": 0, "unused_imports": 0, "schema_mismatches": 0, "files_scanned": 0}

    py_files = list(dev_path.rglob("*.py"))
    # Exclude test files and __pycache__
    py_files = [f for f in py_files if "__pycache__" not in str(f)
                and not f.name.startswith("test_")]

    all_routes:    set[str] = set()
    all_handlers:  set[str] = set()
    unused_total:  int      = 0

    for fpath in py_files:
        try:
            src = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        # Route definitions
        for m in _ROUTE_RE.finditer(src):
            all_routes.add(m.group(1))

        # Handler / function definitions
        for m in _FUNC_RE.finditer(src):
            all_handlers.add(m.group(1))

        # Unused imports
        unused_total += len(_detect_unused_imports(src))

    # Orphan routes: routes whose path fragment doesn't appear as a handler name
    orphan_routes = sum(
        1 for r in all_routes
        if not any(seg.strip("/").replace("-", "_") in all_handlers
                   for seg in r.split("/") if seg)
    )

    return {
        "files_scanned":  len(py_files),
        "total_routes":   len(all_routes),
        "orphan_routes":  orphan_routes,
        "unused_imports": unused_total,
        "schema_mismatches": 0,  # requires frontend TS files; computed separately
    }


def _scan_frontend(frontend_path: Path, dev_path: Path) -> int:
    """Return count of schema mismatches between backend DTOs and frontend types."""
    if not frontend_path.exists() or not dev_path.exists():
        return 0

    # Extract backend DTO field names
    backend_fields: dict[str, set[str]] = defaultdict(set)
    for fpath in dev_path.rglob("*.py"):
        if "dto" in fpath.name or "schema" in fpath.name:
            try:
                src = fpath.read_text(encoding="utf-8", errors="replace")
                for m in _PY_FIELD_RE.finditer(src):
                    fname = m.group(1)
                    if fname not in _SKIP_FIELDS and not fname.startswith("_"):
                        backend_fields[fpath.stem].add(fname)
            except Exception:
                continue

    # Extract frontend TS type field names
    frontend_fields: dict[str, set[str]] = defaultdict(set)
    for fpath in frontend_path.rglob("*.ts"):
        if "__pycache__" in str(fpath) or "node_modules" in str(fpath):
            continue
        try:
            src = fpath.read_text(encoding="utf-8", errors="replace")
            for m in _TS_FIELD_RE.finditer(src):
                fname = m.group(1)
                if fname not in _SKIP_FIELDS and not fname.startswith("_"):
                    frontend_fields[fpath.stem].add(fname)
        except Exception:
            continue

    # Count mismatches: backend field not present in any frontend type file
    mismatches = 0
    for entity, fields in backend_fields.items():
        # Try to find a matching frontend file (name similarity)
        fe_match = next(
            (fe_fields for fe_name, fe_fields in frontend_fields.items()
             if entity.replace("_", "").lower() in fe_name.replace("_", "").lower()
             or fe_name.replace("_", "").lower() in entity.replace("_", "").lower()),
            None
        )
        if fe_match:
            mismatches += len(fields - fe_match - _SKIP_FIELDS)

    return mismatches


def extract_run(run_id) -> dict:
    # Code-level hallucinations
    backend_data = _scan_backend(run_id.dev_path)
    schema_mismatches = _scan_frontend(run_id.frontend_path, run_id.dev_path)
    backend_data["schema_mismatches"] = schema_mismatches

    # Task-level specification extrapolation from NLI files.
    # NOTE: "ungrounded" claims are NOT hallucinations in the SE sense —
    # they are claims the agent elicited beyond the spec (implied requirements,
    # defaults, error copy). This is expected and often desirable.
    total_claims = supported_claims = 0
    task_extrap_rates: list[float] = []
    task_coverage_rates: list[float] = []
    for nli_path in run_id.nli_paths:
        data = json.loads(nli_path.read_text(encoding="utf-8"))
        tot  = int(data["total_claims"])
        sup  = int(data["supported_claims"])
        total_claims     += tot
        supported_claims += sup
        if tot > 0:
            task_extrap_rates.append(1 - sup / tot)
            task_coverage_rates.append(sup / tot)

    mean_task_extrap   = round(sum(task_extrap_rates)   / len(task_extrap_rates),   4) if task_extrap_rates   else 0.0
    mean_task_coverage = round(sum(task_coverage_rates) / len(task_coverage_rates), 4) if task_coverage_rates else 1.0
    overall_extrap     = round(1 - supported_claims / total_claims, 4) if total_claims else 0.0
    overall_coverage   = round(supported_claims / total_claims, 4)     if total_claims else 1.0

    return {
        "run_id":   str(run_id),
        "project":  run_id.project,
        "essay":    run_id.essay,
        "n_tasks":  run_id.task_count(),
        "code_structural_issues": {
            "files_scanned":     backend_data["files_scanned"],
            "total_routes":      backend_data["total_routes"],
            "orphan_routes":     backend_data["orphan_routes"],
            "unused_imports":    backend_data["unused_imports"],
            "schema_mismatches": schema_mismatches,
        },
        # backward-compat alias
        "code_hallucination": {
            "files_scanned":     backend_data["files_scanned"],
            "total_routes":      backend_data["total_routes"],
            "orphan_routes":     backend_data["orphan_routes"],
            "unused_imports":    backend_data["unused_imports"],
            "schema_mismatches": schema_mismatches,
        },
        "task_spec_extrapolation": {
            "total_claims":       total_claims,
            "supported_claims":   supported_claims,
            "n_tasks_with_nli":   len(task_extrap_rates),
            # extrapolation = fraction of claims beyond the spec (not wrong, just untraced)
            "overall_extrapolation_rate": overall_extrap,
            "mean_task_extrapolation":    mean_task_extrap,
            # coverage = fraction of claims traceable to spec (the inverse)
            "overall_coverage_rate": overall_coverage,
            "mean_task_coverage":    mean_task_coverage,
            # backward-compat field name
            "overall_rate": overall_extrap,
        },
        # backward-compat alias
        "task_hallucination": {
            "total_claims":     total_claims,
            "supported_claims": supported_claims,
            "n_tasks_with_nli": len(task_extrap_rates),
            "overall_rate":     overall_extrap,
            "mean_task_rate":   mean_task_extrap,
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

    print("=== Code Hallucination Extraction ===\n")

    all_run_data: dict[str, dict] = {}
    for run_id in ALL_RUNS:
        print(f"  Scanning {run_id.folder_name} ...", end=" ", flush=True)
        data = extract_run(run_id)
        all_run_data[str(run_id)] = data
        out = DATA_DIR / f"{run_id}_halluc.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        ch = data["code_hallucination"]
        th = data["task_hallucination"]
        print(
            f"done  (orphans={ch['orphan_routes']}, unused_imports={ch['unused_imports']}, "
            f"schema_mm={ch['schema_mismatches']}, task_hall={th['overall_rate']:.1%})"
        )

    projects_summary = []
    for project_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        runs = [all_run_data[str(r)] for r in run_ids]

        orphan    = [float(r["code_hallucination"]["orphan_routes"])     for r in runs]
        unused    = [float(r["code_hallucination"]["unused_imports"])    for r in runs]
        schema    = [float(r["code_hallucination"]["schema_mismatches"]) for r in runs]
        extrap    = [r["task_spec_extrapolation"]["overall_extrapolation_rate"] for r in runs]
        coverage  = [r["task_spec_extrapolation"]["overall_coverage_rate"]      for r in runs]

        projects_summary.append({
            "project_id":     project_id,
            "n_essays":       len(runs),
            # Code structural issues (these ARE true defects, not elicitation)
            "orphan_routes":  _stat(orphan, 2),
            "unused_imports": _stat(unused, 2),
            "schema_mismatches": _stat(schema, 2),
            # Spec extrapolation (renamed from hallucination_rate)
            "spec_extrapolation_rate": _stat(extrap, 4),
            "spec_coverage_rate":      _stat(coverage, 4),
            # Backward-compat alias used by plot_rq2.py and latex_tables.py
            "task_hallucination_rate": _stat(extrap, 4),
            "overall_hallucination_rate": _stat(extrap, 4),
        })

    output = {
        "metric":       "rq2_hallucination",
        "description":  (
            "Two DISTINCT categories — do not conflate them. "
            "(A) Code structural issues: defects in generated code that are always errors. "
            "Orphan routes: FastAPI route decorators with no matching handler function. "
            "Unused imports: names imported but absent from all ast.Name/ast.Attribute uses. "
            "Schema mismatches: backend DTO fields absent from frontend type definitions. "
            "(B) Spec extrapolation rate: fraction of user-story claims not traceable to "
            "the source specification (1 - supported_claims / total_claims from NLI). "
            "These are NOT hallucinations — in SE, specifications are incomplete by design "
            "and the agent is expected to elicit implied requirements (defaults, error states, "
            "UX copy) that the spec never mentioned. High extrapolation is expected and often "
            "desirable. 50% extrapolation means 1 implied claim per explicit spec claim. "
            "spec_coverage_rate = 1 - spec_extrapolation_rate. "
            "Values reported as mean ± std across 3 essay seeds per project."
        ),
        "projects": projects_summary,
    }

    (SUMMARY_DIR / "rq2_hallucination.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n  Summary written: summaries/rq2_hallucination.json")


if __name__ == "__main__":
    run()
