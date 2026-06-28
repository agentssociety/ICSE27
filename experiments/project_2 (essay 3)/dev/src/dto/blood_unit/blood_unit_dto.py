from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BloodUnitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BloodUnitCreate(BloodUnitBase):
    abo_rh_type: str
    collection_date: date


class BloodUnitUpdate(BloodUnitBase):
    abo_rh_type: Optional[str] = None
    collection_date: Optional[date] = None
    is_expired: Optional[bool] = None


class BloodUnitResponse(BloodUnitBase):
    id: int
    abo_rh_type: str
    collection_date: date
    is_expired: bool = False

