from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class Permission(Enum):
    GRANT = "grant"
    REVOKE = "revoke"
    VIEW = "view"

class AuditAction(Enum):
    GRANTED = "granted"
    REVOKED = "revoked"

@dataclass
class UserProfile:
    userId: str
    displayName: str

@dataclass
class Admin:
    userId: str
    permissions: list[Permission]

    def canGrantBadge(self) -> bool:
        return Permission.GRANT in self.permissions

@dataclass
class AuditEntry:
    action: AuditAction
    adminId: str
    targetUserId: str
    timestamp: str = ""

@dataclass
class VerifiedBadge:
    id: str
    userId: str
    grantedBy: str
    grantedAt: str = ""
    active: bool = True

@dataclass
class VerifiedBadgeId:
    value: str

@dataclass
class VerifiedBadgeCreatedEvent:
    badgeId: str

@dataclass
class VerifiedBadgeUpdatedEvent:
    badgeId: str
