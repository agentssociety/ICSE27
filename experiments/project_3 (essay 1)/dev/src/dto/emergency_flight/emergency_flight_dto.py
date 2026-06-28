from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class EmergencyFlightBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class EmergencyFlightCreate(EmergencyFlightBase):
    flight_id: int
    slot_id: Optional[int] = None


class EmergencyFlightUpdate(EmergencyFlightBase):
    flight_id: Optional[int] = None
    slot_id: Optional[int] = None


class EmergencyFlightResponse(EmergencyFlightBase):
    id: str
    flight_id: Optional[int] = None
    slot_id: Optional[int] = None
