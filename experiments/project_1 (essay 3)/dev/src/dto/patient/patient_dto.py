from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PatientCreate(PatientBase):
    username: str
    authentication_id: int


class PatientUpdate(PatientBase):
    username: Optional[str] = None
    authentication_id: Optional[int] = None


class PatientResponse(PatientBase):
    id: int
    username: str
    authentication_id: Optional[int] = None
