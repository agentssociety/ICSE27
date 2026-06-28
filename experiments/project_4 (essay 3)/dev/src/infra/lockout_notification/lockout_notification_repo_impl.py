from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.lockout_notification.lockout_notification_dto import LockoutNotificationCreate, LockoutNotificationUpdate, LockoutNotificationResponse
from src.orm.lockout_notification.lockout_notification_orm import LockoutNotificationORM


class SQLAlchemyLockoutNotificationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[LockoutNotificationResponse]:
        row = self._session.get(LockoutNotificationORM, item_id)
        return LockoutNotificationResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LockoutNotificationResponse]:
        rows = self._session.query(LockoutNotificationORM).offset(skip).limit(limit).all()
        return [LockoutNotificationResponse.model_validate(r) for r in rows]

    def create(self, data: LockoutNotificationCreate) -> LockoutNotificationResponse:
        row = LockoutNotificationORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return LockoutNotificationResponse.model_validate(row)

    def update(self, item_id: int, data: LockoutNotificationUpdate) -> Optional[LockoutNotificationResponse]:
        row = self._session.get(LockoutNotificationORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return LockoutNotificationResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(LockoutNotificationORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
