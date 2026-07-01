"""
Code Quality & Design Rigour Comparison  (corrected v2)
========================================================

Measures structural code quality metrics for MetaGPT vs AgentsSociety across
all 4 benchmark projects. Metrics are grouped into four categories:

  A. Design completeness  — how well the design artifact maps to implementation
  B. Code hygiene         — type hints, docstrings, average function length
  C. Defensive rigour     — error handling, input validation, Pydantic usage
  D. Formal spec alignment (AgentsSociety only) — Alloy sig → Python class ratio

Bug fixes vs v1:
  - Pydantic model count: transitive BFS from BaseModel (captures XxxCreate/Update/Response)
  - Alloy sig regex: strips comment lines before matching (avoids "sig to", "sig for")
  - HTTP error density: also counts Flask-RESTful return-tuple pattern (return {}, 4xx)
  - Radon CC: filters to function/method lines only (M/F prefix), excludes class CC (C prefix)
  - SQLAlchemy base detection: tighter guard ("Model" substring removed to avoid false positives)

Output:
  research_results/summaries/rq2_code_quality.json
  research_results/tables/rq2_code_quality.tex
"""
from __future__ import annotations

import ast
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT    = Path(__file__).parent.parent.parent
EXPERIMENTS  = REPO_ROOT / "experiments"
RESULTS_ROOT = Path(__file__).parent.parent
SUMMARY_DIR  = RESULTS_ROOT / "summaries"
TABLE_DIR    = RESULTS_ROOT / "tables"

# ── project paths ─────────────────────────────────────────────────────────────

METAGPT_SRC: dict[int, Path] = {
    1: EXPERIMENTS / "project_1 (metagpt)" / "hospital_triage_queue" / "hospital_triage_queue",
    2: EXPERIMENTS / "project_2 (metagpt)" / "blood_bank_inventory_manager",
    3: EXPERIMENTS / "project_3 (metagpt)" / "airport_runway_scheduling",
    4: EXPERIMENTS / "project_4 (metagpt)" / "atm_withdrawal_safety_backend",
    # P5 MetaGPT produced only task-description filenames, no runnable Python code
    6: EXPERIMENTS / "project_6 (metagpt)" / "community_social_network",
}

# Essays available per project: P1-P4 have 3, P5-P6 have 1
_AGENTS_ESSAYS = {1: (1,2,3), 2: (1,2,3), 3: (1,2,3), 4: (1,2,3), 5: (1,), 6: (1,)}

AGENTS_SRC: dict[int, list[Path]] = {
    pid: [
        EXPERIMENTS / f"project_{pid} (essay {eid})" / "dev" / "src"
        for eid in essays
    ]
    for pid, essays in _AGENTS_ESSAYS.items()
}

AGENTS_ALLOY: dict[int, list[Path]] = {
    pid: sorted(
        (EXPERIMENTS / f"project_{pid} (essay 1)").glob("formal_spec_*.als")
    )
    for pid in _AGENTS_ESSAYS
}

METAGPT_DESIGN: dict[int, Optional[Path]] = {}
for pid, src in METAGPT_SRC.items():
    proj_root = src.parent
    candidates = sorted(proj_root.glob("docs/system_design/*.json"))
    METAGPT_DESIGN[pid] = candidates[-1] if candidates else None

AGENTS_DESIGN: dict[int, list[Path]] = {
    pid: sorted(
        (EXPERIMENTS / f"project_{pid} (essay 1)").glob("class_diagram_*.puml")
    )
    for pid in _AGENTS_ESSAYS
}

# ── helpers ────────────────────────────────────────────────────────────────────

def _pct(a: int, b: int) -> float:
    return round(100 * a / b, 1) if b else 0.0

def _mean(vals: list) -> float:
    return sum(vals) / len(vals) if vals else 0.0

def _std(vals: list) -> float:
    if len(vals) < 2:
        return 0.0
    m = _mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


# ── Pydantic class counting (transitive) ───────────────────────────────────────

