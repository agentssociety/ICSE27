from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.blood_type_resource.blood_type_resource_dto import BloodTypeResourceCreate, BloodTypeResourceUpdate, BloodTypeResourceResponse
from src.orm.blood_type_resource.blood_type_resource_orm import BloodTypeResourceORM


class SQLAlchemyBloodTypeResourceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[BloodTypeResourceResponse]:
        row = self._session.get(BloodTypeResourceORM, item_id)
        return BloodTypeResourceResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BloodTypeResourceResponse]:
        rows = self._session.query(BloodTypeResourceORM).offset(skip).limit(limit).all()
        return [BloodTypeResourceResponse.model_validate(r) for r in rows]

    def create(self, data: BloodTypeResourceCreate) -> BloodTypeResourceResponse:
        row = BloodTypeResourceORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return BloodTypeResourceResponse.model_validate(row)

    def update(self, item_id: int, data: BloodTypeResourceUpdate) -> Optional[BloodTypeResourceResponse]:
        row = self._session.get(BloodTypeResourceORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return BloodTypeResourceResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(BloodTypeResourceORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True