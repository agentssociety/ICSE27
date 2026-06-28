from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class WithdrawalRequestBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WithdrawalRequestCreate(WithdrawalRequestBase):
    pass


class WithdrawalRequestUpdate(WithdrawalRequestBase):
    pass


class WithdrawalRequestResponse(WithdrawalRequestBase):
    id: int
    pass
