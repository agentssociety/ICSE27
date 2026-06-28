from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogResourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditLogResourceCreate(AuditLogResourceBase):
    resourceId: UUID


class AuditLogResourceUpdate(AuditLogResourceBase):
    resourceId: Optional[UUID] = None


class AuditLogResourceResponse(AuditLogResourceBase):
    id: int
    resourceId: UUID
