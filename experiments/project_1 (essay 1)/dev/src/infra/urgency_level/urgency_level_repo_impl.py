from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from src.dto.urgency_level.urgency_level_dto import UrgencyLevelCreateRequest, UrgencyLevelUpdateRequest, UrgencyLevelResponse
from src.orm.urgency_level.urgency_level_orm import UrgencyLevelORM

"""
Infra layer for the UrgencyLevel domain class

Package: infra.urgency_level
Layer: infra
Related tasks: #2, #3, #4, #6
Requirement coverage:
- Assign urgency level to patients based on symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Real-time Patient Dashboard
"""


class SQLAlchemyUrgencyLevelRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[UrgencyLevelResponse]:
        row = self._session.get(UrgencyLevelORM, item_id)
        return UrgencyLevelResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UrgencyLevelResponse]:
        rows = self._session.query(UrgencyLevelORM).offset(skip).limit(limit).all()
        return [UrgencyLevelResponse.model_validate(r) for r in rows]

    def create(self, data: UrgencyLevelCreateRequest) -> UrgencyLevelResponse:
        row = UrgencyLevelORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UrgencyLevelResponse.model_validate(row)

    def update(self, item_id: int, data: UrgencyLevelUpdateRequest) -> Optional[UrgencyLevelResponse]:
        row = self._session.get(UrgencyLevelORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return UrgencyLevelResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(UrgencyLevelORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
