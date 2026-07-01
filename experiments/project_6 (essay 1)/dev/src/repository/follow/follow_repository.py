from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the Follow domain class

Package: repository.follow
Layer: repository
Related tasks: #164
Requirement coverage:
- User Follow/Unfollow Functionality
"""

class FollowUnfollowAPI(Protocol):
    ...

class UserProfileDatabase(Protocol):
    ...
