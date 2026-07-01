from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AttemptReviewBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AttemptReviewCreate(AttemptReviewBase):
    competency_id: Optional[int] = None
    question_id: Optional[int] = None
    student_id: Optional[int] = None


class AttemptReviewUpdate(AttemptReviewBase):
    competency_id: Optional[int] = None
    question_id: Optional[int] = None
    student_id: Optional[int] = None


class AttemptReviewResponse(AttemptReviewBase):
    id: int
    competency_id: Optional[int] = None
    question_id: Optional[int] = None
    student_id: Optional[int] = None
