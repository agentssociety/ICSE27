from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.repository.like import PostDatabase

"""
Service layer for the Like domain class

Package: service.like
Layer: service
Related tasks: #160, #169
Requirement coverage:
- User can like and unlike a post
- User receives notification on post interactions
"""

class LikeService(Protocol):
    ...
