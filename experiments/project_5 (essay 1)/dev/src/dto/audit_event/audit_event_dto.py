from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuditEventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditEventCreate(AuditEventBase):
    event_type: str
    instructor_id: Optional[int] = None
    student_id: Optional[int] = None
    amount: Optional[float] = None
    justification: Optional[str] = None


class AuditEventResponse(AuditEventBase):
    id: int
    event_type: str
    instructor_id: Optional[int] = None
    student_id: Optional[int] = None
    amount: Optional[float] = None
    justification: Optional[str] = None
    timestamp: Optional[datetime] = None
