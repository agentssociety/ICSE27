from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
if TYPE_CHECKING:
    from src.domain.user import User

class PostState(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Permission(Enum):
    READ = "read"
    WRITE = "write"

class Role(Enum):
    OWNER = "owner"
    VIEWER = "viewer"

@dataclass
class Image:
    url: str
    altText: str = ""

@dataclass
class Post:
    id: str
    authorId: str
    textContent: str
    images: list[Image] = field(default_factory=list)
    state: PostState = PostState.PUBLISHED
    createdAt: str = ""
    updatedAt: str = ""
    tags: list[str] = field(default_factory=list)

    def canEdit(self, userId: str) -> bool:
        return self.authorId == userId

    def archive(self) -> None:
        self.state = PostState.ARCHIVED

@dataclass
class PostId:
    value: str

@dataclass
class PostCreatedEvent:
    postId: str
    authorId: str

@dataclass
class PostUpdatedEvent:
    postId: str
