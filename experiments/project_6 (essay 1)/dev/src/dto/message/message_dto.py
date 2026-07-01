from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    pass
