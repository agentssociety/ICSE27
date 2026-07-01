from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditEntryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditEntryCreate(AuditEntryBase):
    operationId: UUID
    adminId: UUID
    targetUserId: UUID


class AuditEntryUpdate(AuditEntryBase):
    operationId: Optional[UUID] = None
    adminId: Optional[UUID] = None
    targetUserId: Optional[UUID] = None


class AuditEntryResponse(AuditEntryBase):
    id: int
    operationId: UUID
    adminId: UUID
    targetUserId: UUID
