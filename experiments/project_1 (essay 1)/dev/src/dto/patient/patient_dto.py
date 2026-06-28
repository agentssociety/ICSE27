from __future__ import annotations

from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PatientCreate(PatientBase):
    patientId: UUID
    patientQueue_id: Optional[int] = None
    state: str = "pending_triage"
    arrival_time: Optional[datetime] = None
    urgency_level: int = 99


class PatientUpdate(PatientBase):
    patientId: Optional[UUID] = None
    patientQueue_id: Optional[int] = None
    state: Optional[str] = None
    arrival_time: Optional[datetime] = None
    urgency_level: Optional[int] = None


class PatientResponse(PatientBase):
    id: int
    patientId: UUID
    patientQueue_id: Optional[int] = None
    state: str
    arrival_time: Optional[datetime] = None
    urgency_level: int
