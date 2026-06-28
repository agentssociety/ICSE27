from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CardCreate(CardBase):
    cardNumber: str
    user_id: int
    authenticationAttempt_id: int


class CardUpdate(CardBase):
    cardNumber: Optional[str] = None
    user_id: Optional[int] = None
    authenticationAttempt_id: Optional[int] = None


class CardResponse(CardBase):
    id: int
    cardNumber: str
    user_id: Optional[int] = None
    authenticationAttempt_id: Optional[int] = None
