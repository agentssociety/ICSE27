from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    content: str


class CommentUpdate(CommentBase):
    content: Optional[str] = None


class CommentResponse(CommentBase):
    id: int
    content: str
