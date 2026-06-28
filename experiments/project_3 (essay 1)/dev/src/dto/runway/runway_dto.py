from __future__ import annotations

from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RunwayBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RunwayCreate(RunwayBase):
    capacity: int
    configuration: str
    slot_id: Optional[int] = None


class RunwayUpdate(RunwayBase):
    capacity: Optional[int] = None
    configuration: Optional[str] = None
    slot_id: Optional[int] = None


class RunwayResponse(RunwayBase):
    id: str
    capacity: int
    configuration: str
    slot_id: Optional[int] = None


class TimetableEntry(BaseModel):
    slot_id: Optional[int] = None
    slot_time: Optional[int] = None
    flight_id: Optional[int] = None
    flight_number: Optional[str] = None
    aircraft_type: Optional[str] = None
    status: Optional[str] = None


class RunwayTimetableResponse(BaseModel):
    runway_id: str
    runway_status: Optional[str] = None
    entries: list[TimetableEntry] = []
