from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ExamSessionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExamSessionCreate(ExamSessionBase):
    student_id: int
    exam_id: int
    answers: dict[Any, str]


class ExamSessionUpdate(ExamSessionBase):
    student_id: Optional[int] = None
    exam_id: Optional[int] = None
    answers: Optional[dict[Any, str]] = None


class ExamSessionResponse(ExamSessionBase):
    id: int
    student_id: Optional[int] = None
    exam_id: Optional[int] = None
    answers: dict[Any, str]