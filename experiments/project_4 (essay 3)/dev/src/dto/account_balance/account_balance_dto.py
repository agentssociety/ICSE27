from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AccountBalanceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccountBalanceCreate(AccountBalanceBase):
    pass


class AccountBalanceUpdate(AccountBalanceBase):
    pass


class AccountBalanceResponse(AccountBalanceBase):
    id: int
    pass
