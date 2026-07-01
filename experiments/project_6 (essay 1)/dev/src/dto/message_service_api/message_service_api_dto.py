from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class Message_Service_APIBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Message_Service_APICreate(Message_Service_APIBase):
    pass


class Message_Service_APIUpdate(Message_Service_APIBase):
    pass


class Message_Service_APIResponse(Message_Service_APIBase):
    id: int
    pass
