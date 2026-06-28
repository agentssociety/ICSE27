from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class WithdrawalLimitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WithdrawalLimitCreate(WithdrawalLimitBase):
    pass


class WithdrawalLimitUpdate(WithdrawalLimitBase):
    pass


class WithdrawalLimitResponse(WithdrawalLimitBase):
    id: int
    pass
