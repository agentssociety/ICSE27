from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CohortLeaderboardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CohortLeaderboardCreate(CohortLeaderboardBase):
    student_id: Optional[int] = None


class CohortLeaderboardUpdate(CohortLeaderboardBase):
    student_id: Optional[int] = None


class CohortLeaderboardResponse(CohortLeaderboardBase):
    id: int
    student_id: Optional[int] = None
