from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict

"""
Dto layer for the Card domain class

Package: dto.card
Layer: dto
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""


class CardCreateRequest(BaseModel):
    user_id: str
    card_number: str


class CardUpdateRequest(BaseModel):
    card_number: Optional[str] = None


class CardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    card_number: str
