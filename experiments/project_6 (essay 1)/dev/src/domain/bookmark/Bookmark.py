from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class LoginStatus(Enum):
    LOGGED_IN = "logged_in"
    LOGGED_OUT = "logged_out"

@dataclass
class SavedList:
    id: str
    userId: str
    name: str = "Saved"
    postIds: list[str] = field(default_factory=list)

    def addPost(self, postId: str) -> None:
        if postId not in self.postIds:
            self.postIds.append(postId)

    def removePost(self, postId: str) -> None:
        if postId in self.postIds:
            self.postIds.remove(postId)

@dataclass
class Bookmark:
    id: str
    userId: str
    postId: str
    createdAt: str = ""

@dataclass
class BookmarkId:
    value: str

@dataclass
class BookmarkCreatedEvent:
    bookmarkId: str

@dataclass
class BookmarkUpdatedEvent:
    bookmarkId: str
