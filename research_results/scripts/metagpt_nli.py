"""
MetaGPT NLI Confidence Measurement
====================================

Applies the same NLI-based confidence measurement used for AgentsSociety to
MetaGPT's generated user stories. Produces output in the identical JSON schema
so numbers can be directly compared in the baseline comparison table.

Pipeline (mirrors ai/nli.py and the original AgentsSociety measurement):
  1. Load source specification  (docs/requirement.txt)
  2. Decompose spec into atomic fact sentences
  3. Load generated user stories  (docs/prd/<timestamp>.json → "User Stories")
  4. Decompose each user story into atomic claims
     - Handles "As a <role>, I want <action> so that <benefit>" format
  5. For each claim, score entailment against every fact using DeBERTa-v3-large-mnli
  6. A claim is "supported" if its best-fact score ≥ THRESHOLD (0.6, same as AgentsSociety)
  7. NLI alignment score = mean entailment score over supported claims only
     (mirrors the "confidence" field in AgentsSociety task_nli_*.json)
  8. Spec extrapolation rate = unsupported_claims / total_claims

Output files:
  research_results/data/nli/metagpt/P{N}_nli.json         — per-project results
  research_results/summaries/rq2_nli_metagpt.json          — aggregated summary

Usage:
  python -m research_results.scripts.metagpt_nli
  # or
  python research_results/scripts/metagpt_nli.py

Requirements:
  pip install transformers torch
  (model: khalidalt/DeBERTa-v3-large-mnli, downloaded on first run)
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Optional

# ── path setup ────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
REPO_ROOT    = SCRIPT_DIR.parent.parent
EXPERIMENTS  = REPO_ROOT / "experiments"
RESULTS_ROOT = SCRIPT_DIR.parent
DATA_DIR     = RESULTS_ROOT / "data" / "nli" / "metagpt"
SUMMARY_DIR  = RESULTS_ROOT / "summaries"

METAGPT_PROJECTS = {
    1: EXPERIMENTS / "project_1 (metagpt)" / "hospital_triage_queue",
    2: EXPERIMENTS / "project_2 (metagpt)",
    3: EXPERIMENTS / "project_3 (metagpt)",
    4: EXPERIMENTS / "project_4 (metagpt)",
}

THRESHOLD = 0.6   # same as AgentsSociety
MODEL_NAME = "khalidalt/DeBERTa-v3-large-mnli"

# ── lazy model loading ────────────────────────────────────────────────────────
_tokenizer = None
_model     = None
_device    = None


def _load_model() -> None:
    global _tokenizer, _model, _device
    if _model is not None:
        return
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    print(f"  Loading NLI model: {MODEL_NAME} ...", flush=True)
    _device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    _model     = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    _model.to(_device)
    _model.eval()
    print(f"  Model loaded on {_device}", flush=True)


def _nli_score(premise: str, hypothesis: str) -> float:
    """Return P(entailment) for the (premise, hypothesis) pair."""
    import torch
    _load_model()
    inputs = _tokenizer(
        premise, hypothesis,
        truncation=True, max_length=512,
        return_tensors="pt",
    )
    inputs = {k: v.to(_device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = _model(**inputs).logits[0]
    probs = torch.softmax(logits, dim=-1).tolist()
    # DeBERTa-v3-large-mnli label order: entailment=0, neutral=1, contradiction=2
    return probs[0]


# ── spec fact extraction ──────────────────────────────────────────────────────

def extract_facts(spec_text: str) -> list[str]:
    """
    Convert the source requirement.txt into atomic declarative fact sentences.

    Strategy:
    - Join continuation lines (non-empty, non-bullet lines after a bullet) with
      the preceding bullet to handle multi-line bullet points.
    - Each bullet → one declarative fact prefixed with "The system".
    - Non-bullet sentences that contain a verb are kept as-is.
    - Headings, blank lines, and very short fragments are skipped.
    """
    # First pass: merge continuation lines into their parent bullet
    raw_lines = spec_text.splitlines()
    merged: list[str] = []
    buf = ""
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            if buf:
                merged.append(buf)
                buf = ""
            continue
        if stripped.startswith("- "):
            if buf:
                merged.append(buf)
            buf = stripped
        elif buf:
            # continuation of previous bullet or sentence
            buf += " " + stripped
        else:
            merged.append(stripped)
    if buf:
        merged.append(buf)

    facts: list[str] = []
    for line in merged:
        if line.startswith("- "):
            body = line[2:].strip()
            if len(body) < 10:
                continue
            sentence = body if body.endswith(".") else body + "."
            # Prefix "The system " for action-style bullets
            lower = sentence.lower()
            starts_with_verb = any(sentence.lower().startswith(v) for v in
                                   ["register", "assign", "order", "reorder", "let ",
                                    "show", "track", "accept", "match", "alert",
                                    "allocate", "close", "declare", "authenticate",
                                    "verify", "decline", "rollback", "flag", "log",
                                    "allow", "support", "provide", "ensure", "handle"])
            if starts_with_verb or (not lower.startswith("the system") and not lower.startswith("a ")):
                sentence = "The system " + sentence[0].lower() + sentence[1:]
            facts.append(sentence)
        else:
            # Non-bullet: keep complete sentences that contain a predicate verb
            if len(line) > 20 and any(v in line.lower() for v in
                                       [" is ", " are ", " can ", " will ", " must ",
                                        " allows ", " supports ", " provides ",
                                        " ensures ", " handles ", " manages "]):
                facts.append(line if line.endswith(".") else line + ".")
    return facts


# ── user story claim extraction ───────────────────────────────────────────────

_AS_A_RE = re.compile(
    r"[Aa]s\s+a(?:n)?\s+(?P<role>[^,]+?),\s*"
    r"[Ii]\s+want\s+(?P<action>.+?)(?:\s+so\s+that\s+(?P<benefit>.+))?$",
    re.DOTALL,
)


def _clean(text: str) -> str:
    text = text.strip().rstrip(".")
    return text[0].upper() + text[1:] if text else text


def extract_claims_from_story(story: str) -> list[str]:
    """
    Decompose a "As a <role>, I want <action> so that <benefit>" user story
    into atomic claim sentences for NLI testing.

    Produces up to three claims per story:
      1. System capability: "The system enables users to <action>."
      2. Benefit outcome:   "<benefit>."
      3. Role-accessibility: "A <role> can <action>."
    """
    claims: list[str] = []
    m = _AS_A_RE.match(story.strip())

    if m:
        role    = _clean(m.group("role"))
        action  = _clean(m.group("action"))
        benefit = _clean(m.group("benefit")) if m.group("benefit") else None

        # Strip leading "to " produced by "I want to <infinitive>" pattern
        action_lower = action[0].lower() + action[1:]
        if action_lower.startswith("to "):
            action_lower = action_lower[3:]

        # Claim 1: system capability ("enables users to <infinitive>")
        claims.append(f"The system enables users to {action_lower}.")

        # Claim 2: benefit / rationale
        if benefit and len(benefit) > 8:
            claims.append(f"{benefit}.")

        # Claim 3: role-based accessibility ("A <role> can <action>")
        claims.append(f"A {role.lower()} can {action_lower}.")
    else:
        # Fallback: treat the whole story as one claim
        sentence = story.strip()
        if not sentence.endswith("."):
            sentence += "."
        claims.append(sentence)

    # Drop empty or near-empty claims
    return [c for c in claims if len(c) > 15]


# ── core NLI evaluation for one story ────────────────────────────────────────

def evaluate_story(
    story: str,
    facts: list[str],
    story_id: int,
) -> dict:
    """
    Evaluate a single user story against the fact set.

    Returns a dict in the same schema as AgentsSociety task_nli_*.json:
      task_id, confidence, total_claims, supported_claims, evidence, threshold
    """
    claims   = extract_claims_from_story(story)
    evidence = []

    for claim in claims:
        best_score = 0.0
        best_fact  = ""
        for fact in facts:
            score = _nli_score(fact, claim)
            if score > best_score:
                best_score = score
                best_fact  = fact

        if best_score >= THRESHOLD:
            evidence.append({
                "claim":           claim,
                "fact":            best_fact,
                "score":           round(best_score, 4),
                "user_story_span": "",
                "fact_span":       "",
            })

    supported = len(evidence)
    total     = len(claims)

    # NLI alignment score = mean entailment score of supported claims only
    # (identical definition to AgentsSociety "confidence" field)
    if supported > 0:
        confidence = round(sum(e["score"] for e in evidence) / supported, 4)
    else:
        confidence = 0.0

    return {
        "task_id":         story_id,
        "confidence":      confidence,
        "evidence":        evidence,
        "total_claims":    total,
        "supported_claims": supported,
        "threshold":       THRESHOLD,
    }


# ── project-level runner ──────────────────────────────────────────────────────

def _find_prd(project_root: Path) -> Optional[Path]:
    """Locate the PRD JSON file produced by MetaGPT."""
    candidates = sorted(project_root.glob("docs/prd/*.json"))
    if candidates:
        return candidates[-1]   # latest timestamp
    # Some projects put docs/ one level up
    candidates = sorted(project_root.parent.glob("docs/prd/*.json"))
    return candidates[-1] if candidates else None


def _find_requirement(project_root: Path) -> Optional[Path]:
    """Locate requirement.txt."""
    for p in [
        project_root / "docs" / "requirement.txt",
        project_root.parent / "docs" / "requirement.txt",
        project_root / "requirement.txt",
    ]:
        if p.exists():
            return p
    return None


def run_project(project_id: int, project_root: Path) -> dict:
    """
    Run the full NLI measurement for one MetaGPT project.
    Returns the project-level result dict.
    """
    print(f"\n=== P{project_id} ({project_root.name}) ===")

    # Load source specification
    req_path = _find_requirement(project_root)
    if not req_path:
        print(f"  ERROR: requirement.txt not found under {project_root}")
        return {"project_id": project_id, "error": "requirement.txt not found", "stories": []}
    spec_text = req_path.read_text(encoding="utf-8")
    facts     = extract_facts(spec_text)
    print(f"  Spec: {req_path.relative_to(REPO_ROOT)}  →  {len(facts)} facts extracted")

    # Load user stories from PRD
    prd_path = _find_prd(project_root)
    if not prd_path:
        print(f"  ERROR: PRD JSON not found under {project_root}")
        return {"project_id": project_id, "error": "PRD not found", "stories": []}
    prd      = json.loads(prd_path.read_text(encoding="utf-8"))
    stories  = prd.get("User Stories", [])
    print(f"  PRD: {prd_path.relative_to(REPO_ROOT)}  →  {len(stories)} user stories")

    # Evaluate each story
    results: list[dict] = []
    scores:  list[float] = []
    for idx, story in enumerate(stories, start=1):
        print(f"  Story {idx}/{len(stories)}: {story[:60]}...", flush=True)
        result = evaluate_story(story, facts, story_id=idx)
        results.append(result)
        if result["confidence"] > 0:
            scores.append(result["confidence"])
        print(f"    claims={result['total_claims']}, supported={result['supported_claims']}, "
              f"confidence={result['confidence']:.4f}")

    # Aggregate
    total_claims     = sum(r["total_claims"]     for r in results)
    supported_claims = sum(r["supported_claims"] for r in results)
    spec_coverage    = round(supported_claims / total_claims, 4) if total_claims else 0.0
    mean_conf        = round(_mean(scores), 4) if scores else 0.0

    q1, q3, iqr = _iqr(scores) if scores else (0, 0, 0)
    lo_thr = q1 - 1.5 * iqr
    hi_thr = q3 + 1.5 * iqr

    project_result = {
        "project_id":   project_id,
        "project_name": prd.get("Project Name", project_root.name),
        "spec_path":    str(req_path.relative_to(REPO_ROOT)),
        "prd_path":     str(prd_path.relative_to(REPO_ROOT)),
        "n_facts":      len(facts),
        "facts":        facts,
        "n_stories":    len(stories),
        "stories":      results,
        "summary": {
            "mean_nli_alignment_score":   mean_conf,
            "median_nli_alignment_score": round(_median(scores), 4) if scores else 0.0,
            "std_nli_alignment_score":    round(_std(scores),    4) if scores else 0.0,
            "q1":  round(q1, 4),
            "q3":  round(q3, 4),
            "iqr": round(iqr, 4),
            "n_outliers":       sum(1 for s in scores if s < lo_thr or s > hi_thr),
            "n_zero_alignment": sum(1 for s in scores if s == 0.0),
            "total_claims":        total_claims,
            "supported_claims":    supported_claims,
            "spec_coverage_rate":      spec_coverage,
            "spec_extrapolation_rate": round(1 - spec_coverage, 4),
            "overall_hallucination_rate": round(1 - spec_coverage, 4),
        },
    }
    return project_result


# ── statistics helpers (self-contained, no dep on rest of repo) ───────────────

def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0

def _std(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = _mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))

def _median(vals: list[float]) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    n = len(s)
    return (s[n // 2 - 1] + s[n // 2]) / 2 if n % 2 == 0 else s[n // 2]

def _percentile(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    idx = p / 100 * (len(s) - 1)
    lo, hi = int(idx), min(int(idx) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (idx - lo)

def _iqr(vals: list[float]) -> tuple[float, float, float]:
    q1 = _percentile(vals, 25)
    q3 = _percentile(vals, 75)
    return q1, q3, q3 - q1


# ── main ──────────────────────────────────────────────────────────────────────

def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("MetaGPT NLI Confidence Measurement")
    print(f"Model : {MODEL_NAME}")
    print(f"Threshold : {THRESHOLD}")
    print("=" * 60)

    all_projects: list[dict] = []
    all_scores:   list[float] = []

    for project_id, project_root in sorted(METAGPT_PROJECTS.items()):
        if not project_root.exists():
            print(f"\nP{project_id}: directory not found ({project_root}), skipping.")
            continue

        result = run_project(project_id, project_root)
        all_projects.append(result)

        # Save per-project file
        out_path = DATA_DIR / f"P{project_id}_nli.json"
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  → Saved: {out_path.relative_to(REPO_ROOT)}")

        if "summary" in result and result["summary"]:
            s = result["summary"]
            print(f"  Summary: alignment={s['mean_nli_alignment_score']:.4f}, "
                  f"coverage={s['spec_coverage_rate']:.2%}, "
                  f"extrapolation={s['spec_extrapolation_rate']:.2%}")
            # Collect scores for cross-project pooling (all tasks, including zero-confidence)
            for story in result.get("stories", []):
                all_scores.append(story.get("confidence", 0.0))

    # Cross-project pooled statistics
    q1, q3, iqr_val = _iqr(all_scores)
    lo_thr = q1 - 1.5 * iqr_val
    hi_thr = q3 + 1.5 * iqr_val

    # Build comparison table vs AgentsSociety
    agentsociety_ref = {
        "pooled_mean_alignment":        0.9683,
        "pooled_median_alignment":      0.9877,
        "pooled_std_alignment":         0.1112,
        "pooled_iqr_alignment":         0.0168,
        "spec_extrapolation_rate_mean": 0.522,
        "n_stories":                    82,
        "source":                       "summaries/rq2_nli_confidence.json",
    }

    summary = {
        "metric":      "rq2_nli_metagpt",
        "description": (
            "NLI-based confidence measurement for MetaGPT-generated user stories. "
            "Identical methodology to AgentsSociety NLI measurement: same model "
            f"({MODEL_NAME}), same entailment threshold ({THRESHOLD}), same "
            "metrics (alignment score = precision of grounded claims; "
            "extrapolation rate = fraction with no spec match)."
        ),
        "projects":    all_projects,
        "pooled_all_projects": {
            "n_stories":            len(all_scores),
            "mean":                 round(_mean(all_scores),   4),
            "median":               round(_median(all_scores), 4),
            "std":                  round(_std(all_scores),    4),
            "q1":                   round(q1,      4),
            "q3":                   round(q3,      4),
            "iqr":                  round(iqr_val, 4),
            "outlier_threshold_lo": round(lo_thr,  4),
            "outlier_threshold_hi": round(hi_thr,  4),
            "n_outliers":           sum(1 for s in all_scores if s < lo_thr or s > hi_thr),
            "n_zero_confidence":    sum(1 for s in all_scores if s == 0.0),
        },
        "comparison_with_agentsociety": agentsociety_ref,
    }

    out_summary = SUMMARY_DIR / "rq2_nli_metagpt.json"
    out_summary.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"{'Project':<30} {'Stories':>7} {'Alignment':>10} {'Coverage':>10} {'Extrapol.':>10}")
    print("-" * 60)
    for p in all_projects:
        s = p.get("summary", {})
        if s:
            print(f"  P{p['project_id']} {p.get('project_name',''):<25} "
                  f"{p['n_stories']:>7} "
                  f"{s['mean_nli_alignment_score']:>10.4f} "
                  f"{s['spec_coverage_rate']:>10.2%} "
                  f"{s['spec_extrapolation_rate']:>10.2%}")

    pool = summary["pooled_all_projects"]
    print("-" * 60)
    print(f"  {'MetaGPT pooled':<30} {pool['n_stories']:>7} {pool['mean']:>10.4f}")
    print(f"  {'AgentsSociety pooled':<30} {'82':>7} {agentsociety_ref['pooled_mean_alignment']:>10.4f}")
    print(f"\nSummary → {out_summary.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    run()
