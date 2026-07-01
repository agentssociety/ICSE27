from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    pass

@dataclass
class StreakService:
    def record_activity(self, student_id: str, date: str) -> int:
        return 1

    def get_current_streak(self, student_id: str) -> int:
        return 0

    def get_longest_streak(self, student_id: str) -> int:
        return 0

    def reset_streak(self, student_id: str) -> None:
        pass
