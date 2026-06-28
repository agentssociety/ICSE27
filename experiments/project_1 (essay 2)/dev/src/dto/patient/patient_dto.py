from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class PatientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class PatientCreate(PatientBase):
    symptoms: str
    urgencyLevel: int
    queuePosition: int
    arrivalTime: datetime
    urgency: str

class PatientUpdate(PatientBase):
    symptoms: Optional[str] = None
    urgencyLevel: Optional[int] = None
    queuePosition: Optional[int] = None
    arrivalTime: Optional[datetime] = None
    urgency: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    symptoms: str
    urgencyLevel: int
    queuePosition: int
    arrivalTime: datetime
    urgency: str

class DashboardItem(BaseModel):
    patient_id: int
    symptoms: str
    urgency_level: int
    urgency: str
    queue_position: int
    estimated_wait_minutes: int
    arrival_time: str
