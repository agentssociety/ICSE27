from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuditLogEntryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditLogEntryCreate(AuditLogEntryBase):
    eventType: str
    userId: str
    sourceIp: str
    outcome: str


class AuditLogEntryUpdate(AuditLogEntryBase):
    eventType: Optional[str] = None
    userId: Optional[str] = None
    sourceIp: Optional[str] = None
    outcome: Optional[str] = None


class AuditLogEntryResponse(AuditLogEntryBase):
    userId: str
    eventType: str
    userId: str
    sourceIp: str
    outcome: str
