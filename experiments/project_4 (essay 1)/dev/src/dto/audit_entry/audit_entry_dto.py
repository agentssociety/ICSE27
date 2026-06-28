from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AuditEntryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditEntryCreate(AuditEntryBase):
    operation_id: int
    recordedBy_id: int


class AuditEntryUpdate(AuditEntryBase):
    operation_id: Optional[int] = None
    recordedBy_id: Optional[int] = None


class AuditEntryResponse(AuditEntryBase):
    id: int
    operation_id: Optional[int] = None
    recordedBy_id: Optional[int] = None
