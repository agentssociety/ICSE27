from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccountCreateRequest(AccountBase):
    account_id: str
    balance: float = 0.0
    locked: bool = False
    failed_attempt_count: int = 0


class AccountUpdateRequest(AccountBase):
    account_id: Optional[str] = None
    balance: Optional[float] = None
    locked: Optional[bool] = None
    failed_attempt_count: Optional[int] = None


class AccountResponse(AccountBase):
    id: int
    account_id: str
    balance: float
    locked: bool
    failed_attempt_count: int
