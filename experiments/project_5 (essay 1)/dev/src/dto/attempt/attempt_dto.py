from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AttemptBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AttemptCreate(AttemptBase):
    method_isCompleted: bool
    student_id: int


class AttemptUpdate(AttemptBase):
    method_isCompleted: Optional[bool] = None
    student_id: Optional[int] = None


class AttemptResponse(AttemptBase):
    id: int
    method_isCompleted: bool
    student_id: Optional[int] = None
