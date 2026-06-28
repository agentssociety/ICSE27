from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class TransfusionRequestBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TransfusionRequestCreate(TransfusionRequestBase):
    requestId: str
    patientId: str
    patientABORh: str
    bloodType: str
    patientID: str


class TransfusionRequestUpdate(TransfusionRequestBase):
    requestId: Optional[str] = None
    patientId: Optional[str] = None
    patientABORh: Optional[str] = None
    bloodType: Optional[str] = None
    patientID: Optional[str] = None


class TransfusionRequestResponse(TransfusionRequestBase):
    id: str
    requestId: str
    patientId: str
    patientABORh: str
    bloodType: str
    patientID: str
