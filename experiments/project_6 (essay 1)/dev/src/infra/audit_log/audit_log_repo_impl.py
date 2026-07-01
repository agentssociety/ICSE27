from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.audit_log.audit_log_dto import AuditLogCreate, AuditLogUpdate, AuditLogResponse
from src.orm.audit_log.audit_log_orm import AuditLogORM


class SQLAlchemyAuditLogRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AuditLogResponse]:
        row = self._session.get(AuditLogORM, item_id)
        return AuditLogResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuditLogResponse]:
        rows = self._session.query(AuditLogORM).offset(skip).limit(limit).all()
        return [AuditLogResponse.model_validate(r) for r in rows]

    def create(self, data: AuditLogCreate) -> AuditLogResponse:
        row = AuditLogORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AuditLogResponse.model_validate(row)

    def update(self, item_id: int, data: AuditLogUpdate) -> Optional[AuditLogResponse]:
        row = self._session.get(AuditLogORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AuditLogResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AuditLogORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
