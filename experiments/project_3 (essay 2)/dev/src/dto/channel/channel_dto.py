from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChannelBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ChannelCreate(ChannelBase):
    channelId: str
    channelType: str


class ChannelUpdate(ChannelBase):
    channelId: Optional[str] = None
    channelType: Optional[str] = None


class ChannelResponse(ChannelBase):
    id: int
    channelId: str
    channelType: str
