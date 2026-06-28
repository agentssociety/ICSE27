from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccountCreate(AccountBase):
    failedAttempts: Optional[int] = 0
    balance: Optional[float] = 0.0
    daily_withdrawal_limit: Optional[float] = 1000.0
    withdrawn_today: Optional[float] = 0.0
    locked_reason: Optional[str] = None


class AccountUpdate(AccountBase):
    failedAttempts: Optional[int] = None
    balance: Optional[float] = None
    daily_withdrawal_limit: Optional[float] = None
    withdrawn_today: Optional[float] = None
    locked_reason: Optional[str] = None


class AccountResponse(AccountBase):
    id: int
    failedAttempts: int
    balance: float
    daily_withdrawal_limit: float
    withdrawn_today: float
    locked_reason: Optional[str] = None
