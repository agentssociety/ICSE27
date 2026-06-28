from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.runway.runway_dto import RunwayCreate, RunwayUpdate, RunwayResponse
from src.orm.runway.runway_orm import RunwayORM


class SQLAlchemyRunwayRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[RunwayResponse]:
        row = self._session.get(RunwayORM, item_id)
        return RunwayResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RunwayResponse]:
        rows = self._session.query(RunwayORM).offset(skip).limit(limit).all()
        return [RunwayResponse.model_validate(r) for r in rows]

    def create(self, data: RunwayCreate) -> RunwayResponse:
        row = RunwayORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return RunwayResponse.model_validate(row)

    def update(self, item_id: int, data: RunwayUpdate) -> Optional[RunwayResponse]:
        row = self._session.get(RunwayORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return RunwayResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(RunwayORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
