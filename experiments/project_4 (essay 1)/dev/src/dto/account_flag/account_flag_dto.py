from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AccountFlagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccountFlagCreate(AccountFlagBase):
    account_id: Optional[int] = None
    transaction_id: Optional[str] = None


class AccountFlagUpdate(AccountFlagBase):
    account_id: Optional[int] = None
    transaction_id: Optional[str] = None


class AccountFlagResponse(AccountFlagBase):
    id: int
    account_id: Optional[int] = None
    transaction_id: Optional[str] = None
