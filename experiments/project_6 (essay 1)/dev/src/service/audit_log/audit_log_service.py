from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.audit_log.audit_log_dto import AuditLogCreate, AuditLogUpdate, AuditLogResponse

if TYPE_CHECKING:
    from src.infra.audit_log.audit_log_repo_impl import SQLAlchemyAuditLogRepository


class AuditLogService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[AuditLogResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuditLogResponse]: ...
    def create(self, data: AuditLogCreate) -> AuditLogResponse: ...
    def update(self, item_id: int, data: AuditLogUpdate) -> Optional[AuditLogResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class AuditLogServiceImpl:
    def __init__(self, repo: SQLAlchemyAuditLogRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[AuditLogResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuditLogResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: AuditLogCreate) -> AuditLogResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: AuditLogUpdate) -> Optional[AuditLogResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