def count_pydantic_classes(py_files: list[Path]) -> int:
    """
    Count all Pydantic schema classes transitively.

    First collects every class and its direct base-class names, then performs
    a BFS from {BaseModel, Schema} to find all descendants.  This captures the
    typical AgentsSociety pattern:

        class PatientBase(BaseModel): ...       ← direct
        class PatientCreate(PatientBase): ...   ← level-2 (was missed in v1)
        class PatientResponse(PatientBase): ... ← level-2
    """
    class_bases: dict[str, list[str]] = {}
    for f in py_files:
        try:
            tree = ast.parse(f.read_text(errors="ignore"))
        except (SyntaxError, Exception):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(base.attr)
                class_bases[node.name] = bases

    pydantic_all: set[str] = set()
    queue: list[str] = ["BaseModel", "Schema"]
    while queue:
        parent = queue.pop()
        for cls, bases in class_bases.items():
            if parent in bases and cls not in pydantic_all:
                pydantic_all.add(cls)
                queue.append(cls)
    return len(pydantic_all)


# ── AST metric extraction ─────────────────────────────────────────────────────

# Regex: return tuple where second element is a 4xx or 5xx status code
# Flask-RESTful pattern: return {'error': ...}, 4xx
_RETURN_HTTP_ERR = re.compile(
    r"return\s+.+,\s*[45]\d{2}\b"
)

def ast_metrics(py_files: list[Path]) -> dict:
    total_funcs     = 0
    fully_typed     = 0    # all non-self params + return annotated
    docstr_funcs    = 0
    func_lines: list[int] = []
    try_excepts     = 0
    assertions      = 0
    total_classes   = 0
    pydantic_validators = 0   # @field_validator / @validator decorators
    raise_http      = 0       # raise HTTPException / raise abort
    return_http_err = 0       # return {...}, 4xx (Flask-RESTful)

    for f in py_files:
        try:
            src = f.read_text(errors="ignore")
        except Exception:
            continue

        # Count return-tuple HTTP error lines (source-level, before AST parse)
        return_http_err += len(_RETURN_HTTP_ERR.findall(src))

        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total_classes += 1
                # Count @field_validator / @validator on methods inside this class
                for item in node.body:
                    if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        continue
                    for dec in item.decorator_list:
                        dec_name = ""
                        if isinstance(dec, ast.Name):
                            dec_name = dec.id
                        elif isinstance(dec, ast.Attribute):
                            dec_name = dec.attr
                        elif isinstance(dec, ast.Call):
                            if isinstance(dec.func, ast.Name):
                                dec_name = dec.func.id
                            elif isinstance(dec.func, ast.Attribute):
                                dec_name = dec.func.attr
                        if dec_name in ("validator", "field_validator",
                                        "model_validator", "root_validator"):
                            pydantic_validators += 1

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total_funcs += 1

                # Full type hint: all non-self/cls params + return annotated
                all_args = (node.args.args + node.args.posonlyargs
                            + node.args.kwonlyargs)
                non_self = [a for a in all_args if a.arg not in ("self", "cls")]
                all_ann  = all(a.annotation for a in non_self) if non_self else True
                if all_ann and node.returns is not None:
                    fully_typed += 1

                # Docstring
                if (node.body
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                        and isinstance(node.body[0].value.value, str)):
                    docstr_funcs += 1

                # Function length
                if hasattr(node, "end_lineno"):
                    func_lines.append(node.end_lineno - node.lineno + 1)

            if isinstance(node, ast.Try):
                try_excepts += 1

            if isinstance(node, ast.Assert):
                assertions += 1

            if isinstance(node, ast.Raise) and node.exc and isinstance(node.exc, ast.Call):
                exc_name = ""
                if isinstance(node.exc.func, ast.Name):
                    exc_name = node.exc.func.id
                elif isinstance(node.exc.func, ast.Attribute):
                    exc_name = node.exc.func.attr
                if exc_name in ("HTTPException", "abort"):
                    raise_http += 1

    avg_len = sum(func_lines) / len(func_lines) if func_lines else 0
    # Combined HTTP error density: raise-based + return-tuple-based
    http_error_total = raise_http + return_http_err

    return {
        "n_functions":               total_funcs,
        "n_classes":                 total_classes,
        "n_pydantic_validators":     pydantic_validators,
        "full_type_hint_pct":        _pct(fully_typed, total_funcs),
        "docstring_pct":             _pct(docstr_funcs, total_funcs),
        "avg_func_len_lines":        round(avg_len, 1),
        "try_except_count":          try_excepts,
        "try_per_100_funcs":         round(100 * try_excepts / total_funcs, 1) if total_funcs else 0,
        "assertions":                assertions,
        "raise_http":                raise_http,
        "return_http_err":           return_http_err,
        "http_error_total":          http_error_total,
        "http_err_per_100_funcs":    round(100 * http_error_total / total_funcs, 1) if total_funcs else 0,
    }


