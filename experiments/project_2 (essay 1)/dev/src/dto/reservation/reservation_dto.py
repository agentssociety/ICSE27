from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from typing import Optional


class ReservationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReservationCreateRequest(ReservationBase):
    bloodType: str
    quantity: int
    scheduledDate: str


class ReservationUpdateRequest(ReservationBase):
    bloodType: Optional[str] = None
    quantity: Optional[int] = None
    scheduledDate: Optional[str] = None


class ReservationResponse(ReservationBase):
    id: int
    bloodType: str
    quantity: int
    scheduledDate: str
    status: str
