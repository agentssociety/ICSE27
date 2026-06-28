from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class FlightBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FlightCreate(FlightBase):
    flightNumber: str
    origin: str
    destination: str
    estimatedDepartureTime: str


class FlightUpdate(FlightBase):
    flightNumber: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    estimatedDepartureTime: Optional[str] = None


class FlightResponse(FlightBase):
    id: int
    flightNumber: str
    origin: str
    destination: str
    estimatedDepartureTime: str