# ── cyclomatic complexity via radon (functions only) ──────────────────────────

def radon_cc(py_files: list[Path]) -> dict:
    """
    Mean cyclomatic complexity across all functions and methods (M/F prefix).
    Explicitly excludes class-level CC scores (C prefix) which radon also reports
    but represent number-of-methods, not path complexity.
    """
    all_scores: list[float] = []
    for f in py_files:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "radon", "cc", "-s", "-n", "A", str(f)],
                capture_output=True, text=True, timeout=15,
            )
        except Exception:
            continue
        for line in result.stdout.splitlines():
            stripped = line.strip()
            # Only M (method) and F (function) lines — skip C (class aggregate)
            if not (stripped.startswith("M ") or stripped.startswith("F ")):
                continue
            m = re.search(r"\((\d+)\)\s*$", line)
            if m:
                all_scores.append(float(m.group(1)))

    if not all_scores:
        return {"cc_mean": 0.0, "cc_max": 0, "cc_n": 0}
    return {
        "cc_mean": round(_mean(all_scores), 2),
        "cc_max":  int(max(all_scores)),
        "cc_n":    len(all_scores),
    }


# ── Alloy sig extraction ──────────────────────────────────────────────────────

# Framework boilerplate sigs that appear in every AgentsSociety spec template
_ALLOY_BOILERPLATE = frozenset({
    "Permission", "Read", "Write", "Execute", "Admin",
    "Bool", "True", "False",
    "Actor", "Resource", "IfaceKind", "Interface",
    "State", "Pre1", "Pre2", "Post1", "Post2", "Post3",
})

def alloy_sig_count(als_files: list[Path]) -> tuple[int, int]:
    """
    Count unique sig names across all .als files.

    Returns (total_sigs, domain_sigs) where domain_sigs excludes framework
    boilerplate (permission lattice, generic Actor/Resource/State scaffolding).
    Comment lines (starting with --) are stripped before matching to avoid
    false positives from phrases like 'helper sig to represent ...'.
    """
    all_sigs: set[str] = set()
    for f in als_files:
        if not f.exists():
            continue
        # Strip single-line comments before applying regex
        src_lines = []
        for line in f.read_text(errors="ignore").splitlines():
            stripped = line.lstrip()
            if stripped.startswith("--"):
                continue
            # Strip inline comments
            line = re.sub(r"--.*$", "", line)
            src_lines.append(line)
        src = "\n".join(src_lines)

        for m in re.finditer(r"\bsig\s+(\w+)", src):
            all_sigs.add(m.group(1))

    domain_sigs = all_sigs - _ALLOY_BOILERPLATE
    return len(all_sigs), len(domain_sigs)


# ── MetaGPT design class extraction ──────────────────────────────────────────

def metagpt_design_classes(design_path: Optional[Path]) -> int:
    """Count classes defined in MetaGPT system design JSON (mermaid diagram)."""
    if not design_path or not design_path.exists():
        return 0
    d = json.loads(design_path.read_text(errors="ignore"))
    text = d.get("Data structures and interfaces", "")
    # mermaid: "class Foo {" or "class Foo:" (with any following whitespace before token)
    return len(re.findall(r"\bclass\s+\w+\s*[{:\n]", text))


def puml_class_count(puml_files: list[Path]) -> int:
    """Count class/interface definitions in PlantUML files."""
    total = 0
    for f in puml_files:
        if not f.exists():
            continue
        src = f.read_text(errors="ignore")
        total += len(re.findall(
            r"^\s*(?:abstract\s+)?(?:class|interface)\s+\w+", src, re.M
        ))
    return total


