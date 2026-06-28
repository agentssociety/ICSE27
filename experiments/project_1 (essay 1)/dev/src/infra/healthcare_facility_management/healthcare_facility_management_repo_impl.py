from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.healthcare_facility_management.healthcare_facility_management_dto import HealthcareFacilityManagementCreate, HealthcareFacilityManagementUpdate, HealthcareFacilityManagementResponse
from src.orm.healthcare_facility_management.healthcare_facility_management_orm import HealthcareFacilityManagementORM


class SQLAlchemyHealthcareFacilityManagementRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[HealthcareFacilityManagementResponse]:
        row = self._session.get(HealthcareFacilityManagementORM, item_id)
        return HealthcareFacilityManagementResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[HealthcareFacilityManagementResponse]:
        rows = self._session.query(HealthcareFacilityManagementORM).offset(skip).limit(limit).all()
        return [HealthcareFacilityManagementResponse.model_validate(r) for r in rows]

    def create(self, data: HealthcareFacilityManagementCreate) -> HealthcareFacilityManagementResponse:
        row = HealthcareFacilityManagementORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return HealthcareFacilityManagementResponse.model_validate(row)

    def update(self, item_id: int, data: HealthcareFacilityManagementUpdate) -> Optional[HealthcareFacilityManagementResponse]:
        row = self._session.get(HealthcareFacilityManagementORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return HealthcareFacilityManagementResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(HealthcareFacilityManagementORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
