from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.post import Post

"""
Repository layer for the Post domain class

Package: repository.post
Layer: repository
Related tasks: #159, #160, #161, #162, #167, #169, #170, #171, #172, #178
Requirement coverage:
- User can create a text post and optionally upload images
- User can like and unlike a post
- Add, edit, and delete comments on posts
- Display News Feed Sorted by Time
- Group Post Feed Filter
"""

class ContentDatabase(Protocol):
    def save(self, post: Post) -> None:
        ...

class ImageStorageService(Protocol):
    ...
