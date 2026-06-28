from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class WithdrawalRecordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WithdrawalRecordCreate(WithdrawalRecordBase):
    transaction_id: str
    amount_id: int


class WithdrawalRecordUpdate(WithdrawalRecordBase):
    transaction_id: Optional[str] = None
    amount_id: Optional[int] = None


class WithdrawalRecordResponse(WithdrawalRecordBase):
    id: int
    transaction_id: str
    amount_id: Optional[int] = None
