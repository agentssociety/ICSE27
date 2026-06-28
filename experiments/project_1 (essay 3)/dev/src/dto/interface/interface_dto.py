from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class InterfaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class InterfaceCreate(InterfaceBase):
    pass


class InterfaceUpdate(InterfaceBase):
    pass


class InterfaceResponse(InterfaceBase):
    id: int
    pass
