from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompetencyBreakdownBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CompetencyBreakdownCreate(CompetencyBreakdownBase):
    exam_session_id: int
    competency_name: str
    score: float
    max_score: float
    is_weak: bool = False


class CompetencyBreakdownUpdate(CompetencyBreakdownBase):
    score: Optional[float] = None
    max_score: Optional[float] = None
    is_weak: Optional[bool] = None


class CompetencyBreakdownResponse(CompetencyBreakdownBase):
    id: int
    exam_session_id: int
    competency_name: str
    score: float
    max_score: float
    is_weak: bool
