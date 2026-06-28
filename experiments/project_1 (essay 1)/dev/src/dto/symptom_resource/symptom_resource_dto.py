from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class SymptomResourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SymptomResourceCreate(SymptomResourceBase):
    patient_id: int


class SymptomResourceUpdate(SymptomResourceBase):
    patient_id: Optional[int] = None


class SymptomResourceResponse(SymptomResourceBase):
    id: int
    patient_id: Optional[int] = None
