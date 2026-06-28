"""
RQ1 Figures — Autonomy Boundaries & Coordination Quality
=========================================================

Fig 1 — Error Incident Analysis (RQ1a)
  4-panel composite:
  (a) Mean incidents per project: stacked bars (fixed / escalated) + ±std
  (b) Self-fix rate (SR) per project with ±std error bars
  (c) Phase distribution of incidents (mean counts across 3 seeds)
  (d) SR distribution across all 12 runs (jitter strip)

Fig 2 — Coordination Metrics Table (RQ1b)
  Visual table: 4 projects × 11 metrics, each cell "mean ± std".
  Cells color-coded best (green) / middle (yellow) / worst (red) per row.

Output (PNG + PDF):
  research_results/figures/fig_rq1a_error_analysis.{png,pdf}
  research_results/figures/fig_rq1b_metrics_table.{png,pdf}

Usage (from repo root):
  python -m research_results.scripts.plot_rq1
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from research_results.scripts.paths import RESULTS_ROOT

# ── Paths ─────────────────────────────────────────────────────────────────────
SUMMARY_DIR = RESULTS_ROOT / "summaries"
FIG_DIR     = RESULTS_ROOT / "figures"

# ── ICSE rc defaults ──────────────────────────────────────────────────────────
# Fonts sized for single-column print width (~3.5").  Figure is authored at
# actual print size so no scaling occurs in LaTeX (\includegraphics[width=\columnwidth]).
plt.rcParams.update({
    "font.family":        "sans-serif",
    "font.sans-serif":    ["Arial", "Helvetica Neue", "Helvetica", "DejaVu Sans"],
    "font.size":          9,
    "axes.titlesize":     9.5,
    "axes.labelsize":     9,
    "xtick.labelsize":    8.5,
    "ytick.labelsize":    8.5,
    "legend.fontsize":    8.5,
    "legend.framealpha":  0.92,
    "legend.edgecolor":   "#CCCCCC",
    "axes.linewidth":     0.7,
    "xtick.major.width":  0.6,
    "ytick.major.width":  0.6,
    "grid.linewidth":     0.4,
    "grid.color":         "#DDDDDD",
    "figure.dpi":         150,
    "savefig.dpi":        300,
    "savefig.bbox":       "tight",
})

# ── Pastel palette ────────────────────────────────────────────────────────────
C_FIXED  = "#7EC8A0"    # pastel teal  — auto-recovered
C_ESC    = "#F4956A"    # pastel coral — escalated / human needed
C_SR     = "#4477AA"    # medium blue  — self-fix rate line
C_BG     = "#FAFAFA"
C_PANEL  = "#F4F7FB"
C_GOOD   = "#C8E6C9"    # light green  — best value in table
C_MID    = "#FFF9C4"    # light yellow — middle value
C_BAD    = "#FFCDD2"    # light red    — worst value
C_HDR    = "#1A3A5C"    # dark blue    — table header

# 4 project accent colours (pastel)
PROJ_COLORS = ["#A8C8E8", "#A8D8A8", "#F5D8A0", "#E8B8D0"]
PROJ_LABELS = ["Proj. 1\n(Triage)", "Proj. 2\n(Blood)", "Proj. 3\n(Runway)", "Proj. 4\n(ATM)"]
PROJ_SHORT  = ["P1", "P2", "P3", "P4"]


def _spine_clean(ax, keep=("left", "bottom")):
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(sp in keep)
        if sp in keep:
            ax.spines[sp].set_linewidth(0.6)


def _save(fig, stem, show=False):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        p = FIG_DIR / f"{stem}.{ext}"
        fig.savefig(p, dpi=300 if ext == "png" else None, bbox_inches="tight", facecolor=C_BG)
        print(f"  Saved → {p}")
    if show:
        plt.show()
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# Fig 1 — RQ1a Error Analysis
# ══════════════════════════════════════════════════════════════════════════════

def _load_rq1a() -> list[dict]:
    return json.loads((SUMMARY_DIR / "rq1a_autonomy.json").read_text())["projects"]

def _load_rq1b() -> list[dict]:
    return json.loads((SUMMARY_DIR / "rq1b_coordination.json").read_text())["projects"]


def panel_a_incident_bars(ax, projects: list[dict]) -> None:
    """Grouped stacked bars: fixed + escalated, with ±std error caps."""
    x = np.arange(len(projects))
    w = 0.52

    fixed_m = [p["fixed_incidents"]["mean"]    for p in projects]
    fixed_s = [p["fixed_incidents"]["std"]     for p in projects]
    esc_m   = [p["escalated_incidents"]["mean"] for p in projects]
    esc_s   = [p["escalated_incidents"]["std"]  for p in projects]

    fixed_arr = np.array(fixed_m)
    esc_arr   = np.array(esc_m)
    fixed_std = np.array(fixed_s)
    esc_std   = np.array(esc_s)
    total_std = np.sqrt(fixed_std**2 + esc_std**2)  # combined std (independent)

    ax.bar(x, fixed_arr, width=w, color=C_FIXED, label="Auto-recovered",  zorder=3)
    ax.bar(x, esc_arr,   width=w, color=C_ESC,   label="Escalated",
           bottom=fixed_arr, zorder=3)

    # Error bars on total height
    ax.errorbar(x, fixed_arr + esc_arr, yerr=total_std,
                fmt="none", ecolor="#555555", elinewidth=1.0, capsize=4, capthick=1.0,
                zorder=5)

    # Annotate SR above each bar
    for proj, xi in zip(projects, x):
        sr_m = proj["self_fix_rate_pct"]["mean"]
        sr_s = proj["self_fix_rate_pct"]["std"]
        top  = proj["fixed_incidents"]["mean"] + proj["escalated_incidents"]["mean"]
        ax.text(xi, top + total_std[int(xi)] + 0.8,
                f"SR={sr_m:.0f}±{sr_s:.0f}%",
                ha="center", va="bottom", fontsize=8.5, color=C_SR, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(PROJ_LABELS, fontsize=9)
    ax.set_ylabel("Mean error incidents", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=0)
    _spine_clean(ax)
    ax.legend(loc="upper left", handlelength=1.0, handletextpad=0.4, borderpad=0.5)
    ax.set_title("Error incidents per project  (mean ± std, n=3 seeds)",
                 fontsize=9.5, loc="left", pad=18, fontweight="bold")


def panel_b_sr_bars(ax, projects: list[dict]) -> None:
    """SR horizontal bar chart with ±std error bars."""
    y = np.arange(len(projects))
    sr_m = np.array([p["self_fix_rate_pct"]["mean"] for p in projects])
    sr_s = np.array([p["self_fix_rate_pct"]["std"]  for p in projects])

    bars = ax.barh(y, sr_m, height=0.52, color=PROJ_COLORS[:len(projects)],
                   edgecolor="#AAAAAA", linewidth=0.5, zorder=3)
    ax.errorbar(sr_m, y, xerr=sr_s, fmt="none",
                ecolor="#555555", elinewidth=1.0, capsize=4, capthick=1.0, zorder=5)

    # Value labels
    for yi, (m, s) in enumerate(zip(sr_m, sr_s)):
        ax.text(m + s + 1.5, yi, f"{m:.1f}%",
                va="center", ha="left", fontsize=8, color="#333333")

    ax.set_yticks(y)
    ax.set_yticklabels(PROJ_SHORT, fontsize=8.5)
    ax.set_xlabel("Self-fix Rate SR (%)", fontsize=8.5)
    ax.set_xlim(0, 115)
    ax.axvline(50, color="#BBBBBB", linewidth=0.7, linestyle="--", zorder=0)
    ax.grid(axis="x", linestyle="--", alpha=0.35, zorder=0)
    ax.invert_yaxis()
    _spine_clean(ax, keep=("bottom", "left"))
    ax.set_title("(b) Self-fix rate (SR) per project",
                 fontsize=9, loc="left", pad=5, fontweight="bold")


def panel_c_phase_heatmap(ax, projects: list[dict]) -> None:
    """
    Heatmap: project × phase, showing mean escalated incidents per phase.
    """
    from paper.log_analysis.phases import PHASE_ORDER, PHASE_INFO
    phase_labels = [PHASE_INFO[p].label for p in PHASE_ORDER
                    if PHASE_INFO[p].label not in ("Project Init", "Orchestration")]
    phases_shown = [p.value for p in PHASE_ORDER
                    if PHASE_INFO[p].label not in ("Project Init", "Orchestration")]

    matrix = np.zeros((len(projects), len(phases_shown)))
    for i, proj in enumerate(projects):
        for j, ph in enumerate(phases_shown):
            esc = proj["by_phase"].get(ph, {})
            matrix[i, j] = esc.get("escalated", {}).get("mean", 0)

    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("esc", ["#F0F8FF", "#F4956A"], N=256)
    vmax = max(matrix.max(), 1)
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=vmax,
                   interpolation="nearest")

    for i in range(len(projects)):
        for j in range(len(phases_shown)):
            v = matrix[i, j]
            txt = f"{v:.1f}" if v > 0 else "—"
            color = "white" if v / vmax > 0.55 else "#333333"
            ax.text(j, i, txt, ha="center", va="center",
                    fontsize=7.5, color=color, fontweight="bold" if v > 0 else "normal")

    # Grid lines
    for i in range(len(projects) + 1):
        ax.axhline(i - 0.5, color="#CCCCCC", linewidth=0.4)
    for j in range(len(phases_shown) + 1):
        ax.axvline(j - 0.5, color="#CCCCCC", linewidth=0.4)

    short = {"Project Init": "Init", "User Stories": "Stories", "Planning": "Plan.",
             "Requirements": "Req.", "Formal Spec": "Spec", "UML Design": "Sys. Design",
             "Architecture": "Arch. Design", "Implementation": "Impl.", "Testing": "Test",
             "Frontend": "FE", "DevOps": "DevOps", "Verification": "Verif."}
    ax.set_xticks(range(len(phases_shown)))
    ax.set_xticklabels([short.get(l, l) for l in phase_labels],
                       rotation=40, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(projects)))
    ax.set_yticklabels(PROJ_SHORT, fontsize=8.5)
    ax.tick_params(length=0)
    _spine_clean(ax, keep=())
    ax.set_title("(c) Mean escalated incidents by phase (per project)",
                 fontsize=9, loc="left", pad=5, fontweight="bold")


def panel_d_sr_jitter(ax, rq1b_projects: list[dict]) -> None:
    """SR distribution: each dot = one essay run; box overlay."""
    # Load raw per-run values from rq1b (which includes SR per run)
    data = json.loads((SUMMARY_DIR / "rq1b_coordination.json").read_text())["projects"]

    for i, proj in enumerate(data):
        vals = proj["SR"]["values"]
        mean = proj["SR"]["mean"]
        std  = proj["SR"]["std"]

        # jitter
        jx = np.random.RandomState(42 + i).uniform(-0.12, 0.12, len(vals))
        ax.scatter([i + jx[k] for k in range(len(vals))], vals,
                   color=PROJ_COLORS[i], s=38, zorder=4,
                   edgecolors="#888888", linewidths=0.5)

        # mean ± std whisker
        ax.errorbar(i, mean, yerr=std, fmt="D", color="#333333",
                    markersize=6, elinewidth=1.3, capsize=5, capthick=1.3, zorder=5)

    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(PROJ_SHORT, fontsize=8.5)
    ax.set_ylabel("SR (%)", fontsize=8.5)
    ax.set_ylim(-5, 115)
    ax.axhline(50, color="#BBBBBB", linewidth=0.7, linestyle="--", zorder=0)
    ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    _spine_clean(ax)
    ax.set_title("(d) SR per seed  (◆ = mean ± std)",
                 fontsize=9, loc="left", pad=5, fontweight="bold")


def plot_rq1a(show: bool = False) -> None:
    rq1a = _load_rq1a()

    # Two-column span (≈7" wide) so bars have room to breathe.
    # In LaTeX use \begin{figure*} + \includegraphics[width=\textwidth].
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_PANEL)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.18)

    panel_a_incident_bars(ax, rq1a)

    # Overall SR across all 12 runs
    all_fixed = sum(p["fixed_incidents"]["mean"] * p["n_essays"] for p in rq1a)
    all_total = sum(p["total_incidents"]["mean"]  * p["n_essays"] for p in rq1a)
    overall_sr = all_fixed / all_total * 100 if all_total else 0

    fig.suptitle(
        f"Overall SR ≈ {overall_sr:.1f}%  ·  4 projects × 3 seeds",
        fontsize=9, fontweight="bold", y=0.97, color="#222222",
    )
    _save(fig, "fig_rq1a_error_analysis", show)


# ══════════════════════════════════════════════════════════════════════════════
# Fig 2 — RQ1b Metrics Table
# ══════════════════════════════════════════════════════════════════════════════

def plot_rq1b_table(show: bool = False) -> None:
    """
    Matplotlib table: rows = metrics, cols = projects.
    Each cell shows "mean ± std". Best/middle/worst per row are color-coded.
    """
    data = _load_rq1b()
    n_proj = len(data)

    # (row_label, key, is_higher_better, section)
    ROW_DEFS = [
        # Execution dynamics
        ("Pipeline steps",           "pipeline_steps",    None,  "Execution Dynamics"),
        ("Phase back-tracks",        "phase_backtracks",  False, "Execution Dynamics"),
        ("Phase re-entries",         "phase_reentries",   False, "Execution Dynamics"),
        ("Orch. overhead (%)",       "orch_overhead_pct", False, "Execution Dynamics"),
        # Delegation quality
        ("SM delegation events",     "sm_delegations",    None,  "Delegation Quality"),
        ("Re-delegation events",     "redelegations",     False, "Delegation Quality"),
        ("Escalation zone (%)",      "escalation_zone_pct", False, "Delegation Quality"),
        # Recovery behavior
        ("Total incidents",          "total_incidents",   False, "Recovery Behavior"),
        ("Escalated (unresolved)",   "escalated_incidents", False, "Recovery Behavior"),
        ("Self-fix rate SR (%)",     "SR",                True,  "Recovery Behavior"),
        ("Wall clock (min)",         "wall_clock_min",    False, "Recovery Behavior"),
    ]

    def _cell_str(proj: dict, key: str) -> str:
        d = proj.get(key, {})
        m, s = d.get("mean", 0), d.get("std", 0)
        if key in ("PL", "DS"):
            return f"{m:.3f} ± {s:.3f}"
        if key in ("SR", "orch_overhead_pct", "escalation_zone_pct"):
            return f"{m:.1f} ± {s:.1f}"
        if key == "wall_clock_min":
            return f"{m:.0f} ± {s:.0f}"
        return f"{m:.0f} ± {s:.0f}"

    def _color_cell(val_str: str, all_strs: list[str], higher_better):
        if higher_better is None:
            return "#FFFFFF"
        def _num(s: str) -> float:
            try:
                return float(s.split("±")[0].strip())
            except ValueError:
                return 0.0
        nums = [_num(s) for s in all_strs]
        n = _num(val_str)
        best  = max(nums) if higher_better else min(nums)
        worst = min(nums) if higher_better else max(nums)
        if n == best:  return C_GOOD
        if n == worst: return C_BAD
        return C_MID

    # Build cell text and colors
    col_labels = ["Metric"] + [f"Project {p['project_id']}" for p in data]
    cell_text   = []
    cell_colors = []
    section_rows = {}  # section_name → set of row indices

    for idx, (label, key, higher, section) in enumerate(ROW_DEFS):
        vals = [_cell_str(p, key) for p in data]
        colors = [_color_cell(v, vals, higher) for v in vals]
        cell_text.append([label] + vals)
        cell_colors.append(["#F2F2F2"] + colors)
        section_rows.setdefault(section, []).append(idx)

    fig, ax = plt.subplots(figsize=(13, 6.5))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.axis("off")

    tbl = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
        cellColours=cell_colors,
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.0, 1.65)

    # Header styling
    for j in range(len(col_labels)):
        cell = tbl[0, j]
        cell.set_facecolor(C_HDR)
        cell.get_text().set_color("white")
        cell.get_text().set_fontweight("bold")
        cell.get_text().set_fontsize(9)

    # Bold + left-align metric labels; add section dividers
    section_starts = set()
    for section, row_list in section_rows.items():
        section_starts.add(row_list[0])

    for ri in range(len(ROW_DEFS)):
        tbl[ri + 1, 0].get_text().set_ha("left")
        tbl[ri + 1, 0].get_text().set_fontweight("bold")
        tbl[ri + 1, 0].get_text().set_fontsize(8)

        # Thicker top border for section starts
        if ri in section_starts and ri > 0:
            for j in range(len(col_labels)):
                tbl[ri + 1, j].visible_edges = "BRTL"

    # Section headers as coloured rows (insert via ax.text — table doesn't support row labels easily)
    # Instead we shade the section header rows differently
    section_header_rows = {0: "Execution Dynamics", 4: "Delegation Quality", 7: "Recovery Behavior"}
    for row_idx, label in section_header_rows.items():
        for j in range(len(col_labels)):
            cell = tbl[row_idx + 1, j]
            if j == 0:
                cell.set_facecolor("#E8EDF5")
            else:
                cell.set_facecolor("#E8EDF5")

    # Legend patches
    handles = [
        mpatches.Patch(facecolor=C_GOOD, edgecolor="#AAAAAA", linewidth=0.5, label="Best per row"),
        mpatches.Patch(facecolor=C_MID,  edgecolor="#AAAAAA", linewidth=0.5, label="Middle"),
        mpatches.Patch(facecolor=C_BAD,  edgecolor="#AAAAAA", linewidth=0.5, label="Worst per row"),
    ]
    ax.legend(handles=handles, loc="lower right", ncol=3,
              fontsize=8, framealpha=0.9, edgecolor="#CCCCCC",
              handlelength=1.0, handletextpad=0.4)

    ax.set_title(
        "RQ1b — Orchestration Quality Metrics  ·  "
        "4 Projects × 3 Seeds  ·  Values: mean ± std\n"
        "SR = N_fixed / N_incidents   "
        "PL = (N_steps − N_backtracks) / N_steps   "
        "DS = (N_deleg − N_redeleg) / N_deleg",
        fontsize=9, pad=10, fontweight="bold", color="#222222",
    )
    _save(fig, "fig_rq1b_metrics_table", show)


# ── main ─────────────────────────────────────────────────────────────────────

def run(show: bool = False) -> None:
    print("  Generating RQ1a error analysis figure ...")
    plot_rq1a(show=show)
    print("  Generating RQ1b coordination metrics table ...")
    plot_rq1b_table(show=show)


if __name__ == "__main__":
    run(show="--show" in sys.argv)
