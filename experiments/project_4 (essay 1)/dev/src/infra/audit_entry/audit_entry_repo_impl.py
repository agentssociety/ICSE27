from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.audit_entry.audit_entry_dto import AuditEntryCreate, AuditEntryUpdate, AuditEntryResponse
from src.orm.audit_entry.audit_entry_orm import AuditEntryORM


class SQLAlchemyAuditEntryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AuditEntryResponse]:
        row = self._session.get(AuditEntryORM, item_id)
        return AuditEntryResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuditEntryResponse]:
        rows = self._session.query(AuditEntryORM).offset(skip).limit(limit).all()
        return [AuditEntryResponse.model_validate(r) for r in rows]

    def create(self, data: AuditEntryCreate) -> AuditEntryResponse:
        row = AuditEntryORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AuditEntryResponse.model_validate(row)

    def update(self, item_id: int, data: AuditEntryUpdate) -> Optional[AuditEntryResponse]:
        row = self._session.get(AuditEntryORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AuditEntryResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AuditEntryORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True