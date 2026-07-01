from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CompetencyTrendChartBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CompetencyTrendChartCreate(CompetencyTrendChartBase):
    competency_id: Optional[int] = None
    question_id: Optional[int] = None
    student_id: Optional[int] = None


class CompetencyTrendChartUpdate(CompetencyTrendChartBase):
    competency_id: Optional[int] = None
    question_id: Optional[int] = None
    student_id: Optional[int] = None


class CompetencyTrendChartResponse(CompetencyTrendChartBase):
    id: int
    competency_id: Optional[int] = None
    question_id: Optional[int] = None
    student_id: Optional[int] = None
