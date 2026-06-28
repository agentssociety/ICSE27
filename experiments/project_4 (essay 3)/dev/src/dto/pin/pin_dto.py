from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PinBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PinCreate(PinBase):
    pass


class PinUpdate(PinBase):
    pass


class PinResponse(PinBase):
    id: int
    pass
