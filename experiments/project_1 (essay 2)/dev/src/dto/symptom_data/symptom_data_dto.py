from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

class SymptomDataBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class SymptomDataCreate(SymptomDataBase):
    owner_id: int

class SymptomDataUpdate(SymptomDataBase):
    owner_id: Optional[int] = None

class SymptomDataResponse(SymptomDataBase):
    id: int
    owner_id: Optional[int] = None
