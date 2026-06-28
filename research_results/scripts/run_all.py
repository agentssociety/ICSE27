"""
Master Pipeline — Generate All Research Results
================================================

Runs all extraction scripts in order, then generates figures and LaTeX tables.

Order:
  1.  extract_tokens_per_task  → rq2_tokens_per_task.json, rq2_latency_per_task.json
  2.  extract_errors           → rq1a_autonomy.json
  3.  extract_orchestration    → rq1b_coordination.json
  4.  extract_nli              → rq2_nli_confidence.json
  5.  extract_alloy            → rq2_alloy_verification.json
  6.  extract_tests            → rq2_test_passrate.json
  7.  extract_devops           → rq2_devops.json
  8.  extract_hallucination    → rq2_hallucination.json
  9.  plot_rq1                 → figures/fig_rq1a_*, fig_rq1b_*  (PNG + PDF)
  10. plot_rq2                 → figures/fig_rq2_*               (PNG + PDF)
  11. latex_tables             → tables/*.tex

Usage (from repo root):
  python -m research_results.scripts.run_all [--no-plots] [--no-tables]

All outputs are written to research_results/summaries/, research_results/data/,
research_results/figures/, and research_results/tables/.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT


def _banner(title: str) -> None:
    width = 70
    print()
    print("═" * width)
    print(f"  {title}")
    print("═" * width)


def main(plots: bool = True, tables: bool = True) -> None:
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          AgentsSociety — Research Results Extraction Pipeline        ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  Runs discovered: {len(ALL_RUNS)}")
    for proj_id, runs in sorted(RUNS_BY_PROJECT.items()):
        n_tasks = runs[0].task_count()
        print(f"    Project {proj_id}: {len(runs)} seeds × {n_tasks} tasks")
    print()

    t0 = time.time()

    # ── 1. Tokens & Latency ───────────────────────────────────────────────────
    _banner("Step 1/8 — Token & Latency Extraction (per task, per phase)")
    from research_results.scripts.extract_tokens_per_task import run as run_tokens
    run_tokens()

    # ── 2. Error Incidents (RQ1a) ─────────────────────────────────────────────
    _banner("Step 2/8 — Error Incident Extraction (RQ1a Autonomy)")
    from research_results.scripts.extract_errors import run as run_errors
    run_errors()

    # ── 3. Orchestration Metrics (RQ1b) ───────────────────────────────────────
    _banner("Step 3/8 — Orchestration Metric Extraction (RQ1b Coordination)")
    from research_results.scripts.extract_orchestration import run as run_orch
    run_orch()

    # ── 4. NLI Confidence ────────────────────────────────────────────────────
    _banner("Step 4/8 — NLI Confidence Score Extraction")
    from research_results.scripts.extract_nli import run as run_nli
    run_nli()

    # ── 5. Alloy Verification ─────────────────────────────────────────────────
    _banner("Step 5/8 — Alloy Specification Verification Extraction")
    from research_results.scripts.extract_alloy import run as run_alloy
    run_alloy()

    # ── 6. Test Pass Rates ────────────────────────────────────────────────────
    _banner("Step 6/8 — Test Pass Rate Extraction")
    from research_results.scripts.extract_tests import run as run_tests
    run_tests()

    # ── 7. DevOps Deployment ─────────────────────────────────────────────────
    _banner("Step 7/8 — DevOps Deployment Success Extraction")
    from research_results.scripts.extract_devops import run as run_devops
    run_devops()

    # ── 8. Code Structural Issues ───────────────────────────────────────────
    _banner("Step 8/13 — Code Structural Issue Extraction (orphan routes, unused imports)")
    from research_results.scripts.extract_hallucination import run as run_halluc
    run_halluc()

    # ── 8b. Task Hallucination (Deleted Tasks) ───────────────────────────────
    _banner("Step 8b/13 — Task Hallucination: Deleted Task Detection")
    from research_results.scripts.extract_task_hallucination import run as run_task_halluc
    run_task_halluc()

    # ── 9. Gantt Execution Traces ─────────────────────────────────────────────
    if plots:
        _banner("Step 9/12 — Execution Trace Gantt (4 projects × 3 seeds + radar)")
        from research_results.scripts.plot_gantt import run as run_gantt
        run_gantt()

    # ── 10. RQ1 Figures ──────────────────────────────────────────────────────
    if plots:
        _banner("Step 10/12 — RQ1 Figures (error analysis + coordination metrics)")
        from research_results.scripts.plot_rq1 import run as run_plot_rq1
        run_plot_rq1()

    # ── 11. RQ2 Figures ──────────────────────────────────────────────────────
    if plots:
        _banner("Step 11/12 — RQ2 Figures (tokens, latency, NLI, quality dashboard)")
        from research_results.scripts.plot_rq2 import run as run_plot_rq2
        run_plot_rq2()

    # ── 12. LaTeX Tables ─────────────────────────────────────────────────────
    if tables:
        _banner("Step 12/12 — LaTeX Table Generation")
        from research_results.scripts.latex_tables import run as run_tables
        run_tables()

    elapsed = time.time() - t0
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print(f"║  Pipeline complete in {elapsed:.1f}s".ljust(71) + "║")
    print("║  summaries/ · figures/ · tables/ all written                        ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()

    # Print summary of generated files
    from research_results.scripts.paths import RESULTS_ROOT
    summary_dir = RESULTS_ROOT / "summaries"
    files = sorted(summary_dir.glob("*.json"))
    print("  JSON summaries:")
    for f in files:
        size_kb = f.stat().st_size / 1024
        print(f"    {f.name:<45} {size_kb:6.1f} KB")

    if plots:
        fig_dir = RESULTS_ROOT / "figures"
        figs = sorted(fig_dir.glob("*.png"))
        if figs:
            print("\n  Figures (PNG):")
            for f in figs:
                size_kb = f.stat().st_size / 1024
                print(f"    {f.name:<45} {size_kb:6.1f} KB")

    if tables:
        table_dir = RESULTS_ROOT / "tables"
        tex_files = sorted(table_dir.glob("*.tex"))
        if tex_files:
            print("\n  LaTeX tables:")
            for f in tex_files:
                print(f"    {f.name}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-plots",  action="store_true", help="Skip figure generation")
    parser.add_argument("--no-tables", action="store_true", help="Skip LaTeX table generation")
    args = parser.parse_args()
    main(plots=not args.no_plots, tables=not args.no_tables)
