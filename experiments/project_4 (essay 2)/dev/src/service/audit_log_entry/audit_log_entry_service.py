from __future__ import annotations

from typing import Any, Optional, Protocol
from datetime import datetime

from src.dto.audit_log_entry.audit_log_entry_dto import AuditLogEntryCreate, AuditLogEntryUpdate, AuditLogEntryResponse

"""
Service layer for the AuditLogEntry domain class

Package: service.audit_log_entry
Layer: service
Related tasks: None
"""


class AuditLogEntryService(Protocol):
    def create_entry(self, data: AuditLogEntryCreate) -> AuditLogEntryResponse: ...
    def get_entry(self, entry_id: int) -> Optional[AuditLogEntryResponse]: ...
    def get_all_entries(self, skip: int = 0, limit: int = 100) -> list[AuditLogEntryResponse]: ...


class AuditLogEntryServiceImpl:
    def __init__(self, repository: Any) -> None:
        self._repository = repository

    def create_entry(self, data: AuditLogEntryCreate) -> AuditLogEntryResponse:
        # Ensure timestamp is set
        if not data.timestamp:
            data.timestamp = datetime.utcnow().isoformat()
        return self._repository.create(data)

    def get_entry(self, entry_id: int) -> Optional[AuditLogEntryResponse]:
        return self._repository.get_by_id(entry_id)

    def get_all_entries(self, skip: int = 0, limit: int = 100) -> list[AuditLogEntryResponse]:
        return self._repository.get_all(skip=skip, limit=limit)
