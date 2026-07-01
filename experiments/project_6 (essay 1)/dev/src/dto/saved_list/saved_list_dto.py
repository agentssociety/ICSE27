from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class SavedListBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SavedListCreate(SavedListBase):
    userId: str


class SavedListUpdate(SavedListBase):
    userId: Optional[str] = None


class SavedListResponse(SavedListBase):
    userId: str
    userId: str
