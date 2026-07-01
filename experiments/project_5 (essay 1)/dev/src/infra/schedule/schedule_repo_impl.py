from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.schedule.schedule_dto import ScheduleCreateRequest, ScheduleUpdateRequest, ScheduleResponse
from src.orm.schedule.schedule_orm import ScheduleORM


class SQLAlchemyScheduleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ScheduleResponse]:
        row = self._session.get(ScheduleORM, item_id)
        return ScheduleResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ScheduleResponse]:
        rows = self._session.query(ScheduleORM).offset(skip).limit(limit).all()
        return [ScheduleResponse.model_validate(r) for r in rows]

    def create(self, data: ScheduleCreateRequest) -> ScheduleResponse:
        row = ScheduleORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ScheduleResponse.model_validate(row)

    def update(self, item_id: int, data: ScheduleUpdateRequest) -> Optional[ScheduleResponse]:
        row = self._session.get(ScheduleORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ScheduleResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ScheduleORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
