from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class EnrollmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class EnrollmentCreate(EnrollmentBase):
    student_id: int
    cohort_id: Optional[int] = None
    exam_id: Optional[int] = None


class EnrollmentUpdate(EnrollmentBase):
    cohort_id: Optional[int] = None
    exam_id: Optional[int] = None


class EnrollmentResponse(EnrollmentBase):
    id: int
    student_id: int
    cohort_id: Optional[int] = None
    exam_id: Optional[int] = None
