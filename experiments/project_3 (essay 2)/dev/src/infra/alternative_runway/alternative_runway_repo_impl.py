from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.alternative_runway.alternative_runway_dto import AlternativeRunwayCreate, AlternativeRunwayUpdate, AlternativeRunwayResponse
from src.orm.alternative_runway.alternative_runway_orm import AlternativeRunwayORM


class SQLAlchemyAlternativeRunwayRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AlternativeRunwayResponse]:
        row = self._session.get(AlternativeRunwayORM, item_id)
        return AlternativeRunwayResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AlternativeRunwayResponse]:
        rows = self._session.query(AlternativeRunwayORM).offset(skip).limit(limit).all()
        return [AlternativeRunwayResponse.model_validate(r) for r in rows]

    def create(self, data: AlternativeRunwayCreate) -> AlternativeRunwayResponse:
        row = AlternativeRunwayORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AlternativeRunwayResponse.model_validate(row)

    def update(self, item_id: int, data: AlternativeRunwayUpdate) -> Optional[AlternativeRunwayResponse]:
        row = self._session.get(AlternativeRunwayORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AlternativeRunwayResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AlternativeRunwayORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
