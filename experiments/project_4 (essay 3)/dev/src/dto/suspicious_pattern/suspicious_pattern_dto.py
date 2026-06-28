from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class SuspiciousPatternBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SuspiciousPatternCreate(SuspiciousPatternBase):
    active: bool
    withdrawalTransaction_id: int


class SuspiciousPatternUpdate(SuspiciousPatternBase):
    active: Optional[bool] = None
    withdrawalTransaction_id: Optional[int] = None


class SuspiciousPatternResponse(SuspiciousPatternBase):
    id: int
    active: bool
    withdrawalTransaction_id: Optional[int] = None
