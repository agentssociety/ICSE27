from __future__ import annotations

from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogEntryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditLogEntryCreate(AuditLogEntryBase):
    operation: str
    timestamp: datetime
    username: str
    ip_address: str
    outcome: str
    user_id: Optional[str] = None
    account_id: Optional[int] = None
    action_type: Optional[str] = None


class AuditLogEntryUpdate(AuditLogEntryBase):
    operation: Optional[str] = None
    timestamp: Optional[datetime] = None
    username: Optional[str] = None
    ip_address: Optional[str] = None
    outcome: Optional[str] = None
    user_id: Optional[str] = None
    account_id: Optional[int] = None
    action_type: Optional[str] = None


class AuditLogEntryResponse(AuditLogEntryBase):
    user_id: str
    operation: str
    timestamp: datetime
    username: str
    ip_address: str
    outcome: str
    user_id: Optional[str] = None
    account_id: Optional[int] = None
    action_type: Optional[str] = None
