from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class JoinRequestStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Permission(Enum):
    INVITE = "invite"
    KICK = "kick"

class Role(Enum):
    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"

@dataclass
class JoinRequest:
    id: str
    userId: str
    groupId: str
    status: JoinRequestStatus = JoinRequestStatus.PENDING
    createdAt: str = ""

@dataclass
class GroupMembership:
    id: str
    userId: str
    groupId: str
    role: Role = Role.MEMBER
    joinedAt: str = ""

    def isAdmin(self) -> bool:
        return self.role in (Role.ADMIN, Role.OWNER)

@dataclass
class GroupMembershipId:
    value: str

@dataclass
class GroupMembershipCreatedEvent:
    membershipId: str

@dataclass
class GroupMembershipUpdatedEvent:
    membershipId: str