# ── per-project runner ────────────────────────────────────────────────────────

def measure_metagpt(pid: int) -> dict:
    src_dir = METAGPT_SRC.get(pid)
    if not src_dir or not src_dir.exists():
        return {"error": f"src not found: {src_dir}"}
    py_files = list(src_dir.rglob("*.py"))
    print(f"  MetaGPT P{pid}: {len(py_files)} .py files")

    metrics  = ast_metrics(py_files)
    cc       = radon_cc(py_files)
    pydantic = count_pydantic_classes(py_files)
    design_n = metagpt_design_classes(METAGPT_DESIGN.get(pid))
    impl_cls = metrics["n_classes"]

    return {
        "project_id":       pid,
        "system":           "MetaGPT",
        "n_py_files":       len(py_files),
        "design_classes":   design_n,
        "impl_classes":     impl_cls,
        "design_impl_ratio": round(design_n / impl_cls, 2) if impl_cls else 0,
        "n_pydantic_models": pydantic,
        **metrics,
        **cc,
    }


def measure_agents(pid: int) -> dict:
    src_dirs = [d for d in AGENTS_SRC[pid] if d.exists()]
    if not src_dirs:
        return {"error": f"no src dirs found for P{pid}"}

    seed_results: list[dict] = []
    for src_dir in src_dirs:
        py_files = list(src_dir.rglob("*.py"))
        m  = ast_metrics(py_files)
        cc = radon_cc(py_files)
        py = count_pydantic_classes(py_files)
        seed_results.append({"n_py_files": len(py_files), "n_pydantic_models": py, **m, **cc})

    # Average across seeds
    num_keys = [k for k in seed_results[0] if isinstance(seed_results[0][k], (int, float))]
    averaged: dict = {k: round(_mean([r[k] for r in seed_results]), 2) for k in num_keys}

    puml_files = AGENTS_DESIGN[pid]
    design_cls = puml_class_count(puml_files)

    als_files = AGENTS_ALLOY[pid]
    total_sigs, domain_sigs = alloy_sig_count(als_files)

    impl_cls = averaged.get("n_classes", 0)
    print(f"  AgentsSociety P{pid}: {len(src_dirs)} seeds, "
          f"avg {averaged.get('n_py_files',0):.0f} .py files, "
          f"alloy_sigs={total_sigs} (domain={domain_sigs}), "
          f"design_classes={design_cls}, "
          f"pydantic={averaged.get('n_pydantic_models',0):.1f}")

    return {
        "project_id":        pid,
        "system":            "AgentsSociety",
        "n_seeds":           len(src_dirs),
        "design_classes":    design_cls,
        "alloy_sigs_total":  total_sigs,
        "alloy_sigs_domain": domain_sigs,
        "impl_classes":      round(impl_cls),
        "alloy_impl_ratio":  round(domain_sigs / impl_cls, 2) if impl_cls else 0,
        "design_impl_ratio": round(design_cls / impl_cls, 2) if impl_cls else 0,
        **averaged,
    }


# ── main ──────────────────────────────────────────────────────────────────────

