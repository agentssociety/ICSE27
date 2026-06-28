from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class UserAccountBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserAccountCreate(UserAccountBase):
    pass


class UserAccountUpdate(UserAccountBase):
    pass


class UserAccountResponse(UserAccountBase):
    id: int
    pass
