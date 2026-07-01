from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoleCreate(RoleBase):
    name: str


class RoleUpdate(RoleBase):
    name: Optional[str] = None


class RoleResponse(RoleBase):
    id: int
    name: str
