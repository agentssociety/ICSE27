"""
Execution Trace Gantt Charts — 4 Projects × 3 Seeds
======================================================

Adapted from paper/orchestration_analysis/orchestration_analysis.py for
the new 4 × 3 experiment structure. All data is re-parsed from raw logs;
no pre-computed JSON is required beyond what parse_tokens produces.

Figures generated:
  fig_gantt_traces.png / .pdf
      4-panel grid (one panel per project).
      Each panel overlays 3 seed traces as horizontal phase-sequence lines
      (Essay 1 = blue/solid, Essay 2 = amber/dashed, Essay 3 = green/dotted).
      Background shading marks phases with ≥1 FAIL_ESCALATED incident.
      Decision-quality strips below each trace.
      Delegation events marked with ▼, re-delegations with ◆.

Usage (from repo root):
  python -m research_results.scripts.plot_gantt
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from paper.log_analysis.token_parser import parse_tokens
from paper.log_analysis.phases import Phase, PHASE_ORDER
from research_results.scripts.paths import ALL_RUNS, RUNS_BY_PROJECT, RESULTS_ROOT
from research_results.scripts.extract_errors import _analyse_log

FIG_DIR = RESULTS_ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── ICSE rc defaults ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "sans-serif",
    "font.sans-serif":   ["Arial", "Helvetica Neue", "Helvetica", "DejaVu Sans"],
    "font.size":         8.5,
    "axes.titlesize":    9.5,
    "axes.labelsize":    8.5,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
    "legend.fontsize":   8,
    "legend.framealpha": 0.92,
    "legend.edgecolor":  "#CCCCCC",
    "figure.dpi":        150,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
})

# ── Pastel palette ────────────────────────────────────────────────────────────
C_BG    = "#FAFAFA"
C_PANEL = "#F4F7FB"
C_GRID  = "#DDDDDD"

# Per-project accent colors (used only for panel labels and radar chart)
PROJ_BASE  = ["#3A78C9", "#3A9A5C", "#D4700A", "#9B3A8A"]
PROJ_NAMES = ["Hospital Triage", "Blood Bank", "Airport Runway", "ATM"]
PROJ_PASTEL = ["#A8C8E8", "#A8D8A8", "#F5D8A0", "#E8B8D0"]
PROJ_NAMES_SHORT = ["Proj.1 / Triage", "Proj.2 / Blood",
                    "Proj.3 / Runway", "Proj.4 / ATM"]

# Per-seed colors — consistent across all project panels (IBM colorblind-safe)
# Essay 1 = blue, Essay 2 = amber, Essay 3 = green
SEED_COLORS  = ["#0072B2", "#E69F00", "#009E73"]
SEED_LS      = ["-",        "--",      ":"]        # solid / dashed / dotted
SEED_LW      = [2.2,        1.8,       1.8]
SEED_ALPHA   = [0.90,       0.85,      0.85]
SEED_LABELS  = ["Essay 1",  "Essay 2", "Essay 3"]

# Quality-strip colours
C_BT    = "#C62828"   # backtrack
C_ESC   = "#EF9A9A"   # escalation zone
C_ORCH  = "#BDBDBD"   # orchestration overhead
C_VERIF = "#B3E5FC"   # verification gate
C_OK    = "#A5D6A7"   # clean forward step

# Phases hidden from the main trace (coordination/meta steps, not SDLC milestones)
HIDDEN_PHASES = {Phase.ORCHESTRATION, Phase.VERIFICATION}

# Canonical SDLC order (excluding ORCHESTRATION for y-axis)
CANONICAL = [p for p in PHASE_ORDER if p != Phase.ORCHESTRATION]
RANK       = {p: i for i, p in enumerate(PHASE_ORDER)}
N          = len(CANONICAL)

SHORT = {
    Phase.INIT:           "Init",
    Phase.USER_STORIES:   "User Stories",
    Phase.PLANNING:       "Planning",
    Phase.REQUIREMENTS:   "Req.",
    Phase.FORMAL_SPEC:    "Formal Spec",
    Phase.DESIGN_UML:     "System Design",
    Phase.ARCHITECTURE:   "Architecture Design",
    Phase.IMPLEMENTATION: "Implementation",
    Phase.TESTING:        "Testing",
    Phase.FRONTEND:       "Frontend",
    Phase.DEVOPS:         "DevOps",
    Phase.VERIFICATION:   "Verification",
    Phase.ORCHESTRATION:  "Orchestration",
}
SUB_AGENTS = {
    "developer_agent", "frontend_agent", "devops_agent",
    "project_manager_agent", "package_design_agent",
    "user_story_backlog_agent", "formal_specification_agent",
    "uml_diagram_generation_agent", "semi_formal_requirement_agent",
}
SM_AGENTS = {"__root__", "scrum_master_agent"}


# ── Per-run data extraction ───────────────────────────────────────────────────

def _extract_run_trace(run_id) -> dict:
    """Return everything needed to draw one Gantt trace."""
    tl     = parse_tokens(run_id.log_path)
    blocks = tl.blocks
    pa     = _analyse_log(run_id.log_path, run_id.project)

    n      = len(blocks)
    phases = [eb.block.phase for eb in blocks]
    ranks  = [RANK[ph] for ph in phases]

    # Backtracks
    bt_idx: set[int] = set()
    last_r = -1
    for i, eb in enumerate(blocks):
        ph = eb.block.phase
        if ph == Phase.ORCHESTRATION:
            continue
        r = RANK[ph]
        if last_r >= 0 and r < last_r:
            bt_idx.add(i)
        last_r = r

    # Escalation zone: phases that contained ≥1 unresolved (FAIL_ESCALATED) incident.
    # This is the same definition as the original paper (orchestration_analysis.py line 102-104):
    #   esc_phases = set of phases with any FAIL_ESCALATED outcome
    #   A block is "in the escalation zone" iff its phase is in esc_phases.
    # We do NOT use a temporal clearing rule (FAIL_FIXED from an unrelated phase should
    # not "clear" an architecture escalation — they are independent error streams).
    esc_phases: set[Phase] = {
        inc.phase for inc in pa.incidents if inc.outcome == "FAIL_ESCALATED"
    }

    # Delegation events: list of (block_index, phase_value, sub_agent)
    delegations: list[tuple[int, str, str]] = []
    for i, eb in enumerate(blocks):
        if eb.agent_session in SM_AGENTS:
            for call in eb.block.calls:
                if call in SUB_AGENTS:
                    delegations.append((i, eb.block.phase.value, call))

    deleg_counter = Counter((ph, ag) for (_, ph, ag) in delegations)
    redeleg_idx: set[int] = set()
    seen: Counter = Counter()
    for (i, ph, ag) in delegations:
        seen[(ph, ag)] += 1
        if seen[(ph, ag)] > 1:
            redeleg_idx.add(i)

    total_err = len(pa.incidents)
    fixed_n   = sum(1 for inc in pa.incidents if inc.outcome == "FAIL_FIXED")
    esc_n     = sum(1 for inc in pa.incidents if inc.outcome == "FAIL_ESCALATED")
    sr        = round(100 * fixed_n / total_err, 1) if total_err else 100.0
    linearity = round(100 * (n - len(bt_idx)) / n, 1) if n else 100.0
    deleg_n   = len(delegations)
    redeleg_n = len(set(redeleg_idx))
    ds_val    = round(100 * (deleg_n - redeleg_n) / deleg_n, 1) if deleg_n else 100.0

    return {
        "run_id":       str(run_id),
        "project":      run_id.project,
        "essay":        run_id.essay,
        "n_steps":      n,
        "phases":       phases,
        "ranks":        ranks,
        "bt_idx":       bt_idx,
        "esc_phases":   esc_phases,   # phases with ≥1 FAIL_ESCALATED
        "delegations":  delegations,
        "redeleg_idx":  redeleg_idx,
        "sr":           sr,
        "linearity":    linearity,
        "ds_val":       ds_val,
        "deleg_n":      deleg_n,
        "redeleg_n":    redeleg_n,
        "total_err":    total_err,
        "esc_n":        esc_n,
        "fixed_n":      fixed_n,
    }


# ── Quality strip helper ──────────────────────────────────────────────────────

def _strip_colors(trace: dict) -> list[str]:
    """
    Per-block quality color for the decision strip.
    Priority: backtrack > orchestration overhead > verification gate > escalation zone > clean.
    Escalation zone = block's phase is in esc_phases (phases with ≥1 unresolved failure).
    Matches the original paper definition (orchestration_analysis.py line 283).
    """
    esc_phases = trace["esc_phases"]
    colors = []
    for i, ph in enumerate(trace["phases"]):
        if i in trace["bt_idx"]:
            colors.append(C_BT)
        elif ph == Phase.ORCHESTRATION:
            colors.append(C_ORCH)
        elif ph == Phase.VERIFICATION:
            colors.append(C_VERIF)
        elif ph in esc_phases:
            colors.append(C_ESC)
        else:
            colors.append(C_OK)
    return colors


# ══════════════════════════════════════════════════════════════════════════════
# Fig A — Execution Trace Gantt (single run: Project 1, Essay 3)
# ══════════════════════════════════════════════════════════════════════════════

def plot_gantt_single(trace: dict, show: bool = False, out_name: str = "fig_gantt_traces") -> None:
    """
    Single-run Gantt: main phase-sequence panel + decision-quality strip below.
    Authored at full-page print width (10") for ICSE readability.
    """
    # SDLC phases shown on y-axis (orchestration and verification hidden)
    DISP_ORDER = [
        Phase.INIT, Phase.USER_STORIES, Phase.PLANNING,
        Phase.REQUIREMENTS, Phase.FORMAL_SPEC, Phase.DESIGN_UML, Phase.ARCHITECTURE,
        Phase.IMPLEMENTATION, Phase.TESTING, Phase.FRONTEND, Phase.DEVOPS,
    ]
    DISP_RANK = {p: i for i, p in enumerate(DISP_ORDER)}
    ND    = len(DISP_ORDER)
    N_TOP = ND - 1  # y-index of Verification

    n_full  = trace["n_steps"]
    color   = SEED_COLORS[trace["essay"] - 1]

    # Truncate display at last DevOps step (trailing steps are parsing artefacts)
    last_dv  = max(
        (i for i, ph in enumerate(trace["phases"]) if ph == Phase.DEVOPS),
        default=n_full - 1,
    )
    n_plot   = last_dv + 1
    phases_p = trace["phases"][:n_plot]

    # Hidden phases (orchestration, verification) excluded from trace
    sdlc_xs = [i for i, ph in enumerate(phases_p) if ph not in HIDDEN_PHASES]
    sdlc_ys = [DISP_RANK[ph] for ph in phases_p if ph not in HIDDEN_PHASES]

    fig = plt.figure(figsize=(10.0, 5.5))
    fig.patch.set_facecolor(C_BG)
    gs = GridSpec(2, 1, figure=fig,
                  height_ratios=[1.0, 0.12],
                  hspace=0.10,
                  left=0.14, right=0.97, top=0.78, bottom=0.09)
    ax_m = fig.add_subplot(gs[0, 0])
    ax_s = fig.add_subplot(gs[1, 0])
    ax_m.set_facecolor(C_PANEL)
    ax_s.set_facecolor(C_PANEL)

    # Ideal diagonal reference (Init → DevOps)
    ax_m.plot([0, n_plot - 1], [0, N_TOP], "--", color="#CCCCCC", lw=0.8, zorder=1)

    # Escalation phase shading
    for i, ph in enumerate(phases_p):
        if ph in trace["esc_phases"]:
            ax_m.axvspan(i - 0.5, i + 0.5, alpha=0.09, color="#B71C1C", zorder=0)

    # Main trace line (SDLC steps only, connected at original x-positions)
    ax_m.plot(sdlc_xs, sdlc_ys, "-", color=color, lw=2.0, alpha=0.80, zorder=2)

    # Phase dots (skip hidden phases)
    for i, ph in enumerate(phases_p):
        if ph in HIDDEN_PHASES:
            continue
        y = DISP_RANK[ph]
        if i in trace["bt_idx"]:
            ax_m.scatter(i, y, color="#C62828", s=22, alpha=0.95, zorder=5, linewidths=0)
        else:
            ax_m.scatter(i, y, color=color, s=12, alpha=0.85, zorder=4, linewidths=0)

    # Delegation markers (above Verification row)
    for (bidx, _, __) in trace["delegations"]:
        if bidx >= n_plot:
            continue
        is_redel = bidx in trace["redeleg_idx"]
        ax_m.scatter(bidx, N_TOP + 1.2,
                     marker="D" if is_redel else "v",
                     s=60 if is_redel else 75,
                     color="#E91E63" if is_redel else "#6A1B9A",
                     zorder=8, clip_on=False)

    # Axes
    ax_m.set_yticks(list(range(ND)))
    ax_m.set_yticklabels([SHORT[p] for p in DISP_ORDER], fontsize=10)
    ax_m.set_ylim(-0.7, N_TOP + 1.8)
    ax_m.set_xlim(-2, n_plot + 6)
    ax_m.grid(axis="x", linestyle=":", alpha=0.25, color=C_GRID)
    ax_m.tick_params(left=False, bottom=False, labelbottom=False)
    for sp in ("top", "right"):
        ax_m.spines[sp].set_visible(False)
    ax_m.spines["left"].set_linewidth(0.5)
    ax_m.spines["bottom"].set_linewidth(0.5)

    # Decision-quality strip (truncated to n_plot)
    strip_clr = _strip_colors(trace)[:n_plot]
    for j, fc in enumerate(strip_clr):
        ax_s.broken_barh([(j, 1)], (0, 1), facecolors=fc, edgecolors="none")
    ax_s.set_xlim(-2, n_plot + 6)
    ax_s.set_ylim(0, 1)
    ax_s.set_yticks([0.5])
    ax_s.set_yticklabels(["Quality"], fontsize=9.5)
    ax_s.set_xlabel("Pipeline step (block index)", fontsize=10.5)
    ax_s.tick_params(left=False, labelsize=9.5)
    ax_s.spines[["top", "right", "left"]].set_visible(False)
    ax_s.spines["bottom"].set_linewidth(0.5)

    # Legend
    handles = [
        Line2D([0], [0], color=color, lw=2.0, marker="o", markersize=5,
               markerfacecolor=color, label=f"Phase sequence (Essay {trace['essay']})"),
        mpatches.Patch(color="#C62828",              label="Back-track"),
        mpatches.Patch(color="#B71C1C", alpha=0.18,  label="Escalation zone"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor="#E91E63",
               markersize=7,                         label="Re-delegation"),
        mpatches.Patch(color=C_BT,    label="Strip: back-track"),
        mpatches.Patch(color=C_ORCH,  label="Strip: orchestration"),
        mpatches.Patch(color=C_ESC,   label="Strip: escalation"),
        mpatches.Patch(color=C_OK,    label="Strip: forward step"),
    ]
    proj  = trace["project"]
    essay = trace["essay"]
    fig.suptitle(
        f"Pipeline execution trace — Project {proj} ({PROJ_NAMES[proj - 1]}), Essay {essay}"
        f"\nSteps: {n_full}  ·  SR: {trace['sr']}%  ·  PL: {trace['linearity']}%  ·  DS: {trace['ds_val']}%",
        fontsize=11, fontweight="bold", y=0.99, color="#222222",
    )
    fig.legend(handles=handles, loc="upper center", ncol=5, fontsize=9,
               bbox_to_anchor=(0.57, 0.89),
               framealpha=0.96, edgecolor="#CCCCCC", handlelength=1.2)

    for ext in ("png", "pdf"):
        p = FIG_DIR / f"{out_name}.{ext}"
        fig.savefig(p, dpi=300 if ext == "png" else None, bbox_inches="tight", facecolor=C_BG)
        print(f"  Saved → {p}")
    if show:
        plt.show()
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# Fig B — 4 × 3 Gantt Grid (all 12 runs)
# ══════════════════════════════════════════════════════════════════════════════

def plot_gantt_grid(traces_by_project: dict, show: bool = False) -> None:
    """4 rows × 3 columns grid — one panel per run, hidden phases excluded."""
    DISP_ORDER = [
        Phase.INIT, Phase.USER_STORIES, Phase.PLANNING,
        Phase.REQUIREMENTS, Phase.FORMAL_SPEC, Phase.DESIGN_UML, Phase.ARCHITECTURE,
        Phase.IMPLEMENTATION, Phase.TESTING, Phase.FRONTEND, Phase.DEVOPS,
    ]
    DISP_RANK = {p: i for i, p in enumerate(DISP_ORDER)}
    ND    = len(DISP_ORDER)
    N_TOP = ND - 1

    fig, axes = plt.subplots(
        4, 3, figsize=(10.0, 13.0),
        gridspec_kw=dict(hspace=0.45, wspace=0.06,
                         left=0.13, right=0.98, top=0.93, bottom=0.05),
    )
    fig.patch.set_facecolor(C_BG)

    for pi, proj_id in enumerate([1, 2, 3, 4]):
        proj_traces = sorted(traces_by_project.get(proj_id, []), key=lambda t: t["essay"])
        for ei, trace in enumerate(proj_traces):
            ax = axes[pi][ei]
            ax.set_facecolor(C_PANEL)
            color = SEED_COLORS[ei]

            n_full   = trace["n_steps"]
            last_dv  = max(
                (i for i, ph in enumerate(trace["phases"]) if ph == Phase.DEVOPS),
                default=n_full - 1,
            )
            n_plot   = last_dv + 1
            phases_p = trace["phases"][:n_plot]

            sdlc_xs = [i for i, ph in enumerate(phases_p) if ph not in HIDDEN_PHASES]
            sdlc_ys = [DISP_RANK[ph] for ph in phases_p if ph not in HIDDEN_PHASES]

            # Diagonal reference
            ax.plot([0, n_plot - 1], [0, N_TOP], "--", color="#CCCCCC", lw=0.6, zorder=1)

            # Escalation shading
            for i, ph in enumerate(phases_p):
                if ph in trace["esc_phases"]:
                    ax.axvspan(i - 0.5, i + 0.5, alpha=0.10, color="#B71C1C", zorder=0)

            # Trace line
            ax.plot(sdlc_xs, sdlc_ys, "-", color=color, lw=1.2, alpha=0.85, zorder=2)

            # Dots (skip hidden phases)
            for i, ph in enumerate(phases_p):
                if ph in HIDDEN_PHASES:
                    continue
                y = DISP_RANK[ph]
                if i in trace["bt_idx"]:
                    ax.scatter(i, y, color="#C62828", s=8, alpha=0.95, zorder=5, linewidths=0)
                else:
                    ax.scatter(i, y, color=color, s=3, alpha=0.85, zorder=4, linewidths=0)

            # Delegation markers
            for (bidx, _, __) in trace["delegations"]:
                if bidx >= n_plot:
                    continue
                is_redel = bidx in trace["redeleg_idx"]
                ax.scatter(bidx, N_TOP + 0.8,
                           marker="D" if is_redel else "v",
                           s=18 if is_redel else 22,
                           color="#E91E63" if is_redel else "#6A1B9A",
                           zorder=8, clip_on=False)

            # Axes
            ax.set_ylim(-0.7, N_TOP + 1.5)
            ax.set_xlim(-2, n_plot + 3)
            ax.grid(axis="x", linestyle=":", alpha=0.25, color=C_GRID)
            ax.tick_params(left=False, bottom=False,
                           labelbottom=(pi == 3), labelleft=(ei == 0))
            if ei == 0:
                ax.set_yticks(list(range(ND)))
                ax.set_yticklabels([SHORT[p] for p in DISP_ORDER], fontsize=6.5)
            else:
                ax.set_yticks([])
            if pi == 3:
                ax.tick_params(axis="x", labelsize=7)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            ax.spines["left"].set_linewidth(0.4)
            ax.spines["bottom"].set_linewidth(0.4)

            # Panel title
            name_short = PROJ_NAMES[pi].split()[0]   # first word only
            title_line1 = (f"P{proj_id} ({name_short}) · E{ei + 1}"
                           if ei == 0 else f"E{ei + 1}")
            ax.set_title(
                f"{title_line1}  ·  SR={trace['sr']}%  PL={trace['linearity']}%",
                fontsize=7, pad=4, color=PROJ_BASE[pi],
            )

    # Shared x-axis label
    fig.text(0.55, 0.02, "Pipeline step (block index)", ha="center", fontsize=8.5)

    # Legend
    handles = [
        Line2D([0],[0], color=SEED_COLORS[0], lw=1.5, marker="o", markersize=4,
               markerfacecolor=SEED_COLORS[0], label="Essay 1"),
        Line2D([0],[0], color=SEED_COLORS[1], lw=1.5, marker="o", markersize=4,
               markerfacecolor=SEED_COLORS[1], label="Essay 2"),
        Line2D([0],[0], color=SEED_COLORS[2], lw=1.5, marker="o", markersize=4,
               markerfacecolor=SEED_COLORS[2], label="Essay 3"),
        mpatches.Patch(color="#C62828",             label="Back-track"),
        mpatches.Patch(color="#B71C1C", alpha=0.18, label="Escalation zone"),
        Line2D([0],[0], marker="v", color="w", markerfacecolor="#6A1B9A",
               markersize=6, label="SM delegation"),
        Line2D([0],[0], marker="D", color="w", markerfacecolor="#E91E63",
               markersize=5, label="Re-delegation"),
    ]
    fig.suptitle("Pipeline execution traces — all 12 runs (4 projects × 3 essays)",
                 fontsize=9.5, fontweight="bold", y=0.99)
    fig.legend(handles=handles, loc="upper center", ncol=7, fontsize=7.5,
               bbox_to_anchor=(0.55, 0.965),
               framealpha=0.96, edgecolor="#CCCCCC", handlelength=1.2)

    for ext in ("png", "pdf"):
        p = FIG_DIR / f"fig_gantt_all.{ext}"
        fig.savefig(p, dpi=300 if ext == "png" else None, bbox_inches="tight", facecolor=C_BG)
        print(f"  Saved → {p}")
    if show:
        plt.show()
    plt.close(fig)


# ── main ─────────────────────────────────────────────────────────────────────

def run(show: bool = False) -> None:
    print("  Parsing execution traces for all 12 runs ...")
    traces_by_project: dict = {}
    for proj_id, run_ids in sorted(RUNS_BY_PROJECT.items()):
        for run_id in sorted(run_ids, key=lambda r: r.essay):
            print(f"    {run_id.folder_name} ...", end=" ", flush=True)
            t = _extract_run_trace(run_id)
            print(f"done  ({t['n_steps']} steps, SR={t['sr']}%, PL={t['linearity']}%)")
            traces_by_project.setdefault(proj_id, []).append(t)

    p1e3 = next(t for t in traces_by_project[1] if t["essay"] == 3)
    print("  Drawing single Gantt trace (P1E3) ...")
    plot_gantt_single(p1e3, show=show)

    print("  Drawing Gantt grid (4 × 3) ...")
    plot_gantt_grid(traces_by_project, show=show)


if __name__ == "__main__":
    run(show="--show" in sys.argv)
