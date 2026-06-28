from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class TriageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TriageAssessmentCreate(TriageBase):
    patientId: str
    severity: int
    notes: Optional[str] = None


class TriageAssessmentResponse(TriageBase):
    id: str
    patientId: str
    severity: int
    notes: Optional[str] = None
    createdAt: str


class TriageQueueEntry(TriageBase):
    patientId: str
    patientName: str
    severity: int
    waitTimeMinutes: int
    assessedAt: str


class MessageResponse(BaseModel):
    message: str
