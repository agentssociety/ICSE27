from __future__ import annotations

from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator


class WithdrawalTransactionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WithdrawalCreateRequest(WithdrawalTransactionBase):
    account_id: str
    amount: Decimal

    @field_validator('amount')
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= Decimal('0'):
            raise ValueError('Withdrawal amount must be greater than 0')
        return v

    @field_validator('account_id')
    @classmethod
    def account_id_required(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('account_id is required')
        return v


class WithdrawalResponse(WithdrawalTransactionBase):
    id: str
    account_id: str
    amount: Decimal
    status: str
    timestamp: datetime


class WithdrawalListResponse(WithdrawalTransactionBase):
    items: list[WithdrawalResponse]
    total: int
