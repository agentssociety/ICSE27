from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class TimeSlotBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimeSlotCreate(TimeSlotBase):
    flight_id: Optional[int] = None


class TimeSlotUpdate(TimeSlotBase):
    flight_id: Optional[int] = None


class TimeSlotResponse(TimeSlotBase):
    id: int
    flight_id: Optional[int] = None
