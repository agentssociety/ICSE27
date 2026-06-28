from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class InterfaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class InterfaceCreate(InterfaceBase):
    kind: str
    encrypted: bool
    authenticated: bool


class InterfaceUpdate(InterfaceBase):
    kind: Optional[str] = None
    encrypted: Optional[bool] = None
    authenticated: Optional[bool] = None


class InterfaceResponse(InterfaceBase):
    id: int
    kind: str
    encrypted: bool
    authenticated: bool
