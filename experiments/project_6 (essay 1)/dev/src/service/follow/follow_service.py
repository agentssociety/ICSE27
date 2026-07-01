from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.repository.follow import FollowUnfollowAPI, UserProfileDatabase

"""
Service layer for the Follow domain class

Package: service.follow
Layer: service
Related tasks: #164
Requirement coverage:
- User Follow/Unfollow Functionality
"""

class FollowUnfollowService(Protocol):
    ...
