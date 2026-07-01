from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.streak.streak_dto import StreakCreate, StreakUpdate, StreakResponse
from src.orm.streak.streak_orm import StreakORM


class SQLAlchemyStreakRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[StreakResponse]:
        row = self._session.get(StreakORM, item_id)
        return StreakResponse.model_validate(row) if row else None

    def get_by_student_id(self, student_id: int) -> Optional[StreakResponse]:
        row = self._session.query(StreakORM).filter(StreakORM.student_id == student_id).first()
        return StreakResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[StreakResponse]:
        rows = self._session.query(StreakORM).offset(skip).limit(limit).all()
        return [StreakResponse.model_validate(r) for r in rows]

    def create(self, data: StreakCreate) -> StreakResponse:
        row = StreakORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return StreakResponse.model_validate(row)

    def update(self, item_id: int, data: StreakUpdate) -> Optional[StreakResponse]:
        row = self._session.get(StreakORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return StreakResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(StreakORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True

    def record_correct(self, student_id: int) -> Optional[StreakResponse]:
        row = self._session.query(StreakORM).filter(StreakORM.student_id == student_id).first()
        if row is None:
            return None
        row.current_streak = (row.current_streak or 0) + 1
        if row.current_streak > (row.longest_streak or 0):
            row.longest_streak = row.current_streak
        self._session.commit()
        self._session.refresh(row)
        return StreakResponse.model_validate(row)

    def record_wrong(self, student_id: int) -> Optional[StreakResponse]:
        row = self._session.query(StreakORM).filter(StreakORM.student_id == student_id).first()
        if row is None:
            return None
        row.current_streak = 0
        self._session.commit()
        self._session.refresh(row)
        return StreakResponse.model_validate(row)
