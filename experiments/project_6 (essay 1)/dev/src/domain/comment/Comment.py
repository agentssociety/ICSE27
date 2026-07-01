from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass
from datetime import time
from enum import Enum

if TYPE_CHECKING:
    from src.domain.post import Post
    from src.domain.user import User

"""
Domain layer for the Comment domain class

Package: domain.comment
Layer: domain
Related tasks: #161, #169
Requirement coverage:
- Add, edit, and delete comments on posts
- User receives notification on post interactions
"""

@dataclass
class Resource:
    owner: User
    accessible: list[User]

@dataclass
class Comment:
    owner: User
    content: str
    post: Post

class Role(Enum):
    CONTENT_AUTHORS = "content_authors"
    COMMUNITY_MANAGERS = "community_managers"
    END_USERS = "end_users"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    INVARIANTS = "invariants"
    READ_WRITE_ADMIN = "read_write_admin"

class State(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST2 = "post2"
    POST3 = "post3"
    INVARIANTS = "invariants"

@dataclass
class CommentId:
    pass

@dataclass
class CommentCreatedEvent:
    pass

@dataclass
class CommentUpdatedEvent:
    pass
