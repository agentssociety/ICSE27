from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AircraftBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AircraftCreate(AircraftBase):
    type: str
    size: str


class AircraftUpdate(AircraftBase):
    type: Optional[str] = None
    size: Optional[str] = None


class AircraftResponse(AircraftBase):
    id: int
    type: str
    size: str
