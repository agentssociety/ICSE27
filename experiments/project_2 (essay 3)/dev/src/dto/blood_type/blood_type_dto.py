from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BloodTypeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BloodTypeCreate(BloodTypeBase):
    bloodUnit_id: int
    transfusionRequest_id: int


class BloodTypeUpdate(BloodTypeBase):
    bloodUnit_id: Optional[int] = None
    transfusionRequest_id: Optional[int] = None


class BloodTypeResponse(BloodTypeBase):
    id: int
    bloodUnit_id: Optional[int] = None
    transfusionRequest_id: Optional[int] = None
