"""
RQ2 Figures — Quality Evaluation
==================================

Fig 3 — Token Consumption per Task per Phase (stacked bars + ±std)
  Bars show mean input / output tokens per task, per SDLC phase.
  Error bars (total token std) per bar.

Fig 4 — Latency per Task per Phase (spline + ±std ribbon)
  Smooth spline of mean latency per task per phase with ±1 std ribbon.

Fig 5 — NLI Confidence Score Distribution (4-panel)
  (a) Distribution histogram + KDE, pooled across all runs
  (b) Box plot per project (3-seed spread visible)
  (c) Supported vs unsupported claims per project
  (d) Hallucination rate bar chart per project

Fig 6 — Quality Summary Dashboard
  (a) Alloy verification rate per project
  (b) Test pass rates (backend / frontend) per project
  (c) Deployment success rate per project
  (d) Code hallucination: orphan routes + unused imports

Output (PNG + PDF):
  research_results/figures/fig_rq2_{tokens,latency,nli,quality}.{png,pdf}

Usage (from repo root):
  python -m research_results.scripts.plot_rq2
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from research_results.scripts.paths import RESULTS_ROOT
from paper.log_analysis.phases import PHASE_ORDER, PHASE_INFO, Phase

# ── Paths ─────────────────────────────────────────────────────────────────────
SUMMARY_DIR = RESULTS_ROOT / "summaries"
FIG_DIR     = RESULTS_ROOT / "figures"

# ── ICSE rc defaults ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":        "sans-serif",
    "font.sans-serif":    ["Arial", "Helvetica Neue", "Helvetica", "DejaVu Sans"],
    "font.size":          8.5,
    "axes.titlesize":     9.5,
    "axes.labelsize":     8.5,
    "xtick.labelsize":    8,
    "ytick.labelsize":    8,
    "legend.fontsize":    8,
    "legend.framealpha":  0.92,
    "legend.edgecolor":   "#CCCCCC",
    "axes.linewidth":     0.6,
    "xtick.major.width":  0.5,
    "ytick.major.width":  0.5,
    "grid.linewidth":     0.4,
    "grid.color":         "#DDDDDD",
    "figure.dpi":         150,
    "savefig.dpi":        300,
    "savefig.bbox":       "tight",
})

# ── Pastel palette ────────────────────────────────────────────────────────────
C_IN     = "#A8C8E8"    # pastel blue  — input tokens
C_OUT    = "#F5B8A0"    # pastel peach — output tokens
C_LINE   = "#6BAED6"    # medium blue  — spline line
C_FILL   = "#C6DBEF"    # fill under spline
C_GREEN  = "#A8D8A8"    # pastel green — supported claims / alloy pass
C_PEACH  = "#F5B8A0"    # unsupported / failures
C_PURPLE = "#C8A8E8"    # hallucination
C_AMBER  = "#F5D8A0"    # deployment
C_BG     = "#FAFAFA"
C_PANEL  = "#F4F7FB"
C_DARK   = "#3A3A4A"
C_GRID   = "#DDDDDD"
C_MUTED  = "#888888"

PROJ_COLORS = ["#A8C8E8", "#A8D8A8", "#F5D8A0", "#E8B8D0"]
PROJ_LABELS = ["Proj. 1\n(Triage)", "Proj. 2\n(Blood)", "Proj. 3\n(Runway)", "Proj. 4\n(ATM)"]
PROJ_SHORT  = ["P1", "P2", "P3", "P4"]

# Phase display names (short)
PHASE_SHORT = {
    "INIT":           "Init",
    "USER_STORIES":   "Stories",
    "PLANNING":       "Planning",
    "REQUIREMENTS":   "Req.",
    "FORMAL_SPEC":    "Formal\nSpec",
    "DESIGN_UML":     "Sys. Design",
    "ARCHITECTURE":   "Arch. Design",
    "IMPLEMENTATION": "Impl.",
    "TESTING":        "Testing",
    "FRONTEND":       "Frontend",
    "DEVOPS":         "DevOps",
    "VERIFICATION":   "Verif.",
    "ORCHESTRATION":  "Orch.",
}


def _spine_clean(ax, keep=("left", "bottom")):
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(sp in keep)
        if sp in keep:
            ax.spines[sp].set_linewidth(0.6)


def _fmt_tokens(n: float) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return f"{n:.0f}"


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
# Fig 3 — Token Consumption per Task per Phase
# ══════════════════════════════════════════════════════════════════════════════

def _load_tokens() -> dict:
    return json.loads((SUMMARY_DIR / "rq2_tokens_per_task.json").read_text())

def _load_latency() -> dict:
    return json.loads((SUMMARY_DIR / "rq2_latency_per_task.json").read_text())


def plot_tokens_per_task(show: bool = False) -> None:
    d = _load_tokens()

    # Use cross-project means with per-phase std
    phases_ordered = [p.value for p in PHASE_ORDER]
    phase_labels   = [PHASE_SHORT[p.value] for p in PHASE_ORDER]

    # Build arrays: for each phase, average across the 4 projects
    def _phase_mean_std(field: str):
        means, stds = [], []
        for ph in PHASE_ORDER:
            proj_means = []
            proj_stds  = []
            for proj in d["projects"]:
                pe = next((p for p in proj["phases"] if p["phase"] == ph.value), None)
                if pe and pe[field]["mean"] > 0:
                    proj_means.append(pe[field]["mean"])
                    proj_stds.append(pe[field]["std"])
            if proj_means:
                means.append(np.mean(proj_means))
                stds.append(np.mean(proj_stds))
            else:
                means.append(0.0)
                stds.append(0.0)
        return np.array(means), np.array(stds)

    in_means, in_stds  = _phase_mean_std("per_task_input")
    out_means, out_stds = _phase_mean_std("per_task_output")

    # Only show phases with non-trivial tokens
    active_mask = (in_means + out_means) > 100
    x      = np.arange(active_mask.sum())
    labels = [phase_labels[i] for i, m in enumerate(active_mask) if m]
    in_m   = in_means[active_mask]
    out_m  = out_means[active_mask]
    in_s   = in_stds[active_mask]
    out_s  = out_stds[active_mask]
    total_s = np.sqrt(in_s**2 + out_s**2)

    # Two-column print width — authored at 7" so LaTeX does not scale fonts.
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_PANEL)
    fig.subplots_adjust(left=0.10, right=0.97, top=0.80, bottom=0.20)

    w = 0.55
    ax.bar(x, in_m,  width=w, color=C_IN,  label="Input tokens",  zorder=3)
    ax.bar(x, out_m, width=w, color=C_OUT, label="Output tokens",
           bottom=in_m, zorder=3)

    # Error bars on total
    ax.errorbar(x, in_m + out_m, yerr=total_s,
                fmt="none", ecolor="#555555", elinewidth=1.0,
                capsize=4, capthick=1.0, zorder=5)

    # Annotate total above bar
    for xi, (im, om, ts) in enumerate(zip(in_m, out_m, total_s)):
        ax.text(xi, im + om + ts + (im + om) * 0.02,
                _fmt_tokens(im + om),
                ha="center", va="bottom", fontsize=8.5, color=C_DARK)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, rotation=35, ha="right")
    ax.set_ylabel("Mean tokens per task  (± std)", fontsize=9)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: _fmt_tokens(v))
    )
    ax.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID, zorder=0)
    _spine_clean(ax)
    ax.legend(fontsize=9, loc="upper right")
    ax.set_title(
        "Token consumption per task per SDLC phase",
        fontsize=9.5, fontweight="bold", pad=18,
    )
    _save(fig, "fig_rq2_tokens_per_task", show)


# ══════════════════════════════════════════════════════════════════════════════
# Fig 4 — Latency per Task per Phase (spline + ribbon)
# ══════════════════════════════════════════════════════════════════════════════

def plot_latency_per_task(show: bool = False) -> None:
    d = _load_latency()

    means, stds, labels = [], [], []
    for ph in PHASE_ORDER:
        proj_means, proj_stds = [], []
        for proj in d["projects"]:
            pe = next((p for p in proj["phases"] if p["phase"] == ph.value), None)
            if pe:
                m = pe["per_task_dur_s"]["mean"]
                s = pe["per_task_dur_s"]["std"]
                if m > 0.5:
                    proj_means.append(m)
                    proj_stds.append(s)
        if proj_means:
            means.append(np.mean(proj_means))
            stds.append(np.mean(proj_stds))
            labels.append(PHASE_SHORT[ph.value])

    means = np.array(means)
    stds  = np.array(stds)
    x     = np.arange(len(means), dtype=float)

    # Smooth spline
    try:
        from scipy.interpolate import make_interp_spline
        if len(x) >= 4:
            x_fine  = np.linspace(x[0], x[-1], 600)
            spl_m   = make_interp_spline(x, means, k=3)
            spl_s   = make_interp_spline(x, stds,  k=3)
            y_fine  = np.clip(spl_m(x_fine), 0, None)
            ys_fine = np.clip(spl_s(x_fine), 0, None)
        else:
            x_fine, y_fine, ys_fine = x.copy(), means.copy(), stds.copy()
    except ImportError:
        x_fine, y_fine, ys_fine = x.copy(), means.copy(), stds.copy()

    from paper.log_analysis.phases import PHASE_INFO
    dot_colors = [PHASE_INFO[ph].color for ph in PHASE_ORDER
                  if ph.value in [l.replace("\n", " ") for l in labels]]

    # Pastelify dot colors
    def _pastel(h: str) -> str:
        r, g, b = (int(h[i:i+2], 16) for i in (1, 3, 5))
        return f"#{int(r+(255-r)*0.4):02X}{int(g+(255-g)*0.4):02X}{int(b+(255-b)*0.4):02X}"

    # Two-column print width — authored at 7" so LaTeX does not scale fonts.
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_PANEL)
    fig.subplots_adjust(left=0.10, right=0.97, top=0.80, bottom=0.20)

    ax.fill_between(x_fine, np.clip(y_fine - ys_fine, 0, None),
                    y_fine + ys_fine, alpha=0.18, color=C_FILL, label="±1 std")
    ax.plot(x_fine, y_fine, color=C_LINE, linewidth=2.2, zorder=3, label="Mean")

    # Phase dots with individual colors
    for xi, (yi, si, ph) in enumerate(zip(means, stds, PHASE_ORDER)):
        if xi >= len(dot_colors):
            break
        color = _pastel(PHASE_INFO[ph].color) if PHASE_INFO[ph].color.startswith("#") else "#A8C8E8"
        ax.scatter(xi, yi, color=color, s=90, zorder=5,
                   edgecolors="#AAAAAA", linewidths=0.8)
        ax.annotate(
            f"{yi:.0f}s\n±{si:.0f}",
            xy=(xi, yi),
            xytext=(0, 13),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=8, color="#555555",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, rotation=35, ha="right")
    ax.set_ylabel("Mean latency per task (s)  ·  ±1 std ribbon", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID, zorder=0)
    _spine_clean(ax)
    ax.legend(fontsize=9, loc="upper right")
    ax.set_title(
        "Execution latency per task per SDLC phase",
        fontsize=9.5, fontweight="bold", pad=18,
    )
    _save(fig, "fig_rq2_latency_per_task", show)


# ══════════════════════════════════════════════════════════════════════════════
# Fig 5 — Confidence (model-level NLI + system-level alloy / tests / deployment)
# ══════════════════════════════════════════════════════════════════════════════

def plot_confidence(show: bool = False) -> None:
    """Confidence: model-level (NLI) + system-level (Alloy, tests, deployment)."""
    d_nli   = json.loads((SUMMARY_DIR / "rq2_nli_confidence.json").read_text())
    alloy   = json.loads((SUMMARY_DIR / "rq2_alloy_verification.json").read_text())["projects"]
    tests   = json.loads((SUMMARY_DIR / "rq2_test_passrate.json").read_text())["projects"]
    devops  = json.loads((SUMMARY_DIR / "rq2_devops.json").read_text())["projects"]

    pooled   = d_nli["pooled_all_runs"]
    projects = d_nli["projects"]
    all_scores_per_proj = {p["project_id"]: p["mean_confidence"]["values"] for p in projects}
    all_run_means = [v for proj in projects for v in proj["mean_confidence"]["values"]]
    vals = np.array(all_run_means)

    # 2 rows × 6 virtual columns:
    #   row 0: (a) NLI histogram [0:3], (b) NLI boxplot [3:6]
    #   row 1: (c) Alloy [0:2],  (d) Tests [2:4],  (e) Deployment [4:6]
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor(C_BG)
    gs = GridSpec(2, 6, figure=fig,
                  left=0.07, right=0.96, top=0.92, bottom=0.09,
                  hspace=0.50, wspace=0.60)
    ax_a = fig.add_subplot(gs[0, 0:3])
    ax_b = fig.add_subplot(gs[0, 3:6])
    ax_c = fig.add_subplot(gs[1, 0:2])
    ax_d = fig.add_subplot(gs[1, 2:4])
    ax_e = fig.add_subplot(gs[1, 4:6])
    for ax in (ax_a, ax_b, ax_c, ax_d, ax_e):
        ax.set_facecolor(C_PANEL)

    # ── (a) NLI alignment histogram ──────────────────────────────────────────
    ax_a.hist(vals, bins=16, color=C_IN, edgecolor="white", linewidth=0.6,
              density=True, alpha=0.85, zorder=3, label="Run means")
    try:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(vals, bw_method=0.4)
        xs  = np.linspace(0, 1, 300)
        ax_a.plot(xs, kde(xs), color=C_LINE, linewidth=2.2, zorder=4, label="KDE")
    except ImportError:
        pass
    lo = pooled["outlier_threshold_lo"]
    ax_a.axvline(lo, color="#D93535", linewidth=1.3, linestyle="--",
                 label=f"Outlier fence  {lo:.3f}")
    ax_a.set_xlabel("NLI Alignment Score  (precision of grounded claims per run)", fontsize=8.5)
    ax_a.set_ylabel("Density", fontsize=8.5)
    ax_a.set_xlim(0, 1.05)
    ax_a.legend(fontsize=8, handlelength=1.0)
    ax_a.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID)
    _spine_clean(ax_a)
    ax_a.set_title(
        f"(a) NLI alignment distribution  "
        f"(mean={pooled['mean']:.3f}, median={pooled['median']:.3f})\n"
        f"  Model-level — only grounded claims enter score (structurally high)",
        fontsize=9, loc="left", pad=5, fontweight="bold")

    # ── (b) Per-project NLI boxplot ──────────────────────────────────────────
    valid  = [(pid, v) for pid, v in all_scores_per_proj.items() if v]
    pids_b = [p for p, v in valid]
    data_b = [v for p, v in valid]
    bp = ax_b.boxplot(data_b, positions=range(len(pids_b)), widths=0.45,
                      patch_artist=True, notch=False,
                      medianprops=dict(color=C_LINE, linewidth=2),
                      whiskerprops=dict(linewidth=0.8),
                      capprops=dict(linewidth=0.8),
                      flierprops=dict(marker="o", markersize=5,
                                      markerfacecolor="#D93535", alpha=0.7))
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(PROJ_COLORS[pids_b[i] - 1])
        patch.set_alpha(0.75)
    for i, (pid, dv) in enumerate(valid):
        jx = np.random.RandomState(42 + i).uniform(-0.1, 0.1, len(dv))
        ax_b.scatter([i + j for j in jx], dv, color=PROJ_COLORS[pid - 1],
                     s=28, zorder=5, edgecolors="#888888", linewidths=0.5)
    ax_b.set_xticks(range(len(pids_b)))
    ax_b.set_xticklabels([PROJ_SHORT[p - 1] for p in pids_b], fontsize=8.5)
    ax_b.set_ylabel("NLI alignment score (grounded claims)", fontsize=8.5)
    ax_b.set_ylim(0.7, 1.05)
    ax_b.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID)
    _spine_clean(ax_b)
    ax_b.set_title(
        "(b) Per-project NLI alignment  (n=3 except P3: n=2 · ● = individual seeds)",
        fontsize=9, loc="left", pad=5, fontweight="bold")

    # ── (c) Alloy formal spec verification ───────────────────────────────────
    x = np.arange(4); w = 0.52
    rates_m = [p["verification_rate"]["mean"] * 100 for p in alloy]
    rates_s = [p["verification_rate"]["std"]  * 100 for p in alloy]
    ax_c.bar(x, rates_m, width=w, color=C_GREEN, edgecolor="#AAAAAA", linewidth=0.5, zorder=3)
    ax_c.errorbar(x, rates_m, yerr=rates_s, fmt="none",
                  ecolor="#555555", elinewidth=1.0, capsize=4, capthick=1.0, zorder=5)
    for xi, (m, s) in enumerate(zip(rates_m, rates_s)):
        ax_c.text(xi, m + s + 1, f"{m:.0f}%", ha="center", va="bottom",
                  fontsize=8.5, fontweight="bold", color=C_DARK)
    ax_c.set_xticks(x); ax_c.set_xticklabels(PROJ_SHORT, fontsize=8.5)
    ax_c.set_ylim(0, 120)
    ax_c.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax_c.set_ylabel("Alloy verification rate", fontsize=8.5)
    ax_c.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID)
    _spine_clean(ax_c)
    ax_c.set_title("(c) Formal spec verification  (Alloy SAT solver)",
                   fontsize=9, loc="left", pad=5, fontweight="bold")

    # ── (d) Test pass rates ──────────────────────────────────────────────────
    be_m = [p["backend_pass_rate"]["mean"]  * 100 for p in tests]
    be_s = [p["backend_pass_rate"]["std"]   * 100 for p in tests]
    fe_m = [p["frontend_pass_rate"]["mean"] * 100 for p in tests]
    fe_s = [p["frontend_pass_rate"]["std"]  * 100 for p in tests]
    bw = 0.3
    ax_d.bar(x - bw/2, be_m, width=bw, color=C_IN,    label="Backend",  zorder=3,
             edgecolor="#AAAAAA", linewidth=0.5)
    ax_d.bar(x + bw/2, fe_m, width=bw, color=C_GREEN, label="Frontend", zorder=3,
             edgecolor="#AAAAAA", linewidth=0.5)
    ax_d.errorbar(x - bw/2, be_m, yerr=be_s, fmt="none",
                  ecolor="#555555", elinewidth=1.0, capsize=3, capthick=1.0, zorder=5)
    ax_d.errorbar(x + bw/2, fe_m, yerr=fe_s, fmt="none",
                  ecolor="#555555", elinewidth=1.0, capsize=3, capthick=1.0, zorder=5)
    for xi, (bm, fm) in enumerate(zip(be_m, fe_m)):
        ax_d.text(xi - bw/2, bm + 1.5, f"{bm:.0f}%",
                  ha="center", va="bottom", fontsize=7.5, color=C_DARK)
        ax_d.text(xi + bw/2, fm + 1.5, f"{fm:.0f}%",
                  ha="center", va="bottom", fontsize=7.5, color=C_DARK)
    ax_d.set_xticks(x); ax_d.set_xticklabels(PROJ_SHORT, fontsize=8.5)
    ax_d.set_ylim(85, 108)
    ax_d.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax_d.set_ylabel("Test pass rate", fontsize=8.5)
    ax_d.legend(fontsize=8, handlelength=1.0)
    ax_d.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID)
    _spine_clean(ax_d)
    ax_d.set_title("(d) Test pass rates  (backend pytest + frontend jest)",
                   fontsize=9, loc="left", pad=5, fontweight="bold")

    # ── (e) Deployment success ───────────────────────────────────────────────
    dep_m = [p["deployment_success_rate"]["mean"] * 100 for p in devops]
    dep_s = [p["deployment_success_rate"]["std"]  * 100 for p in devops]
    ax_e.bar(x, dep_m, width=w, color=C_AMBER,
             edgecolor="#AAAAAA", linewidth=0.5, zorder=3)
    ax_e.errorbar(x, dep_m, yerr=dep_s, fmt="none",
                  ecolor="#555555", elinewidth=1.0, capsize=4, capthick=1.0, zorder=5)
    for xi, (m, s) in enumerate(zip(dep_m, dep_s)):
        ax_e.text(xi, m + s + 1.5, f"{m:.0f}%",
                  ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_DARK)
    ax_e.set_xticks(x); ax_e.set_xticklabels(PROJ_SHORT, fontsize=8.5)
    ax_e.set_ylim(0, 120)
    ax_e.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax_e.set_ylabel("Deployment success rate", fontsize=8.5)
    ax_e.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID)
    _spine_clean(ax_e)
    ax_e.set_title("(e) Deployment success  (Docker compose + service health)",
                   fontsize=9, loc="left", pad=5, fontweight="bold")

    fig.suptitle(
        "RQ2 — Confidence  ·  "
        "Model-level (a–b: NLI alignment)  ·  "
        "System-level (c: Alloy formal spec  ·  d: Test pass rates  ·  e: Deployment)",
        fontsize=10, fontweight="bold", y=0.975, color="#222222",
    )
    _save(fig, "fig_rq2_confidence", show)


# ══════════════════════════════════════════════════════════════════════════════
# Fig 6 — Hallucination (task-level extrapolation + over-generation + code-level)
# ══════════════════════════════════════════════════════════════════════════════

def plot_hallucination(show: bool = False) -> None:
    """Hallucination illustration."""
    d_nli = json.loads((SUMMARY_DIR / "rq2_nli_confidence.json").read_text())
    hall  = json.loads((SUMMARY_DIR / "rq2_hallucination.json").read_text())["projects"]

    projects = d_nli["projects"]

    def _extrap(proj: dict) -> dict:
        return proj.get("spec_extrapolation_rate") or proj.get("overall_hallucination_rate", {})

    # 1 × 2 layout — two-column print width (~7")
    fig = plt.figure(figsize=(7.0, 3.2))
    fig.patch.set_facecolor(C_BG)
    gs = GridSpec(1, 2, figure=fig,
                  left=0.08, right=0.96, top=0.80, bottom=0.18,
                  wspace=0.42)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    for ax in (ax_a, ax_b):
        ax.set_facecolor(C_PANEL)

    # ── (a) Spec-grounded vs beyond-spec stacked bar ─────────────────────────
    hall_vals: dict[int, tuple[float, float]] = {}
    for proj in projects:
        pid   = proj["project_id"]
        field = _extrap(proj)
        hall_vals[pid] = (field.get("mean", 0.0), field.get("std", 0.0))
    pids_a = sorted(hall_vals)
    sup_m  = np.array([1 - hall_vals[p][0] for p in pids_a])
    uns_m  = np.array([hall_vals[p][0]      for p in pids_a])
    uns_s  = np.array([hall_vals[p][1]      for p in pids_a])
    x_a    = np.arange(len(pids_a))
    w      = 0.52
    ax_a.bar(x_a, sup_m, width=w, color=C_GREEN, label="Spec-grounded",         zorder=3)
    ax_a.bar(x_a, uns_m, width=w, color=C_PEACH, label="Beyond-spec (elicited)",
             bottom=sup_m, zorder=3)
    ax_a.errorbar(x_a, np.ones(len(pids_a)), yerr=uns_s,
                  fmt="none", ecolor="#555555", elinewidth=1.0,
                  capsize=4, capthick=1.0, zorder=5)
    for xi, (s, u) in enumerate(zip(sup_m, uns_m)):
        ax_a.text(xi, 1.06, f"{u:.0%}", ha="center", va="bottom",
                  fontsize=8.5, color=C_DARK, fontweight="bold")
    ax_a.set_xticks(x_a)
    ax_a.set_xticklabels([PROJ_SHORT[p - 1] for p in pids_a], fontsize=9)
    ax_a.set_ylim(0, 1.22)
    ax_a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax_a.set_ylabel("Fraction of claims", fontsize=9)
    ax_a.legend(fontsize=8.5, handlelength=1.0)
    ax_a.grid(axis="y", linestyle="--", alpha=0.4, color=C_GRID)
    _spine_clean(ax_a)
    ax_a.set_title("(a) Spec-grounded vs beyond-spec claims",
                   fontsize=9.5, loc="left", pad=18, fontweight="bold")

    # ── (b) Code structural issues ────────────────────────────────────────────
    x_b      = np.arange(4)
    orphan_m = [p["orphan_routes"]["mean"]  for p in hall]
    orphan_s = [p["orphan_routes"]["std"]   for p in hall]
    unused_m = [p["unused_imports"]["mean"] for p in hall]
    unused_s = [p["unused_imports"]["std"]  for p in hall]
    ax_b2    = ax_b.twinx()
    bw       = 0.3
    ax_b.bar(x_b - bw/2, orphan_m, width=bw, color=C_PURPLE, label="Orphan routes",
             zorder=3, edgecolor="#AAAAAA", linewidth=0.5)
    ax_b.errorbar(x_b - bw/2, orphan_m, yerr=orphan_s, fmt="none",
                  ecolor="#555555", elinewidth=1.0, capsize=3, capthick=1.0, zorder=5)
    ax_b2.bar(x_b + bw/2, unused_m, width=bw, color=C_PEACH, label="Unused imports",
              zorder=3, edgecolor="#AAAAAA", linewidth=0.5)
    ax_b2.errorbar(x_b + bw/2, unused_m, yerr=unused_s, fmt="none",
                   ecolor="#555555", elinewidth=1.0, capsize=3, capthick=1.0, zorder=5)
    ax_b.set_xticks(x_b)
    ax_b.set_xticklabels(PROJ_SHORT, fontsize=9)
    ax_b.set_ylabel("Orphan routes (count)", fontsize=9, color="#6B3FA0")
    ax_b2.set_ylabel("Unused imports (count)", fontsize=9, color="#C08050")
    ax_b.tick_params(axis="y", colors="#6B3FA0")
    ax_b2.tick_params(axis="y", colors="#C08050")
    ax_b.grid(axis="y", linestyle="--", alpha=0.3, color=C_GRID)
    h1 = mpatches.Patch(facecolor=C_PURPLE, edgecolor="#AAAAAA", linewidth=0.5,
                         label="Orphan routes (left axis)")
    h2 = mpatches.Patch(facecolor=C_PEACH,  edgecolor="#AAAAAA", linewidth=0.5,
                         label="Unused imports (right axis)")
    ax_b.legend(handles=[h1, h2], fontsize=8.5, handlelength=1.0, loc="upper left")
    ax_b.spines["top"].set_visible(False)
    ax_b.set_title("(b) Code structural issues",
                   fontsize=9.5, loc="left", pad=18, fontweight="bold")

    fig.suptitle(
        "RQ2 — Hallucination Illustration",
        fontsize=9.5, fontweight="bold", y=0.97, color="#222222",
    )
    _save(fig, "fig_rq2_hallucination", show)


# ── main ─────────────────────────────────────────────────────────────────────

def run(show: bool = False) -> None:
    print("  Generating confidence figure (NLI + Alloy + tests + deployment) ...")
    plot_confidence(show=show)
    print("  Generating hallucination figure (spec extrapolation + rejected stories + code) ...")
    plot_hallucination(show=show)
    print("  Generating token consumption figure ...")
    plot_tokens_per_task(show=show)
    print("  Generating latency figure ...")
    plot_latency_per_task(show=show)


if __name__ == "__main__":
    run(show="--show" in sys.argv)
