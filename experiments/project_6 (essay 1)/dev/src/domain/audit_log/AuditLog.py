from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Operation(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SOFT_DELETE = "soft_delete"
    RECOVER = "recover"

class Permission(Enum):
    VIEW = "view"
    EXPORT = "export"

class State(Enum):
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Admin:
    userId: str

@dataclass
class Resource:
    type: str
    id: str

@dataclass
class AuditLog:
    id: str
    userId: str
    action: Operation
    resource: str
    resourceId: str
    details: str = ""
    state: State = State.COMPLETED
    timestamp: str = ""

@dataclass
class AuditLogId:
    value: str

@dataclass
class AuditLogCreatedEvent:
    auditLogId: str

@dataclass
class AuditLogUpdatedEvent:
    auditLogId: str
