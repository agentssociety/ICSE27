from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.user import User

"""
Domain layer for the NotificationPreference domain class

Package: domain.notification_preference
Layer: domain
Related tasks: #176
Requirement coverage:
- Enable/Disable Notifications per Category
"""

@dataclass
class NotificationPreference:
    userId: str
    category: NotificationCategory
    enabled: bool
    user: User

class NotificationCategory(Enum):
    LIKES = "likes"
    COMMENTS = "comments"
    FRIEND_REQUESTS = "friend_requests"

class Permission(Enum):
    READ_OWN_SETTINGS = "read_own_settings"
    WRITE_OWN_SETTINGS = "write_own_settings"

class UserState(Enum):
    LOGGED_IN = "logged_in"
    TOGGLING = "toggling"
    POST_TOGGLE = "post_toggle"

@dataclass
class NotificationPreferenceId:
    pass

@dataclass
class NotificationPreferenceCreatedEvent:
    pass

@dataclass
class NotificationPreferenceUpdatedEvent:
    pass
