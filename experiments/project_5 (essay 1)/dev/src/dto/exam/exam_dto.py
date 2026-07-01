from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ExamBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExamCreate(ExamBase):
    title: str
    description: Optional[str] = None
    instructor_id: Optional[int] = None
    cohort_ids: list[int] = []
    is_active: bool = True


class ExamUpdate(ExamBase):
    title: Optional[str] = None
    description: Optional[str] = None
    cohort_ids: Optional[list[int]] = None
    is_active: Optional[bool] = None


class ExamResponse(ExamBase):
    id: int
    title: str
    description: Optional[str] = None
    instructor_id: Optional[int] = None
    cohort_ids: list[int] = []
    is_active: bool = True
