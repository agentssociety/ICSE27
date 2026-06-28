from __future__ import annotations

import uuid
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TransactionCreate(TransactionBase):
    transaction_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    amount_id: int
    timestamp: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    status_id: int


class TransactionUpdate(TransactionBase):
    transaction_id: Optional[str] = None
    amount_id: Optional[int] = None
    timestamp: Optional[str] = None
    status_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    transaction_id: str
    amount_id: Optional[int] = None
    timestamp: str
    status_id: Optional[int] = None