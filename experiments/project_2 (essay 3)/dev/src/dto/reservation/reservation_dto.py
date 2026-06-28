from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ReservationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReservationCreate(ReservationBase):
    request_id: int
    unit_id: int


class ReservationUpdate(ReservationBase):
    request_id: Optional[int] = None
    unit_id: Optional[int] = None


class ReservationResponse(ReservationBase):
    id: str
    request_id: Optional[int] = None
    unit_id: Optional[int] = None
