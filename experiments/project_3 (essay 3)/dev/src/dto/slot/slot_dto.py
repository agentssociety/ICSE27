from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SlotBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SlotCreateRequest(SlotBase):
    startTime: datetime
    endTime: datetime
    flight_type: str = "arrival"
    duration: str = "5 minutes"
    gapAfter: str = "3 minutes"


class SlotUpdateRequest(SlotBase):
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    flight_type: Optional[str] = None
    duration: Optional[str] = None
    gapAfter: Optional[str] = None


class SlotResponse(SlotBase):
    id: int
    startTime: datetime
    endTime: datetime
    flight_type: str
    duration: str
    gapAfter: str
