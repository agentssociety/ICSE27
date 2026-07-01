from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.audit_event.audit_event_dto import AuditEventCreate, AuditEventResponse
from src.orm.audit_event.audit_event_orm import AuditEventORM


class SQLAlchemyAuditEventRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AuditEventResponse]:
        row = self._session.get(AuditEventORM, item_id)
        return AuditEventResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuditEventResponse]:
        rows = self._session.query(AuditEventORM).order_by(AuditEventORM.timestamp.desc()).offset(skip).limit(limit).all()
        return [AuditEventResponse.model_validate(r) for r in rows]

    def create(self, data: AuditEventCreate) -> AuditEventResponse:
        row = AuditEventORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AuditEventResponse.model_validate(row)
