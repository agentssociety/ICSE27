from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class TransactionStateChangeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TransactionStateChangeCreate(TransactionStateChangeBase):
    pass


class TransactionStateChangeUpdate(TransactionStateChangeBase):
    pass


class TransactionStateChangeResponse(TransactionStateChangeBase):
    id: int
    pass
