from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReservationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReservationCreate(ReservationBase):
    bloodUnitId: str
    transfusionRequestId: str
    bloodUnit_id: int


class ReservationUpdate(ReservationBase):
    bloodUnitId: Optional[str] = None
    transfusionRequestId: Optional[str] = None
    bloodUnit_id: Optional[int] = None
    status: Optional[str] = None


class ReservationResponse(ReservationBase):
    id: str
    bloodUnitId: str
    transfusionRequestId: str
    bloodUnit_id: Optional[int] = None
    status: str = "active"
