from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime

if TYPE_CHECKING:
    from src.domain.user import User

"""
Domain layer for the AuditLogEntry domain class

Package: domain.audit_log_entry
Layer: domain
Related tasks: None
"""


@dataclass
class AuditLogEntry:
    eventType: str
    timestamp: datetime
    userId: str
    sourceIp: str
    outcome: str
    user: Optional[User] = None

    def createEntry(self, eventType: str, timestamp: datetime, userId: str, sourceIp: str, outcome: str) -> AuditLogEntry:
        return AuditLogEntry(
            eventType=eventType,
            timestamp=timestamp,
            userId=userId,
            sourceIp=sourceIp,
            outcome=outcome,
        )


@dataclass
class AuditLogEntryId:
    pass


@dataclass
class AuditLogEntryCreatedEvent:
    pass


@dataclass
class AuditLogEntryUpdatedEvent:
    pass
