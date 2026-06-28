from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class AlternativeRunwayBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AlternativeRunwayCreate(AlternativeRunwayBase):
    runway_id: int
    isAvailable: Optional[bool] = True


class AlternativeRunwayUpdate(AlternativeRunwayBase):
    runway_id: Optional[int] = None
    isAvailable: Optional[bool] = None


class AlternativeRunwayResponse(AlternativeRunwayBase):
    id: int
    runway_id: Optional[int] = None
    isAvailable: bool
