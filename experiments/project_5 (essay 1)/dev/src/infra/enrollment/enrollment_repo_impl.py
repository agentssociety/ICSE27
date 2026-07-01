from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.enrollment.enrollment_dto import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from src.orm.enrollment.enrollment_orm import EnrollmentORM


class SQLAlchemyEnrollmentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[EnrollmentResponse]:
        row = self._session.get(EnrollmentORM, item_id)
        return EnrollmentResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[EnrollmentResponse]:
        rows = self._session.query(EnrollmentORM).offset(skip).limit(limit).all()
        return [EnrollmentResponse.model_validate(r) for r in rows]

    def create(self, data: EnrollmentCreate) -> EnrollmentResponse:
        row = EnrollmentORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return EnrollmentResponse.model_validate(row)

    def update(self, item_id: int, data: EnrollmentUpdate) -> Optional[EnrollmentResponse]:
        row = self._session.get(EnrollmentORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return EnrollmentResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(EnrollmentORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
