from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class SymptomRecordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SymptomRecordCreate(SymptomRecordBase):
    recordId: str
    symptomData: str
    patientId: str
    symptom_id: int


class SymptomRecordUpdate(SymptomRecordBase):
    recordId: Optional[str] = None
    symptomData: Optional[str] = None
    patientId: Optional[str] = None
    symptom_id: Optional[int] = None


class SymptomRecordResponse(SymptomRecordBase):
    id: int
    recordId: str
    symptomData: str
    patientId: str
    symptom_id: Optional[int] = None
