from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class InterfaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class InterfaceCreate(InterfaceBase):
    name: str
    description: str
    securityRequirements: str


class InterfaceUpdate(InterfaceBase):
    name: Optional[str] = None
    description: Optional[str] = None
    securityRequirements: Optional[str] = None


class InterfaceResponse(InterfaceBase):
    id: int
    name: str
    description: str
    securityRequirements: str
