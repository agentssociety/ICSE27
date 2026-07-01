from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class FriendRequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class OnlineStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class NotificationType(Enum):
    FRIEND_REQUEST = "friend_request"
    FRIEND_ACCEPTED = "friend_accepted"

@dataclass
class FriendRequest:
    fromUserId: str
    toUserId: str
    status: FriendRequestStatus = FriendRequestStatus.PENDING
    createdAt: str = ""

@dataclass
class Friendship:
    id: str
    userId: str
    friendId: str
    status: FriendRequestStatus = FriendRequestStatus.PENDING
    createdAt: str = ""

@dataclass
class FriendshipId:
    value: str

@dataclass
class FriendshipCreatedEvent:
    friendshipId: str

@dataclass
class FriendshipUpdatedEvent:
    friendshipId: str
