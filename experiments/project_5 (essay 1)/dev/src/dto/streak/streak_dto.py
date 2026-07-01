from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field


class StreakBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StreakCreate(StreakBase):
    student_id: int
    current_streak: int = 0
    longest_streak: int = 0


class StreakUpdate(StreakBase):
    current_streak: Optional[int] = None
    longest_streak: Optional[int] = None


class StreakResponse(StreakBase):
    id: int
    student_id: int
    current_streak: int
    longest_streak: int

    @computed_field
    @property
    def multiplier(self) -> float:
        if self.current_streak >= 5:
            return 3.0
        elif self.current_streak >= 3:
            return 2.0
        elif self.current_streak >= 1:
            return 1.5
        return 1.0
