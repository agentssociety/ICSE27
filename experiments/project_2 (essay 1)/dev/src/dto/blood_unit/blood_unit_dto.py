from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from typing import Optional


class BloodUnitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RecordBloodUnitRequest(BloodUnitBase):
    bloodType: str
    rhFactor: str
    donationDate: str


class BloodUnitResponse(BloodUnitBase):
    id: int
    bloodType: str
    rhFactor: str
    donationDate: str
    expirationDate: Optional[str] = None
    isExpiring: bool = False
