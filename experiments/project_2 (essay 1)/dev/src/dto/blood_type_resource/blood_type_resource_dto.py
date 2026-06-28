from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BloodTypeResourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BloodTypeResourceCreate(BloodTypeResourceBase):
    bloodType: str
    units: int


class BloodTypeResourceUpdate(BloodTypeResourceBase):
    bloodType: Optional[str] = None
    units: Optional[int] = None


class BloodTypeResourceResponse(BloodTypeResourceBase):
    id: int
    bloodType: str
    units: int
