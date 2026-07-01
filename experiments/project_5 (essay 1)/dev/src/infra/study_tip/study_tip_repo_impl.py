from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.study_tip.study_tip_dto import StudyTipCreate, StudyTipUpdate, StudyTipResponse
from src.orm.study_tip.study_tip_orm import StudyTipORM


class SQLAlchemyStudyTipRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[StudyTipResponse]:
        row = self._session.get(StudyTipORM, item_id)
        return StudyTipResponse.model_validate(row) if row else None

    def get_by_competency(self, competency_name: str) -> list[StudyTipResponse]:
        rows = self._session.query(StudyTipORM).filter(StudyTipORM.competency_name == competency_name).all()
        return [StudyTipResponse.model_validate(r) for r in rows]

    def get_all(self, skip: int = 0, limit: int = 100) -> list[StudyTipResponse]:
        rows = self._session.query(StudyTipORM).offset(skip).limit(limit).all()
        return [StudyTipResponse.model_validate(r) for r in rows]

    def create(self, data: StudyTipCreate) -> StudyTipResponse:
        row = StudyTipORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return StudyTipResponse.model_validate(row)

    def update(self, item_id: int, data: StudyTipUpdate) -> Optional[StudyTipResponse]:
        row = self._session.get(StudyTipORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return StudyTipResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(StudyTipORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
