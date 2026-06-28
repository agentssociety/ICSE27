from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BloodUnitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BloodUnitCreate(BloodUnitBase):
    uniqueID: str
    aboType: str
    rhFactor: str
    collectionDate: date


class BloodUnitUpdate(BloodUnitBase):
    uniqueID: Optional[str] = None
    aboType: Optional[str] = None
    rhFactor: Optional[str] = None
    collectionDate: Optional[date] = None
    status: Optional[str] = None


class BloodUnitResponse(BloodUnitBase):
    id: int
    uniqueID: str
    aboType: str
    rhFactor: str
    collectionDate: date
    expiryDate: date
    status: str
