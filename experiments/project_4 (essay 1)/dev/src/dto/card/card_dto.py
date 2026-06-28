from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CardCreate(CardBase):
    owner_id: int
    expiryDate: Optional[str] = None


class CardUpdate(CardBase):
    owner_id: Optional[int] = None
    expiryDate: Optional[str] = None


class CardResponse(CardBase):
    id: int
    owner_id: Optional[int] = None
    expiryDate: Optional[str] = None
