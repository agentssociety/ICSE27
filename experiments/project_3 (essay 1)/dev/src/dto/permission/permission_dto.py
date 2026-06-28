from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int
    pass
