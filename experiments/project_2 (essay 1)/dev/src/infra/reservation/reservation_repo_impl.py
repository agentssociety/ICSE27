from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.reservation.reservation_dto import (
    ReservationCreateRequest,
    ReservationUpdateRequest,
    ReservationResponse,
)
from src.orm.reservation.reservation_orm import ReservationORM


class SQLAlchemyReservationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ReservationResponse]:
        row = self._session.get(ReservationORM, item_id)
        return ReservationResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ReservationResponse]:
        rows = self._session.query(ReservationORM).offset(skip).limit(limit).all()
        return [ReservationResponse.model_validate(r) for r in rows]

    def create(self, data: ReservationCreateRequest) -> ReservationResponse:
        row = ReservationORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ReservationResponse.model_validate(row)

    def update(self, item_id: int, data: ReservationUpdateRequest) -> Optional[ReservationResponse]:
        row = self._session.get(ReservationORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ReservationResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ReservationORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
