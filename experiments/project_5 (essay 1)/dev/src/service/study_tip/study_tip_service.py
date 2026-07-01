from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from src.domain.study_tip import State

@dataclass
class StudyTipService:
    def get_tips_for_competency(self, competency_id: str) -> list[dict[str, Any]]:
        return []

    def get_tips_for_weak_areas(self, competency_scores: dict[str, float]) -> list[dict[str, Any]]:
        weak_areas = {k: v for k, v in competency_scores.items() if v < 60.0}
        return [{"competency": k, "score": v, "tip": f"Practice more in {k}"} for k, v in weak_areas.items()]
