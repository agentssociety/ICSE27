from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BookmarkBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BookmarkCreate(BookmarkBase):
    userId: str
    postId: str


class BookmarkUpdate(BookmarkBase):
    userId: Optional[str] = None
    postId: Optional[str] = None


class BookmarkResponse(BookmarkBase):
    userId: str
    userId: str
    postId: str
