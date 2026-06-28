from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PatientCreate(PatientBase):
    firstName: str
    lastName: str
    dateOfBirth: str
    gender: str
    contactPhone: str
    contactEmail: str
    address: str


class PatientUpdate(PatientBase):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    dateOfBirth: Optional[str] = None
    gender: Optional[str] = None
    contactPhone: Optional[str] = None
    contactEmail: Optional[str] = None
    address: Optional[str] = None


class PatientResponse(PatientBase):
    id: str
    firstName: str
    lastName: str
    dateOfBirth: str
    gender: str
    contactPhone: str
    contactEmail: str
    address: str
