from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class SymptomBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SymptomCreate(SymptomBase):
    description: str
    language: str
    patientId: str
    patient_id: int


class SymptomUpdate(SymptomBase):
    description: Optional[str] = None
    language: Optional[str] = None
    patientId: Optional[str] = None
    patient_id: Optional[int] = None


class SymptomResponse(SymptomBase):
    id: int
    description: str
    language: str
    patientId: str
    patient_id: Optional[int] = None
