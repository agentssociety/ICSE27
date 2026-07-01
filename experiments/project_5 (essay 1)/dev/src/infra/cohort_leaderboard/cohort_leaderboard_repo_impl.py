from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.cohort_leaderboard.cohort_leaderboard_dto import CohortLeaderboardCreate, CohortLeaderboardUpdate, CohortLeaderboardResponse
from src.orm.cohort_leaderboard.cohort_leaderboard_orm import CohortLeaderboardORM


class SQLAlchemyCohortLeaderboardRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[CohortLeaderboardResponse]:
        row = self._session.get(CohortLeaderboardORM, item_id)
        return CohortLeaderboardResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CohortLeaderboardResponse]:
        rows = self._session.query(CohortLeaderboardORM).offset(skip).limit(limit).all()
        return [CohortLeaderboardResponse.model_validate(r) for r in rows]

    def create(self, data: CohortLeaderboardCreate) -> CohortLeaderboardResponse:
        row = CohortLeaderboardORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return CohortLeaderboardResponse.model_validate(row)

    def update(self, item_id: int, data: CohortLeaderboardUpdate) -> Optional[CohortLeaderboardResponse]:
        row = self._session.get(CohortLeaderboardORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return CohortLeaderboardResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(CohortLeaderboardORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
