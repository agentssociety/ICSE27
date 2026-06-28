from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AuthenticationSessionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuthenticationSessionCreate(AuthenticationSessionBase):
    sessionId: str
    user_id: int
    card_id: int


class AuthenticationSessionUpdate(AuthenticationSessionBase):
    sessionId: Optional[str] = None
    user_id: Optional[int] = None
    card_id: Optional[int] = None


class AuthenticationSessionResponse(AuthenticationSessionBase):
    id: int
    sessionId: str
    user_id: Optional[int] = None
    card_id: Optional[int] = None
