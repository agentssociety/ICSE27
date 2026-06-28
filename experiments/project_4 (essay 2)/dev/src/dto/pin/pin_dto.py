from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict

"""
Dto layer for the Pin domain class

Package: dto.pin
Layer: dto
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""


class PinCreateRequest(BaseModel):
    user_id: str
    pin_code: str


class PinUpdateRequest(BaseModel):
    pin_code: Optional[str] = None


class PinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    pin_code: str
