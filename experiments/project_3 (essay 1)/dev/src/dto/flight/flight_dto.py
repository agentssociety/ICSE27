from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class FlightBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FlightCreate(FlightBase):
    flightNumber: str
    aircraftType: str


class FlightUpdate(FlightBase):
    flightNumber: Optional[str] = None
    aircraftType: Optional[str] = None


class FlightResponse(FlightBase):
    id: int
    flightNumber: str
    aircraftType: str
