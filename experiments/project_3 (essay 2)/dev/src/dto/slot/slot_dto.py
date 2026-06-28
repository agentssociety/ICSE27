from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class SlotBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SlotCreate(SlotBase):
    flight_id: int
    runway_id: int


class SlotUpdate(SlotBase):
    flight_id: Optional[int] = None
    runway_id: Optional[int] = None


class SlotResponse(SlotBase):
    id: int
    flight_id: Optional[int] = None
    runway_id: Optional[int] = None
