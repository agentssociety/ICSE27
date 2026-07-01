from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    pass

"""
Domain layer for the Cohort domain class

Package: domain.cohort
Layer: domain
Related tasks: #108, #115
Requirement coverage:
- Cohort Creation and Management
- Cohort Leaderboard Ranked by Nuggets
"""


@dataclass
class Cohort:
    name: str
    description: str = ""
    student_ids: list[str] = field(default_factory=list)

    def add_student(self, student_id: str) -> None:
        if student_id not in self.student_ids:
            self.student_ids.append(student_id)

    def remove_student(self, student_id: str) -> None:
        if student_id in self.student_ids:
            self.student_ids.remove(student_id)

    def get_student_count(self) -> int:
        return len(self.student_ids)

@dataclass
class CohortId:
    pass

@dataclass
class CohortCreatedEvent:
    pass

@dataclass
class CohortUpdatedEvent:
    pass
