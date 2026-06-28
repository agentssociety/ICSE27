from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PINBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PINCreate(PINBase):
    owner_id: int
    user_id: int


class PINUpdate(PINBase):
    owner_id: Optional[int] = None
    user_id: Optional[int] = None


class PINResponse(PINBase):
    id: int
    owner_id: Optional[int] = None
    user_id: Optional[int] = None
