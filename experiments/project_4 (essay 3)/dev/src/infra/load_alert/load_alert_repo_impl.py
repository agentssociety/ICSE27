from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.load_alert.load_alert_dto import LoadAlertCreate, LoadAlertUpdate, LoadAlertResponse
from src.orm.load_alert.load_alert_orm import LoadAlertORM


class SQLAlchemyLoadAlertRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[LoadAlertResponse]:
        row = self._session.get(LoadAlertORM, item_id)
        return LoadAlertResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LoadAlertResponse]:
        rows = self._session.query(LoadAlertORM).offset(skip).limit(limit).all()
        return [LoadAlertResponse.model_validate(r) for r in rows]

    def create(self, data: LoadAlertCreate) -> LoadAlertResponse:
        row = LoadAlertORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return LoadAlertResponse.model_validate(row)

    def update(self, item_id: int, data: LoadAlertUpdate) -> Optional[LoadAlertResponse]:
        row = self._session.get(LoadAlertORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return LoadAlertResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(LoadAlertORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
