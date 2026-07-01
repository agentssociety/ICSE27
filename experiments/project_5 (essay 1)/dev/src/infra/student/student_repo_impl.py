from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.student.student_dto import StudentCreate, StudentUpdate, StudentResponse
from src.orm.student.student_orm import StudentORM


class SQLAlchemyStudentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[StudentResponse]:
        row = self._session.get(StudentORM, item_id)
        return StudentResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[StudentResponse]:
        rows = self._session.query(StudentORM).offset(skip).limit(limit).all()
        return [StudentResponse.model_validate(r) for r in rows]

    def create(self, data: StudentCreate) -> StudentResponse:
        row = StudentORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return StudentResponse.model_validate(row)

    def update(self, item_id: int, data: StudentUpdate) -> Optional[StudentResponse]:
        row = self._session.get(StudentORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return StudentResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(StudentORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
