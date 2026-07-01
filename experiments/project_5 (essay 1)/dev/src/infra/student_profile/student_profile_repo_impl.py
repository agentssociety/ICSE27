from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.student_profile.student_profile_dto import StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse
from src.orm.student_profile.student_profile_orm import StudentProfileORM


class SQLAlchemyStudentProfileRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[StudentProfileResponse]:
        row = self._session.get(StudentProfileORM, item_id)
        return StudentProfileResponse.model_validate(row) if row else None

    def get_by_student_id(self, student_id: int) -> Optional[StudentProfileResponse]:
        row = self._session.query(StudentProfileORM).filter(StudentProfileORM.student_id == student_id).first()
        return StudentProfileResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[StudentProfileResponse]:
        rows = self._session.query(StudentProfileORM).offset(skip).limit(limit).all()
        return [StudentProfileResponse.model_validate(r) for r in rows]

    def create(self, data: StudentProfileCreate) -> StudentProfileResponse:
        row = StudentProfileORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return StudentProfileResponse.model_validate(row)

    def update(self, item_id: int, data: StudentProfileUpdate) -> Optional[StudentProfileResponse]:
        row = self._session.get(StudentProfileORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return StudentProfileResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(StudentProfileORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
