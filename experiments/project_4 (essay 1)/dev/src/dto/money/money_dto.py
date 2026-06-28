from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class MoneyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MoneyCreate(MoneyBase):
    amount: float
    currency: Optional[str] = 'USD'


class MoneyUpdate(MoneyBase):
    amount: Optional[float] = None
    currency: Optional[str] = None


class MoneyResponse(MoneyBase):
    id: int
    amount: float
    currency: str
