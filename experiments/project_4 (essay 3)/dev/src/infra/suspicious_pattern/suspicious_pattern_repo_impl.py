from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.suspicious_pattern.suspicious_pattern_dto import SuspiciousPatternCreate, SuspiciousPatternUpdate, SuspiciousPatternResponse
from src.orm.suspicious_pattern.suspicious_pattern_orm import SuspiciousPatternORM


class SQLAlchemySuspiciousPatternRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SuspiciousPatternResponse]:
        row = self._session.get(SuspiciousPatternORM, item_id)
        return SuspiciousPatternResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SuspiciousPatternResponse]:
        rows = self._session.query(SuspiciousPatternORM).offset(skip).limit(limit).all()
        return [SuspiciousPatternResponse.model_validate(r) for r in rows]

    def create(self, data: SuspiciousPatternCreate) -> SuspiciousPatternResponse:
        row = SuspiciousPatternORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SuspiciousPatternResponse.model_validate(row)

    def update(self, item_id: int, data: SuspiciousPatternUpdate) -> Optional[SuspiciousPatternResponse]:
        row = self._session.get(SuspiciousPatternORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SuspiciousPatternResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SuspiciousPatternORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
