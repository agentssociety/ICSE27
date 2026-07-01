from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from src.domain.study_tip import State

@dataclass
class CompetencyBreakdownService:
    def get_breakdown(self, student_id: str, exam_id: str) -> dict[str, Any]:
        return {}

    def calculate_competency_scores(self, answers: dict[str, str], competencies: dict[str, list[str]]) -> dict[str, float]:
        scores = {}
        for comp_name, question_ids in competencies.items():
            if question_ids:
                correct = sum(1 for qid in question_ids if qid in answers)
                scores[comp_name] = correct / len(question_ids) * 100.0
            else:
                scores[comp_name] = 0.0
        return scores
