from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.patient_care_team.patient_care_team_dto import PatientCareTeamCreate, PatientCareTeamUpdate, PatientCareTeamResponse
from src.orm.patient_care_team.patient_care_team_orm import PatientCareTeamORM


class SQLAlchemyPatientCareTeamRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PatientCareTeamResponse]:
        row = self._session.get(PatientCareTeamORM, item_id)
        return PatientCareTeamResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PatientCareTeamResponse]:
        rows = self._session.query(PatientCareTeamORM).offset(skip).limit(limit).all()
        return [PatientCareTeamResponse.model_validate(r) for r in rows]

    def create(self, data: PatientCareTeamCreate) -> PatientCareTeamResponse:
        row = PatientCareTeamORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PatientCareTeamResponse.model_validate(row)

    def update(self, item_id: int, data: PatientCareTeamUpdate) -> Optional[PatientCareTeamResponse]:
        row = self._session.get(PatientCareTeamORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PatientCareTeamResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PatientCareTeamORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