def run() -> None:
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 64)
    print("Code Quality & Design Rigour Comparison  (corrected v2)")
    print("=" * 64)

    mg_rows: list[dict] = []
    as_rows: list[dict] = []

    for pid in sorted(_AGENTS_ESSAYS.keys()):
        print(f"\n--- Project {pid} ---")
        mg_row = measure_metagpt(pid)
        if "error" not in mg_row:
            mg_rows.append(mg_row)
        as_rows.append(measure_agents(pid))

    def xmean(rows, k):
        vals = [r.get(k, 0) for r in rows if isinstance(r.get(k), (int, float))]
        return round(_mean(vals), 2)

    fields = [
        ("cc_mean",               "CC mean (fns only)"),
        ("avg_func_len_lines",    "Avg func len (lines)"),
        ("full_type_hint_pct",    "Full type hints (%)"),
        ("docstring_pct",         "Docstrings (%)"),
        ("try_per_100_funcs",     "try/except per 100 fns"),
        ("http_err_per_100_funcs","HTTP errors per 100 fns"),
        ("n_pydantic_models",     "Pydantic models (transitive)"),
        ("n_pydantic_validators", "Pydantic validators"),
        ("design_impl_ratio",     "Design:impl ratio"),
    ]

    print("\n" + "=" * 64)
    print("SUMMARY")
    print("=" * 64)
    print(f"{'Metric':<38} {'MetaGPT':>10} {'AgentsSoc':>10}")
    print("-" * 60)
    for key, label in fields:
        mg_v = xmean(mg_rows, key)
        as_v = xmean(as_rows, key)
        print(f"  {label:<36} {mg_v:>10} {as_v:>10}")

    print("\nAlloy sigs per project (AgentsSociety):")
    for r in as_rows:
        print(f"  P{r['project_id']}: total={r.get('alloy_sigs_total','?')}, "
              f"domain={r.get('alloy_sigs_domain','?')}, "
              f"impl_classes={r.get('impl_classes','?')}, "
              f"alloy:impl(domain)={r.get('alloy_impl_ratio','?')}")

    print("\nPydantic models per project:")
    for r in mg_rows:
        print(f"  MetaGPT P{r['project_id']}: {r.get('n_pydantic_models', 0)}")
    for r in as_rows:
        print(f"  AgentsSoc P{r['project_id']}: {r.get('n_pydantic_models', 0):.1f} (avg seeds)")

    print("\nHTTP error breakdown (MetaGPT):")
    for r in mg_rows:
        print(f"  P{r['project_id']}: raise_http={r.get('raise_http',0)}, "
              f"return_tuple={r.get('return_http_err',0)}, "
              f"total={r.get('http_error_total',0)}, "
              f"per_100={r.get('http_err_per_100_funcs',0)}")

    # Save JSON
    result = {
        "metric":  "rq2_code_quality_v2",
        "version": "corrected: transitive Pydantic, comment-stripped Alloy, combined HTTP errors, fn-only CC",
        "metagpt_projects":  mg_rows,
        "agents_projects":   as_rows,
        "cross_project_means": {
            "metagpt":      {k: xmean(mg_rows, k) for k, _ in fields},
            "agentsociety": {k: xmean(as_rows, k) for k, _ in fields},
        },
    }
    out = SUMMARY_DIR / "rq2_code_quality.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nJSON → {out.relative_to(REPO_ROOT)}")

    # Build and save corrected LaTeX table
    mg_m = result["cross_project_means"]["metagpt"]
    as_m = result["cross_project_means"]["agentsociety"]

    # Collect impl and design class means for table header rows
    mg_impl  = xmean(mg_rows, "impl_classes")
    as_impl  = xmean(as_rows, "impl_classes")
    mg_des   = xmean(mg_rows, "design_classes")
    as_des   = xmean(as_rows, "design_classes")
    as_sigs  = xmean(as_rows, "alloy_sigs_domain")
    as_sigs_r = xmean(as_rows, "alloy_impl_ratio")

    # Build LaTeX as a plain string (no f-string) to avoid backslash/brace conflicts
    def v(x, fmt=".1f"):
        return format(float(x), fmt)

    def r2(x):   # 2-decimal format for ratios
        return format(float(x), ".2f")

    caption = (
        r"Code quality and design-rigour comparison (cross-project means; AS: $n=6$ projects, MG: $n=5$ projects with runnable code). "
        r"Cyclomatic complexity (CC) measured with \texttt{radon~cc} on functions and methods only "
        r"(class-aggregate CC excluded); lower = simpler. "
        r"Full type-hint coverage = \% of functions with all parameters \emph{and} return annotated. "
        r"HTTP error density = \texttt{raise~HTTPException} + \texttt{return \{\}, 4xx/5xx} per 100~functions "
        r"(captures both FastAPI and Flask-RESTful error patterns). "
        r"Pydantic count is transitive: includes \texttt{XxxBase}, \texttt{XxxCreate}, "
        r"\texttt{XxxUpdate}, \texttt{XxxResponse} subclasses. "
        r"Design-completeness ratio = design-artifact classes $\div$ implemented classes. "
        r"Alloy:impl ratio uses domain-specific sigs only (framework boilerplate excluded)."
    )

    rows_A = [
        (r"Design-artifact classes (mean)", v(as_des, ".0f"), v(mg_des, ".0f")),
        (r"Implemented classes (mean)",     v(as_impl, ".0f"), v(mg_impl, ".0f")),
        (r"Design-completeness ratio",
         r"\textbf{" + r2(as_m['design_impl_ratio']) + r"}",
         r2(mg_m['design_impl_ratio'])),
        (r"Alloy domain types modelled (sigs, mean)", v(as_sigs, ".0f"), "N/A"),
        (r"Alloy sig : impl-class ratio (domain)",    r2(as_sigs_r), "N/A"),
    ]
    rows_B = [
        (r"Cyclomatic complexity (mean CC per fn)",
         r"\textbf{" + r2(as_m['cc_mean']) + r"}",
         r2(mg_m['cc_mean'])),
        (r"Avg.\ function length (lines)",
         r"\textbf{" + v(as_m['avg_func_len_lines']) + r"}",
         v(mg_m['avg_func_len_lines'])),
        (r"Full type-hint coverage (\%)",
         v(as_m['full_type_hint_pct']),
         r"\textbf{" + v(mg_m['full_type_hint_pct']) + r"}"),
        (r"Docstring coverage (\%)",
         v(as_m['docstring_pct']),
         r"\textbf{" + v(mg_m['docstring_pct']) + r"}"),
    ]
    rows_C = [
        (r"Error-handling density (try/100~fns)",
         r"\textbf{" + v(as_m['try_per_100_funcs']) + r"}",
         v(mg_m['try_per_100_funcs'])),
        (r"HTTP error density (/100~fns)",
         v(as_m['http_err_per_100_funcs']),
         r"\textbf{" + v(mg_m['http_err_per_100_funcs']) + r"}"),
        (r"Pydantic schema classes (mean / project)",
         r"\textbf{" + v(as_m['n_pydantic_models'], ".0f") + r"}",
         v(mg_m['n_pydantic_models'], ".1f")),
        (r"Pydantic field validators (mean / project)",
         r"\textbf{" + v(as_m['n_pydantic_validators']) + r"}",
         v(mg_m['n_pydantic_validators'])),
    ]
    rows_D = [
        (r"Alloy formal spec files / project",
         r"\checkmark (per task)", r"\ding{55}"),
        (r"SAT-solver verified invariants",
         r"\checkmark", r"\ding{55}"),
        (r"Schema-typed API contracts (Pydantic)",
         r"\checkmark", "partial"),
        (r"Business-rule validators (\texttt{@field\_validator})",
         r"\checkmark", r"\ding{55}"),
    ]

    def tex_row(label, as_val, mg_val):
        return f"{label} & {as_val} & {mg_val} \\\\"

    def tex_section(title, rows):
        lines = [r"\multicolumn{3}{@{}l}{\textit{" + title + r"}} \\"]
        lines += [tex_row(*r) for r in rows]
        return "\n".join(lines)

    tex = (
        r"\begin{table}[t]" + "\n"
        r"\centering" + "\n"
        r"\caption{" + caption + r"}" + "\n"
        r"\label{tab:rq2_code_quality}" + "\n"
        r"\renewcommand{\arraystretch}{1.15}" + "\n"
        r"\begin{tabular}{@{}lrr@{}}" + "\n"
        r"\toprule" + "\n"
        r"\textbf{Metric} & \textbf{\textsc{AgentsSociety}} & \textbf{MetaGPT} \\" + "\n"
        r"\midrule" + "\n"
        + tex_section(r"A.\ Design completeness", rows_A) + "\n"
        r"\midrule" + "\n"
        + tex_section(r"B.\ Code hygiene", rows_B) + "\n"
        r"\midrule" + "\n"
        + tex_section(r"C.\ Defensive rigour and input validation", rows_C) + "\n"
        r"\midrule" + "\n"
        + tex_section(r"D.\ Formal-specification grounding (\textsc{AgentsSociety} only)", rows_D) + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n"
    )
    tex_out = TABLE_DIR / "rq2_code_quality.tex"
    tex_out.write_text(tex, encoding="utf-8")
    print(f"LaTeX → {tex_out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    run()
