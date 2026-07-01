from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AuditLogBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditLogCreate(AuditLogBase):
    adminId: str
    actionType: str
    targetUserId: str


class AuditLogUpdate(AuditLogBase):
    adminId: Optional[str] = None
    actionType: Optional[str] = None
    targetUserId: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    id: int
    adminId: str
    actionType: str
    targetUserId: str
