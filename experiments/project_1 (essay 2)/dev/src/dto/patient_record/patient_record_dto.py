from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

class PatientRecordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class PatientRecordCreate(PatientRecordBase):
    owner_id: int

class PatientRecordUpdate(PatientRecordBase):
    owner_id: Optional[int] = None

class PatientRecordResponse(PatientRecordBase):
    id: int
    owner_id: Optional[int] = None
