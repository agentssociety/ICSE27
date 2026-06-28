from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class RunwayBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RunwayCreate(RunwayBase):
    flight_id: Optional[int] = None


class RunwayUpdate(RunwayBase):
    flight_id: Optional[int] = None


class RunwayResponse(RunwayBase):
    id: str
    flight_id: Optional[int] = None
