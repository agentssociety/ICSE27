from __future__ import annotations

from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PostCreateDTO(PostBase):
    authorId: str
    textContent: str


class PostUpdateDTO(PostBase):
    textContent: Optional[str] = None


class PostResponseDTO(PostBase):
    id: int
    authorId: str
    textContent: str


class CreatePostRequest(BaseModel):
    textContent: str
    images: List[bytes]


class CreatePostResponse(BaseModel):
    success: bool
    postId: str
