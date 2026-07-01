from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.registration_data.registration_data_dto import RegistrationDataCreate, RegistrationDataUpdate, RegistrationDataResponse
from src.orm.registration_data.registration_data_orm import RegistrationDataORM


class SQLAlchemyRegistrationDataRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[RegistrationDataResponse]:
        row = self._session.get(RegistrationDataORM, item_id)
        return RegistrationDataResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RegistrationDataResponse]:
        rows = self._session.query(RegistrationDataORM).offset(skip).limit(limit).all()
        return [RegistrationDataResponse.model_validate(r) for r in rows]

    def create(self, data: RegistrationDataCreate) -> RegistrationDataResponse:
        row = RegistrationDataORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return RegistrationDataResponse.model_validate(row)

    def update(self, item_id: int, data: RegistrationDataUpdate) -> Optional[RegistrationDataResponse]:
        row = self._session.get(RegistrationDataORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return RegistrationDataResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(RegistrationDataORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
