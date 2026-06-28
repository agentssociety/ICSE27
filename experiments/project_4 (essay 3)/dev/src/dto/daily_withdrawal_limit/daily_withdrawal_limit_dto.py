from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class DailyWithdrawalLimitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DailyWithdrawalLimitCreateRequest(DailyWithdrawalLimitBase):
    account_id: str
    daily_limit: float = 200.0
    used_today: float = 0.0


class DailyWithdrawalLimitUpdateRequest(DailyWithdrawalLimitBase):
    account_id: Optional[str] = None
    daily_limit: Optional[float] = None
    used_today: Optional[float] = None


class DailyWithdrawalLimitResponse(DailyWithdrawalLimitBase):
    id: int
    account_id: str
    daily_limit: float
    used_today: float
