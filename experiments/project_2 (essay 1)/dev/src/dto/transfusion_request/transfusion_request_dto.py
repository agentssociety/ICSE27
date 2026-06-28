from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from typing import Optional


class TransfusionRequestBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TransfusionRequestCreateRequest(TransfusionRequestBase):
    patientName: str
    bloodType: str
    quantity: int
    urgency: str


class TransfusionRequestUpdateRequest(TransfusionRequestBase):
    patientName: Optional[str] = None
    bloodType: Optional[str] = None
    quantity: Optional[int] = None
    urgency: Optional[str] = None


class TransfusionRequestResponse(TransfusionRequestBase):
    id: int
    patientName: str
    bloodType: str
    quantity: int
    urgency: str
    status: str
