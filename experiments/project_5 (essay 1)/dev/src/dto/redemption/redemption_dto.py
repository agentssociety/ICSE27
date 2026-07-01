from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RedemptionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RedemptionCreate(RedemptionBase):
    student_id: int
    reward_item_id: int
    nuggets_spent: float


class RedemptionUpdate(RedemptionBase):
    pass


class RedemptionResponse(RedemptionBase):
    id: int
    student_id: int
    reward_item_id: int
    nuggets_spent: float
    redeemed_at: Optional[datetime] = None
