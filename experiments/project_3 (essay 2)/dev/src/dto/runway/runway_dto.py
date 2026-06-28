from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class RunwayBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RunwayCreate(RunwayBase):
    runwayId: str
    length: Optional[int] = 3000
    timeSlot: Optional[Any] = None


class RunwayUpdate(RunwayBase):
    runwayId: Optional[str] = None
    length: Optional[int] = None
    timeSlot: Optional[Any] = None


class RunwayResponse(RunwayBase):
    id: int
    runwayId: str
    length: int
    timeSlot: Optional[Any] = None
