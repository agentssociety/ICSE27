from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BonusNuggetBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BonusNuggetCreate(BonusNuggetBase):
    amount: int
    justification: str
    teacherId: str
    studentId: str
    student_id: int
    auditEvent_id: int


class BonusNuggetUpdate(BonusNuggetBase):
    amount: Optional[int] = None
    justification: Optional[str] = None
    teacherId: Optional[str] = None
    studentId: Optional[str] = None
    student_id: Optional[int] = None
    auditEvent_id: Optional[int] = None


class BonusNuggetResponse(BonusNuggetBase):
    id: int
    amount: int
    justification: str
    teacherId: str
    studentId: str
    student_id: Optional[int] = None
    auditEvent_id: Optional[int] = None
