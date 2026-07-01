from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class NotificationType(Enum):
    LIKE = "like"
    COMMENT = "comment"
    FRIEND_REQUEST = "friend_request"
    SYSTEM = "system"

class ChannelType(Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    PUSH = "push"

class NotificationState(Enum):
    UNREAD = "unread"
    READ = "read"

@dataclass
class Notification:
    id: str
    userId: str
    type: NotificationType
    title: str
    message: str
    state: NotificationState = NotificationState.UNREAD
    channel: ChannelType = ChannelType.IN_APP
    referenceId: str = ""
    createdAt: str = ""

    def markAsRead(self) -> None:
        self.state = NotificationState.READ

@dataclass
class NotificationId:
    value: str

@dataclass
class NotificationCreatedEvent:
    notificationId: str

@dataclass
class NotificationUpdatedEvent:
    notificationId: str
