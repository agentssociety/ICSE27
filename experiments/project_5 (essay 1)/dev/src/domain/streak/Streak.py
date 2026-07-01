from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    pass

"""
Domain layer for the Streak domain class

Package: domain.streak
Layer: domain
Related tasks: #112
Requirement coverage:
- Streak System Implementation
"""


@dataclass
class Streak:
    student_id: str
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: str = ""

    def record_activity(self, date: str) -> None:
        self.current_streak += 1
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        self.last_activity_date = date

    def reset_streak(self) -> None:
        self.current_streak = 0

@dataclass
class StreakId:
    pass

@dataclass
class StreakCreatedEvent:
    pass

@dataclass
class StreakUpdatedEvent:
    pass
