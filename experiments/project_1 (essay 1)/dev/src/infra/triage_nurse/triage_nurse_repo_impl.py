from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.triage_nurse.triage_nurse_dto import TriageNurseCreate, TriageNurseUpdate, TriageNurseResponse
from src.orm.triage_nurse.triage_nurse_orm import TriageNurseORM


class SQLAlchemyTriageNurseRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[TriageNurseResponse]:
        row = self._session.get(TriageNurseORM, item_id)
        return TriageNurseResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TriageNurseResponse]:
        rows = self._session.query(TriageNurseORM).offset(skip).limit(limit).all()
        return [TriageNurseResponse.model_validate(r) for r in rows]

    def create(self, data: TriageNurseCreate) -> TriageNurseResponse:
        row = TriageNurseORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TriageNurseResponse.model_validate(row)

    def update(self, item_id: int, data: TriageNurseUpdate) -> Optional[TriageNurseResponse]:
        row = self._session.get(TriageNurseORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return TriageNurseResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(TriageNurseORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
