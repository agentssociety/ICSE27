from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FlightBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FlightCreate(FlightBase):
    flightNumber: str
    airline: str
    origin: str
    destination: str
    scheduledTime: datetime
    type: str
    note: Optional[str] = ''


class FlightUpdate(FlightBase):
    flightNumber: Optional[str] = None
    airline: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    scheduledTime: Optional[datetime] = None
    type: Optional[str] = None
    note: Optional[str] = None


class FlightResponse(FlightBase):
    id: int
    flightNumber: str
    airline: str
    origin: str
    destination: str
    scheduledTime: datetime
    type: str
    note: str


# Aliases for backwards compatibility with API tests
FlightRegistrationRequest = FlightCreate
FlightUpdateRequest = FlightUpdate
