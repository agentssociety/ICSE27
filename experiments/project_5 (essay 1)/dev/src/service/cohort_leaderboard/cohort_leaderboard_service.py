from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from src.domain.instructor import Instructor
    from src.domain.student import Student
    from src.domain.study_tip import Actor, Permission, State

@dataclass
class RankedStudent:
    student_id: str = ""
    score: float = 0.0
    rank: int = 0

@dataclass
class CohortLeaderboardService:
    def viewLeaderboard(self, cohort_id: str) -> list[RankedStudent]:
        return []

    def aggregateAndRank(self, nuggets: list) -> list[RankedStudent]:
        ranked = []
        for i, n in enumerate(sorted(nuggets, key=lambda x: getattr(x, 'score', 0) if hasattr(x, 'score') else float(x), reverse=True)):
            student_id = getattr(n, 'student_id', '') if hasattr(n, 'student_id') else ''
            score_val = getattr(n, 'score', 0) if hasattr(n, 'score') else float(n)
            ranked.append(RankedStudent(student_id=student_id, score=score_val, rank=i+1))
        return ranked

    def configureLeaderboard(self, instructor: Instructor, settings: dict) -> None:
        pass
