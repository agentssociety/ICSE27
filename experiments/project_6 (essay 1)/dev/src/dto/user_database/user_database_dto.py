from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class User_DatabaseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User_DatabaseCreate(User_DatabaseBase):
    pass


class User_DatabaseUpdate(User_DatabaseBase):
    pass


class User_DatabaseResponse(User_DatabaseBase):
    id: int
    pass
