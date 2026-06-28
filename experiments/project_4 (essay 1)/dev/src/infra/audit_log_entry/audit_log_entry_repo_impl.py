from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.audit_log_entry.audit_log_entry_dto import (
    AuditLogEntryCreate,
    AuditLogEntryUpdate,
    AuditLogEntryResponse,
)


class SQLAlchemyAuditLogEntryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AuditLogEntryResponse]:
        from src.orm.audit_log_entry.audit_log_entry_orm import AuditLogEntryORM

        row = self._session.get(AuditLogEntryORM, item_id)
        return AuditLogEntryResponse.model_validate(row) if row else None

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> list[AuditLogEntryResponse]:
        from src.orm.audit_log_entry.audit_log_entry_orm import AuditLogEntryORM

        rows = self._session.query(AuditLogEntryORM).offset(skip).limit(limit).all()
        return [AuditLogEntryResponse.model_validate(r) for r in rows]

    def create(self, data: AuditLogEntryCreate) -> AuditLogEntryResponse:
        from src.orm.audit_log_entry.audit_log_entry_orm import AuditLogEntryORM

        row = AuditLogEntryORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AuditLogEntryResponse.model_validate(row)

    def update(
        self, item_id: int, data: AuditLogEntryUpdate
    ) -> Optional[AuditLogEntryResponse]:
        from src.orm.audit_log_entry.audit_log_entry_orm import AuditLogEntryORM

        row = self._session.get(AuditLogEntryORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AuditLogEntryResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        from src.orm.audit_log_entry.audit_log_entry_orm import AuditLogEntryORM

        row = self._session.get(AuditLogEntryORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True