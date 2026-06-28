from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class TransactionLogBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TransactionLogCreate(TransactionLogBase):
    logRecord: str


class TransactionLogUpdate(TransactionLogBase):
    logRecord: Optional[str] = None


class TransactionLogResponse(TransactionLogBase):
    id: int
    logRecord: str
