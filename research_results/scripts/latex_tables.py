"""
LaTeX Table Generation for ICSE Paper
======================================

Generates camera-ready LaTeX tables for:
  - Table 1: RQ1a Autonomy metrics (SR, incidents, wall-clock)
  - Table 2: RQ1b Coordination metrics (PL, DS, steps, backtracks)
  - Table 3: RQ2 System Quality (Alloy, tests, deployment)
  - Table 4: RQ2 Token & Latency per phase (top-5 phases)
  - Table 5: RQ2 Code Hallucination summary

Output directory: research_results/tables/
Files: rq1a_autonomy.tex, rq1b_coordination.tex, rq2_quality.tex,
       rq2_cost.tex, rq2_hallucination.tex

Usage:
  python -m research_results.scripts.latex_tables
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from research_results.scripts.paths import RESULTS_ROOT

SUMMARY_DIR = RESULTS_ROOT / "summaries"
TABLE_DIR   = RESULTS_ROOT / "tables"

PROJ_NAMES = {
    1: "Hospital Triage",
    2: "Blood-Type Alert",
    3: "Airport Runway",
    4: "ATM Withdrawal",
    5: "Competency Platform",
    6: "Social Network",
}

ICSE_HEADER = r"""\usepackage{booktabs}
\usepackage{multirow}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{siunitx}
"""

# Pastel row colors in LaTeX (light enough for text, distinct per project)
ROW_COLORS = {
    1: r"\rowcolor[HTML]{E8F4FF}",   # pastel blue
    2: r"\rowcolor[HTML]{E8F5E8}",   # pastel green
    3: r"\rowcolor[HTML]{FEF7E0}",   # pastel amber
    4: r"\rowcolor[HTML]{F8EAF2}",   # pastel rose
    5: r"\rowcolor[HTML]{EAF0FF}",   # pastel indigo
    6: r"\rowcolor[HTML]{FFF5E0}",   # pastel gold
}
BEST_COLOR  = r"\cellcolor[HTML]{D6EFD6}"   # soft green
WORST_COLOR = r"\cellcolor[HTML]{FDDADA}"   # soft red
MEAN_COLOR  = r"\cellcolor[HTML]{FFF9D6}"   # soft yellow


def _pct(v: float, digits: int = 1) -> str:
    return f"{v:.{digits}f}\\%"

def _f(v: float, digits: int = 1) -> str:
    return f"{v:.{digits}f}"

def _i(v: float) -> str:
    return f"{round(v)}"

def _ms(mean: float, std: float, fmt=_f, digits: int = 1) -> str:
    return rf"{fmt(mean, digits)} \pm {fmt(std, digits)}"

def _ms_pct(mean: float, std: float, digits: int = 1) -> str:
    return rf"{mean:.{digits}f}\% $\pm$ {std:.{digits}f}\%"

def _wrap(body: str, caption: str, label: str, footnote: str = "", star: bool = True) -> str:
    fn_block = (
        rf"\footnotesize {footnote}" + "\n"
        if footnote else ""
    )
    env = "table*" if star else "table"
    return (
        rf"\begin{{{env}}}[t]" + "\n"
        rf"\centering" + "\n"
        rf"\caption{{{caption}}}" + "\n"
        rf"\label{{{label}}}" + "\n"
        rf"\renewcommand{{\arraystretch}}{{1.15}}" + "\n"
        + body + "\n"
        + fn_block
        + rf"\end{{{env}}}" + "\n"
    )


def _best_worst_cells(values: list[float], fmt_fn, higher_is_better: bool = True):
    """Return list of LaTeX cell strings, colour-coding best and worst."""
    if not values:
        return ["--"] * len(values)
    ranked = sorted(enumerate(values), key=lambda x: x[1])
    if higher_is_better:
        worst_i = ranked[0][0]
        best_i  = ranked[-1][0]
    else:
        worst_i = ranked[-1][0]
        best_i  = ranked[0][0]
    cells = []
    for i, v in enumerate(values):
        s = fmt_fn(v)
        if i == best_i:
            cells.append(rf"{BEST_COLOR} {s}")
        elif i == worst_i:
            cells.append(rf"{WORST_COLOR} {s}")
        else:
            cells.append(s)
    return cells


def _rank_colors(vals: list, higher_is_better: bool = False) -> list:
    """Return 'cgood'/'cmid'/'cbad' for each position (best/middle/worst)."""
    ranked = sorted(range(len(vals)), key=lambda i: vals[i])
    best_i  = ranked[-1] if higher_is_better else ranked[0]
    worst_i = ranked[0]  if higher_is_better else ranked[-1]
    return [
        "cgood" if i == best_i else "cbad" if i == worst_i else "cmid"
        for i in range(len(vals))
    ]


# ══════════════════════════════════════════════════════════════════════════════
# Table 1 — RQ1a Autonomy
# ══════════════════════════════════════════════════════════════════════════════

def _table_rq1a() -> str:
    d = json.loads((SUMMARY_DIR / "rq1a_autonomy.json").read_text())

    lines = [
        r"\begin{tabular}{@{}lrrrrrr@{}}",
        r"\toprule",
        r"\multirow{2}{*}{\textbf{Project}} & "
        r"\multicolumn{2}{c}{\textbf{Incidents}} & "
        r"\multirow{2}{*}{\textbf{Steps}} & "
        r"\multirow{2}{*}{\textbf{SR (\%)}} & "
        r"\multirow{2}{*}{\textbf{Escalated}} & "
        r"\multirow{2}{*}{\textbf{Wall-clock (min)}} \\",
        r"\cmidrule(lr){2-3}",
        r" & Total & Fixed & & & & \\",
        r"\midrule",
    ]

    sr_vals  = []
    projects = sorted(d["projects"], key=lambda p: p["project_id"])
    for proj in projects:
        pid  = proj["project_id"]
        name = PROJ_NAMES[pid]
        rc   = ROW_COLORS[pid]

        tot_m = proj["total_incidents"]["mean"]
        tot_s = proj["total_incidents"]["std"]
        fix_m = proj["fixed_incidents"]["mean"]
        fix_s = proj["fixed_incidents"]["std"]
        stp_m = proj["pipeline_steps"]["mean"]
        stp_s = proj["pipeline_steps"]["std"]
        sr_m  = proj["self_fix_rate_pct"]["mean"]
        sr_s  = proj["self_fix_rate_pct"]["std"]
        esc_m = proj["escalated_incidents"]["mean"]
        esc_s = proj["escalated_incidents"]["std"]
        wc_m  = proj["wall_clock_s"]["mean"] / 60
        wc_s  = proj["wall_clock_s"]["std"]  / 60

        sr_vals.append(sr_m)

        lines.append(
            rf"{rc} {name} & "
            rf"${_i(tot_m)} \pm {_i(tot_s)}$ & "
            rf"${_i(fix_m)} \pm {_i(fix_s)}$ & "
            rf"${_i(stp_m)} \pm {_i(stp_s)}$ & "
            rf"$\mathbf{{{_f(sr_m)}}} \pm {_f(sr_s)}$ & "
            rf"${_i(esc_m)} \pm {_i(esc_s)}$ & "
            rf"${_f(wc_m)} \pm {_f(wc_s)}$ \\"
        )

    # Mean row
    lines.append(r"\midrule")
    all_sr_m = sum(sr_vals) / len(sr_vals) if sr_vals else 0
    lines.append(
        rf"\textit{{Overall mean}} & & & & "
        rf"$\mathbf{{{_f(all_sr_m)}}}$ & & \\"
    )
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")

    body = "\n".join(lines)
    return _wrap(
        body,
        caption=(
            r"RQ1a: Autonomy Metrics per Project (mean $\pm$ std, $n=3$ seeds). "
            r"SR~=~Self-Fix Rate (\%), Incidents detected and resolved by the "
            r"orchestrating agent without human intervention. "
            r"\textbf{Best SR} highlighted \colorbox[HTML]{D6EFD6}{green}, "
            r"worst \colorbox[HTML]{FDDADA}{red}."
        ),
        label="tab:rq1a_autonomy",
        footnote=(
            r"Wall-clock time measured from first to last log timestamp per run. "
            r"All values report sample std (ddof=1)."
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Table 2 — RQ1b Coordination
# ══════════════════════════════════════════════════════════════════════════════

def _table_rq1b() -> str:
    d = json.loads((SUMMARY_DIR / "rq1b_coordination.json").read_text())
    projects = sorted(d["projects"], key=lambda p: p["project_id"])

    def gm(proj, key):
        return proj[key]["mean"]

    def gs(proj, key):
        return proj[key]["std"]

    means = {
        "steps":    [gm(p, "pipeline_steps")        for p in projects],
        "bktracks": [gm(p, "phase_backtracks")       for p in projects],
        "reentry":  [gm(p, "phase_reentries")        for p in projects],
        "overhead": [gm(p, "orch_overhead_pct")      for p in projects],
        "smdel":    [gm(p, "sm_delegations")         for p in projects],
        "redel":    [gm(p, "redelegations")          for p in projects],
        "esczone":  [gm(p, "escalation_zone_pct")    for p in projects],
        "pl":       [gm(p, "PL") * 100              for p in projects],
        "ds":       [gm(p, "DS") * 100              for p in projects],
        "tinc":     [gm(p, "total_incidents")        for p in projects],
        "escalat":  [gm(p, "escalated_incidents")    for p in projects],
        "sr":       [gm(p, "SR")                    for p in projects],
    }
    stds = {
        "steps":    [gs(p, "pipeline_steps")        for p in projects],
        "bktracks": [gs(p, "phase_backtracks")       for p in projects],
        "reentry":  [gs(p, "phase_reentries")        for p in projects],
        "overhead": [gs(p, "orch_overhead_pct")      for p in projects],
        "smdel":    [gs(p, "sm_delegations")         for p in projects],
        "redel":    [gs(p, "redelegations")          for p in projects],
        "esczone":  [gs(p, "escalation_zone_pct")    for p in projects],
        "pl":       [gs(p, "PL") * 100              for p in projects],
        "ds":       [gs(p, "DS") * 100              for p in projects],
        "tinc":     [gs(p, "total_incidents")        for p in projects],
        "escalat":  [gs(p, "escalated_incidents")    for p in projects],
        "sr":       [gs(p, "SR")                    for p in projects],
    }

    def _row(label: str, key: str, fmt, hib: bool = False, nocolor: bool = False) -> str:
        ms = means[key]
        ss = stds[key]
        if nocolor:
            cells = " & ".join(
                rf"{{\scriptsize${fmt(m)}\pm{fmt(s)}$}}" for m, s in zip(ms, ss)
            )
        else:
            colors = _rank_colors(ms, higher_is_better=hib)
            cells = " & ".join(
                rf"\cellcolor{{{c}}}{{\scriptsize${fmt(m)}\pm{fmt(s)}$}}"
                for c, m, s in zip(colors, ms, ss)
            )
        return rf"{label} & {cells} \\"

    lines = [
        r"\setlength{\tabcolsep}{5pt}",
        r"\renewcommand{\arraystretch}{1.18}",
        r"\footnotesize",
        r"\begin{tabularx}{\linewidth}{"
        r">{\raggedright\arraybackslash\hsize=1.8\hsize}X "
        r">{\raggedleft\arraybackslash\hsize=0.8\hsize}X "
        r">{\raggedleft\arraybackslash\hsize=0.8\hsize}X "
        r">{\raggedleft\arraybackslash\hsize=0.8\hsize}X "
        r">{\raggedleft\arraybackslash\hsize=0.8\hsize}X}",
        r"\toprule",
        (r"\rowcolor{chdr}"
         r"\textcolor{white}{\textbf{Metric}} & "
         r"\textcolor{white}{\textbf{P1}} & "
         r"\textcolor{white}{\textbf{P2}} & "
         r"\textcolor{white}{\textbf{P3}} & "
         r"\textcolor{white}{\textbf{P4}} \\"),
        r"\midrule",
        r"\rowcolor{csec}\multicolumn{5}{l}{\textit{Execution Dynamics}} \\",
        _row(r"Pipeline steps $\downarrow$",           "steps",    _i),
        _row(r"Phase back-tracks $\downarrow$",        "bktracks", _i),
        _row(r"Phase re-entries $\downarrow$",         "reentry",  _i),
        _row(r"Orch.\ overhead (\%) $\downarrow$",     "overhead", _f),
        r"\rowcolor{csec}\multicolumn{5}{l}{\textit{Delegation Quality}} \\",
        _row("SM delegations",                         "smdel",    _i,  nocolor=True),
        _row(r"Re-delegations $\downarrow$",           "redel",    _i),
        _row(r"Escalation zone (\%) $\downarrow$",     "esczone",  _f),
        _row(r"PL (\%) $\uparrow$",                   "pl",       _f,  hib=True),
        _row(r"DS (\%) $\uparrow$",                   "ds",       _f,  hib=True),
        r"\rowcolor{csec}\multicolumn{5}{l}{\textit{Recovery Behavior}} \\",
        _row(r"Total incidents $\downarrow$",          "tinc",     _i),
        _row(r"Escalated incidents $\downarrow$",      "escalat",  _i),
        _row(r"SR (\%) $\uparrow$",                   "sr",       _f,  hib=True),
        r"\bottomrule",
        r"\end{tabularx}",
    ]

    body = "\n".join(lines)
    return _wrap(
        body,
        caption=(
            r"RQ1b: Orchestration coordination metrics across 4 benchmark projects "
            r"(mean $\pm$ std, $n=3$ seeds). "
            r"\colorbox{cgood}{\phantom{x}}~best~$\cdot$~"
            r"\colorbox{cmid}{\phantom{x}}~middle~$\cdot$~"
            r"\colorbox{cbad}{\phantom{x}}~worst per row. "
            r"PL~=~Path Linearity; DS~=~Delegation Stability; SR~=~Self-Fix Rate."
        ),
        label="tab:rq1b_coordination",
        footnote=(
            r"SM~delegations are informational (no coloring). "
            r"Esc.\ zone~=~fraction of phases containing $\geq 1$ escalated incident."
        ),
        star=False,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Table 3 — RQ2 System Quality
# ══════════════════════════════════════════════════════════════════════════════

def _table_rq2_quality() -> str:
    alloy  = json.loads((SUMMARY_DIR / "rq2_alloy_verification.json").read_text())["projects"]
    tests  = json.loads((SUMMARY_DIR / "rq2_test_passrate.json").read_text())["projects"]
    devops = json.loads((SUMMARY_DIR / "rq2_devops.json").read_text())["projects"]
    nli    = json.loads((SUMMARY_DIR / "rq2_nli_confidence.json").read_text())["projects"]

    # Index by project id
    alloy_d  = {p["project_id"]: p for p in alloy}
    tests_d  = {p["project_id"]: p for p in tests}
    devops_d = {p["project_id"]: p for p in devops}
    nli_d    = {p["project_id"]: p for p in nli}

    lines = [
        r"\begin{tabular}{@{}lrrrrr@{}}",
        r"\toprule",
        r"\textbf{Project} & "
        r"\textbf{Alloy verif.} & "
        r"\textbf{BE pass rate} & "
        r"\textbf{FE pass rate} & "
        r"\textbf{Deployment} & "
        r"\textbf{NLI confidence} \\",
        r"\midrule",
    ]

    for pid in sorted(alloy_d):
        name = PROJ_NAMES[pid]
        rc   = ROW_COLORS[pid]

        av_m = alloy_d[pid]["verification_rate"]["mean"] * 100
        av_s = alloy_d[pid]["verification_rate"]["std"]  * 100

        be_m = tests_d[pid]["backend_pass_rate"]["mean"]  * 100
        be_s = tests_d[pid]["backend_pass_rate"]["std"]   * 100
        fe_m = tests_d[pid]["frontend_pass_rate"]["mean"] * 100
        fe_s = tests_d[pid]["frontend_pass_rate"]["std"]  * 100

        dp_m = devops_d[pid]["deployment_success_rate"]["mean"] * 100
        dp_s = devops_d[pid]["deployment_success_rate"]["std"]  * 100

        if pid in nli_d:
            nc_m = nli_d[pid]["mean_confidence"]["mean"] * 100
            nc_s = nli_d[pid]["mean_confidence"]["std"]  * 100
            nc_cell = rf"${_f(nc_m)}\% \pm {_f(nc_s)}\%$"
        else:
            nc_cell = r"---\tablefootnote{P3E2 NLI data missing}"

        lines.append(
            rf"{rc} {name} & "
            rf"${_f(av_m)}\% \pm {_f(av_s)}\%$ & "
            rf"${_f(be_m)}\% \pm {_f(be_s)}\%$ & "
            rf"${_f(fe_m)}\% \pm {_f(fe_s)}\%$ & "
            rf"${_f(dp_m)}\% \pm {_f(dp_s)}\%$ & "
            rf"{nc_cell} \\"
        )

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")

    body = "\n".join(lines)
    return _wrap(
        body,
        caption=(
            r"RQ2: System-Level Confidence Metrics per Project (mean $\pm$ std, $n=3$ seeds). "
            r"Alloy: SAT-solver verification of formal specifications. "
            r"BE/FE pass rate: pytest / jest, skipped tests excluded from denominator. "
            r"NLI confidence: entailment score from NLI model over generated user stories; "
            r"$\dagger$ P3E2 excluded from NLI aggregation ($N=11$)."
        ),
        label="tab:rq2_quality",
        footnote=(
            r"Deployment success $=$ \texttt{mark\_project\_complete} in log "
            r"OR Docker containers healthy (checked in both root and \texttt{dev/} subfolder). "
            r"All 12 runs succeeded."
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Table 4 — RQ2 Token & Latency (top-5 phases, cross-project mean)
# ══════════════════════════════════════════════════════════════════════════════

def _table_rq2_cost() -> str:
    tok = json.loads((SUMMARY_DIR / "rq2_tokens_per_task.json").read_text())
    lat = json.loads((SUMMARY_DIR / "rq2_latency_per_task.json").read_text())

    # Build cross-project mean ± std for tokens and latency per phase
    tok_by_phase: dict[str, list[float]] = {}
    lat_by_phase: dict[str, list[float]] = {}

    for proj in tok["projects"]:
        for pe in proj["phases"]:
            ph = pe["phase"]
            # per_task_tokens is the combined total (input + output)
            total_m = pe["per_task_tokens"]["mean"]
            tok_by_phase.setdefault(ph, []).append(total_m)

    for proj in lat["projects"]:
        for pe in proj["phases"]:
            ph = pe["phase"]
            dur_m = pe["per_task_dur_s"]["mean"]
            lat_by_phase.setdefault(ph, []).append(dur_m)

    # Aggregate
    phase_tok = {
        ph: (sum(v) / len(v), (sum((x - sum(v)/len(v))**2 for x in v)/(len(v)-1))**0.5 if len(v)>1 else 0)
        for ph, v in tok_by_phase.items()
    }
    phase_lat = {
        ph: (sum(v) / len(v), (sum((x - sum(v)/len(v))**2 for x in v)/(len(v)-1))**0.5 if len(v)>1 else 0)
        for ph, v in lat_by_phase.items()
    }

    # Top-8 phases by token consumption
    from paper.log_analysis.phases import PHASE_ORDER
    phases_ordered = [ph.value for ph in PHASE_ORDER]
    ranked = sorted(
        [ph for ph in phases_ordered if ph in phase_tok],
        key=lambda ph: phase_tok[ph][0],
        reverse=True,
    )[:8]

    def _ktok(v: float) -> str:
        return f"{v/1000:.1f}K" if v >= 1000 else f"{v:.0f}"

    lines = [
        r"\begin{tabular}{@{}lrrrr@{}}",
        r"\toprule",
        r"\textbf{Phase} & "
        r"\textbf{Tokens/task (mean)} & "
        r"\textbf{Tokens/task (std)} & "
        r"\textbf{Latency/task (mean, s)} & "
        r"\textbf{Latency/task (std, s)} \\",
        r"\midrule",
    ]

    tok_means = [phase_tok[ph][0] for ph in ranked]
    for i, ph in enumerate(ranked):
        tm, ts = phase_tok[ph]
        lm, ls = phase_lat.get(ph, (0.0, 0.0))
        # Colour the highest-token phase
        is_top = (i == 0)
        row_color = r"\rowcolor[HTML]{FEF7E0} " if is_top else ""
        lines.append(
            rf"{row_color}{ph.replace('_', r'\_')} & "
            rf"{_ktok(tm)} & "
            rf"{_ktok(ts)} & "
            rf"{_f(lm)} & "
            rf"{_f(ls)} \\"
        )

    lines.append(r"\midrule")
    total_tok = sum(phase_tok[ph][0] for ph in ranked)
    impl_tok  = phase_tok.get("IMPLEMENTATION", (0, 0))[0]
    impl_pct  = 100 * impl_tok / total_tok if total_tok else 0
    lines.append(
        rf"\multicolumn{{5}}{{l}}{{\footnotesize "
        rf"\textsc{{Implementation}} consumes "
        rf"${impl_pct:.0f}\%$ of cross-phase token budget (top-8 phases shown).}} \\"
    )
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")

    body = "\n".join(lines)
    return _wrap(
        body,
        caption=(
            r"RQ2: Mean Token Consumption and Latency per Task per SDLC Phase "
            r"(cross-project mean $\pm$ std, $n = 4 \times 3 = 12$ runs, "
            r"top-8 phases by token budget). "
            r"Per-task normalization removes the task-count confound across projects. "
            r"Phase totals exceed the wall-clock total because nested agent steps are "
            r"attributed to both the sub-phase and the parent ORCHESTRATION phase."
        ),
        label="tab:rq2_cost",
        footnote=(
            r"Tokens include both agent-reasoning tokens "
            r"(from \texttt{[Step N: Input/Output tokens: ...]} log lines) "
            r"and tool-LLM tokens "
            r"(from \texttt{OpenRouter/Ollama token usage} lines)."
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Table 5 — RQ2 Code Hallucination
# ══════════════════════════════════════════════════════════════════════════════

def _table_rq2_hallucination() -> str:
    hall_d = json.loads((SUMMARY_DIR / "rq2_hallucination.json").read_text())["projects"]
    hall_d = sorted(hall_d, key=lambda p: p["project_id"])
    # Spec extrapolation rate comes from rq2_nli_confidence.json (correct P3 n=2 value,
    # not from rq2_hallucination.json which includes P3E2 as 0.0 — a missing-data artifact).
    nli_d  = {p["project_id"]: p for p in
               json.loads((SUMMARY_DIR / "rq2_nli_confidence.json").read_text())["projects"]}

    lines = [
        r"\begin{tabular}{@{}lrrrr@{}}",
        r"\toprule",
        r"\textbf{Project} & "
        r"\textbf{Orphan routes} & "
        r"\textbf{Unused imports} & "
        r"\textbf{Schema mismatches} & "
        r"\textbf{Spec. extrapol. rate (\%)} \\",
        r"\midrule",
    ]

    extrap_vals = []
    for proj in hall_d:
        pid  = proj["project_id"]
        name = PROJ_NAMES[pid]
        rc   = ROW_COLORS[pid]

        or_m  = proj["orphan_routes"]["mean"]
        or_s  = proj["orphan_routes"]["std"]
        ui_m  = proj["unused_imports"]["mean"]
        ui_s  = proj["unused_imports"]["std"]
        sm_m  = proj.get("schema_mismatches", {}).get("mean", 0.0)
        sm_s  = proj.get("schema_mismatches", {}).get("std",  0.0)

        # Use rq2_nli_confidence.json for correct extrapolation rate (proper n per project)
        nli_proj = nli_d.get(pid, {})
        extrap   = nli_proj.get("spec_extrapolation_rate", {})
        se_m = extrap.get("mean", 0.0) * 100
        se_s = extrap.get("std",  0.0) * 100
        n_nli = nli_proj.get("n_essays_with_data", nli_proj.get("n_essays", 3))
        note  = rf"$^\dagger$" if n_nli < 3 else ""
        extrap_vals.append(se_m)

        lines.append(
            rf"{rc} {name} & "
            rf"${_f(or_m)} \pm {_f(or_s)}$ & "
            rf"${_f(ui_m)} \pm {_f(ui_s)}$ & "
            rf"${_f(sm_m)} \pm {_f(sm_s)}$ & "
            rf"${_f(se_m)}\% \pm {_f(se_s)}\%${note} \\"
        )

    lines.append(r"\midrule")
    avg_extrap = sum(extrap_vals) / len(extrap_vals) if extrap_vals else 0
    lines.append(
        rf"\textit{{Overall mean}} & & & & "
        rf"$\mathbf{{{_f(avg_extrap)}\%}}$ \\"
    )
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")

    body = "\n".join(lines)
    return _wrap(
        body,
        caption=(
            r"RQ2: Code Structural Issues and Specification Extrapolation per Project "
            r"(mean $\pm$ std, $n=3$ seeds). "
            r"Orphan routes: FastAPI route decorators with no matching handler function. "
            r"Unused imports: imports absent from all \texttt{ast.Name}/\texttt{ast.Attribute} uses. "
            r"Schema mismatches: backend DTO fields absent from matching frontend TypeScript types "
            r"(conservative static analysis; manual review deferred to future work). "
            r"Spec.\ extrapolation rate $= 1 - \text{supported}/\text{total NLI claims}$ — "
            r"measures how much the agent generates \emph{beyond} the source specification "
            r"(implied requirements, defaults, error copy); this is \emph{not} hallucination. "
            r"$\dagger$ P3: $n=2$ seeds (P3E2 NLI data missing)."
        ),
        label="tab:rq2_hallucination",
    )


# ══════════════════════════════════════════════════════════════════════════════
# Table: Benchmark Dataset
# ══════════════════════════════════════════════════════════════════════════════

def _table_dataset() -> str:
    # Static data derived from experiments/ folder — constant across seeds.
    # LOC measured from essay 1 (reference seed); varies ≤5% across seeds.
    projects = [
        {
            "id":      "P1",
            "system":  "Hospital Triage Queue",
            "domain":  "Healthcare",
            "descr":   "Emergency-room intake that prioritises patients by clinical urgency.",
            "stories": 6,
            "tasks":   6,
            "alloy":   6,
            "be_loc":  2228,
            "fe_loc":  590,
            "tests":   13,
        },
        {
            "id":      "P2",
            "system":  "Blood Bank Inventory",
            "domain":  "Healthcare",
            "descr":   "Blood-unit stock manager with compatibility rules and expiry tracking.",
            "stories": 7,
            "tasks":   7,
            "alloy":   7,
            "be_loc":  2842,
            "fe_loc":  798,
            "tests":   18,
        },
        {
            "id":      "P3",
            "system":  "Airport Runway Scheduler",
            "domain":  "Transport",
            "descr":   "Slot allocator for two runways with emergency-priority preemption.",
            "stories": 7,
            "tasks":   7,
            "alloy":   7,
            "be_loc":  3295,
            "fe_loc":  1151,
            "tests":   17,
        },
        {
            "id":      "P4",
            "system":  "ATM Withdrawal Safety",
            "domain":  "Finance",
            "descr":   "Transactional ATM backend with fraud detection and full rollback.",
            "stories": 8,
            "tasks":   8,
            "alloy":   8,
            "be_loc":  3908,
            "fe_loc":  1290,
            "tests":   30,
        },
        {
            "id":      "P5",
            "system":  "Competency Assessment Platform",
            "domain":  "Education",
            "descr":   "Gamified exam platform where instructors build competency-tagged assessments.",
            "stories": 12,
            "tasks":   12,
            "alloy":   12,
            "be_loc":  9953,
            "fe_loc":  3142,
            "tests":   173,
        },
        {
            "id":      "P6",
            "system":  "Community Social Network",
            "domain":  "Social",
            "descr":   "Social media platform with profiles, posts, communities, and moderation.",
            "stories": 25,
            "tasks":   25,
            "alloy":   25,
            "be_loc":  7618,
            "fe_loc":  1866,
            "tests":   81,
        },
    ]

    rows = []
    for pr in projects:
        rows.append(
            rf"  {pr['id']} & {pr['system']} & {pr['domain']} "
            rf"& \multicolumn{{1}}{{p{{4.5cm}}}}{{\small {pr['descr']}}} "
            rf"& {pr['tasks']} & {pr['alloy']} "
            rf"& {pr['be_loc']:,} & {pr['fe_loc']:,} & {pr['tests']} \\"
        )

    body = (
        r"\begin{tabularx}{\linewidth}{@{} l l l X r r r r r @{}}" + "\n"
        r"\toprule" + "\n"
        r"\rowcolor[HTML]{2D3748}"
        r"\textcolor{white}{\textbf{ID}} &"
        r"\textcolor{white}{\textbf{System}} &"
        r"\textcolor{white}{\textbf{Domain}} &"
        r"\textcolor{white}{\textbf{Description}} &"
        r"\textcolor{white}{\textbf{Tasks}} &"
        r"\textcolor{white}{\textbf{Alloy}} &"
        r"\textcolor{white}{\textbf{BE LOC}} &"
        r"\textcolor{white}{\textbf{FE LOC}} &"
        r"\textcolor{white}{\textbf{Tests}} \\" + "\n"
        r"\midrule" + "\n"
        + "\n".join(rows) + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabularx}"
    )

    return _wrap(
        body,
        caption=(
            r"Benchmark dataset: 4 software systems used in the evaluation. "
            r"Each project was executed with 3 independent seeds. "
            r"Tasks = user stories decomposed from the specification; "
            r"Alloy = number of formal Alloy specifications generated; "
            r"BE LOC / FE LOC = backend Python / frontend TypeScript lines of code "
            r"(measured from seed~1, varies $\leq$5\% across seeds); "
            r"Tests = automated test files generated."
        ),
        label="tab:dataset",
        footnote=(
            r"Projects span three safety-relevant domains (healthcare, transport, finance) "
            r"and range from 6 to 8 user stories, providing a diverse complexity profile."
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Table: Experimental Configuration (LLM + NLI)
# ══════════════════════════════════════════════════════════════════════════════

def _table_llm_config() -> str:
    llm_rows = [
        # (role, model_id, provider, temp, max_tok, deployment, note)
        ("All agents (default)",
         r"\texttt{deepseek/deepseek-v4-flash}",
         "OpenRouter", "0.70", r"8\,192", "Cloud API",
         "Orchestration, planning, implementation, frontend, DevOps"),
        ("Formal spec --- generation",
         r"\texttt{deepseek/deepseek-v4-flash}",
         "OpenRouter", "0.10", r"8\,192", "Cloud API",
         "Low temperature for deterministic Alloy output"),
        ("Formal spec --- fix pass",
         r"\texttt{deepseek/deepseek-v4-flash}",
         "OpenRouter", "0.10", r"16\,384", "Cloud API",
         "Extended budget for iterative Alloy repair"),
        ("UML generation",
         r"\texttt{deepseek/deepseek-v4-flash}",
         "OpenRouter", r"0.10--0.15", r"8\,192", "Cloud API",
         "Near-deterministic structural diagram output"),
        ("Local code tasks",
         r"\texttt{qwen2.5-coder:7b}",
         "Ollama", "0.70", r"8\,192$^{*}$", "Self-hosted",
         r"Context window 8\,192; no cloud egress"),
    ]

    llm_section = (
        r"\multicolumn{6}{@{}l}{\textit{\textbf{Generative LLM Configuration}}} \\"
        + r"\midrule" + "\n"
    )
    llm_section += (
        r"\textbf{Role} & \textbf{Model ID} & \textbf{Provider} "
        r"& \textbf{Temp.} & \textbf{Max tokens} & \textbf{Deployment} \\" + "\n"
        r"\midrule" + "\n"
    )
    for role, mid, prov, temp, mt, deploy, note in llm_rows:
        llm_section += (
            rf"  {role} & {mid} & {prov} & {temp} & {mt} & {deploy} "
            rf"\\ % {note}" + "\n"
        )

    nli_params = [
        ("Model identifier",      r"\texttt{khalidalt/DeBERTa-v3-large-mnli}"),
        ("Architecture",          r"DeBERTa-v3-large fine-tuned on MultiNLI~\cite{williams2018multinli}"),
        ("Hidden dimension",      r"1{,}024"),
        ("Transformer layers",    r"24"),
        ("Attention heads",       r"16"),
        ("Max sequence length",   r"512 tokens (premise--hypothesis pair)"),
        ("Vocabulary size",       r"128{,}100"),
        ("Inference classes",     r"\textit{entailment} / \textit{neutral} / \textit{contradiction}"),
        ("Entailment threshold",  r"0.60 (softmax probability on entailment class)"),
        ("Input truncation",      r"Enabled (premise--hypothesis pair truncated jointly)"),
        ("Inference device",      r"CUDA if available, else CPU (float32)"),
    ]

    nli_section = (
        r"\midrule" + "\n"
        r"\multicolumn{6}{@{}l}{\textit{\textbf{NLI Classification Model Configuration}}} \\"
        + r"\midrule" + "\n"
        r"\multicolumn{2}{@{}l}{\textbf{Parameter}} & \multicolumn{4}{l}{\textbf{Value}} \\" + "\n"
        r"\midrule" + "\n"
    )
    for param, val in nli_params:
        nli_section += rf"  \multicolumn{{2}}{{@{{}}l}}{{{param}}} & \multicolumn{{4}}{{l}}{{{val}}} \\" + "\n"

    agent_params = [
        ("Agent framework",              r"smolagents \texttt{CodeAgent}~\cite{smolagents2025}",      "—"),
        ("Scrum Master (orchestrator)",  r"\texttt{planning\_interval}=6, \texttt{max\_steps}=20",  "Plans every 6 steps; re-plans on escalation"),
        ("Developer / Frontend agents",  r"\texttt{max\_steps}=200",                                 "Long horizon for iterative code generation"),
        ("DevOps agent",                 r"\texttt{max\_steps}=50",                                  ""),
        ("All other agents",             r"\texttt{max\_steps}=5",                                   "Formal spec, UML, requirements, user stories"),
        ("Max execution time",           r"3{,}600 seconds per run",                                 "Hard timeout per full-pipeline execution"),
    ]

    agent_section = (
        r"\midrule" + "\n"
        r"\multicolumn{6}{@{}l}{\textit{\textbf{Agent Framework Configuration}}} \\"
        + r"\midrule" + "\n"
        r"\multicolumn{2}{@{}l}{\textbf{Component}} & \multicolumn{3}{l}{\textbf{Setting}} & \textbf{Note} \\" + "\n"
        r"\midrule" + "\n"
    )
    for comp, setting, note in agent_params:
        agent_section += (
            rf"  \multicolumn{{2}}{{@{{}}l}}{{{comp}}} & \multicolumn{{3}}{{l}}{{{setting}}} & {note} \\" + "\n"
        )

    body = (
        r"\begin{tabularx}{\linewidth}{@{} l l l l l X @{}}" + "\n"
        r"\toprule" + "\n"
        + llm_section
        + nli_section
        + agent_section
        + r"\bottomrule" + "\n"
        r"\end{tabularx}"
    )

    return _wrap(
        body,
        caption=(
            r"Experimental configuration: generative LLM hyperparameters, NLI model "
            r"architecture, and agent-framework settings used in all 12 pipeline runs. "
            r"Temperature is reduced to $\leq 0.15$ for phases that require "
            r"deterministic structured output (formal specifications, UML diagrams). "
            r"The NLI model runs locally; no user-story content is sent to external services."
        ),
        label="tab:config",
        footnote=(
            r"$^{*}$Qwen2.5-Coder is used via Ollama with a fixed context window of "
            r"8{,}192 tokens; \texttt{max\_tokens} is governed by the context budget. "
            r"\texttt{DeBERTa-v3-large-mnli} is loaded from HuggingFace Hub at first use "
            r"and cached locally."
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Write all tables
# ══════════════════════════════════════════════════════════════════════════════

TABLE_SPECS = [
    ("dataset.tex",            _table_dataset),
    ("config.tex",             _table_llm_config),
    ("rq1a_autonomy.tex",      _table_rq1a),
    ("rq1b_coordination.tex",  _table_rq1b),
    ("rq2_quality.tex",        _table_rq2_quality),
    ("rq2_cost.tex",           _table_rq2_cost),
    ("rq2_hallucination.tex",  _table_rq2_hallucination),
]

PREAMBLE_FILE = "latex_preamble.tex"


def _write_preamble() -> None:
    p = TABLE_DIR / PREAMBLE_FILE
    p.write_text(
        "% Required packages for AgentsSociety ICSE tables\n"
        + ICSE_HEADER
        + r"""
% Usage: \input{tables/latex_preamble.tex} in your paper preamble.
% Then \input{tables/<table>.tex} where you want the table.
"""
    )
    print(f"  Saved → {p}")


def run() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    _write_preamble()

    for filename, gen_fn in TABLE_SPECS:
        tex = gen_fn()
        p   = TABLE_DIR / filename
        p.write_text(tex)
        print(f"  Saved → {p}")


if __name__ == "__main__":
    run()
