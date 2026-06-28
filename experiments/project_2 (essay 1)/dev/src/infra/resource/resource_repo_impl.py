from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.resource.resource_dto import ResourceCreate, ResourceUpdate, ResourceResponse


class SQLAlchemyResourceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ResourceResponse]:
        from src.orm.resource.resource_orm import ResourceORM
        row = self._session.get(ResourceORM, item_id)
        return ResourceResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ResourceResponse]:
        from src.orm.resource.resource_orm import ResourceORM
        rows = self._session.query(ResourceORM).offset(skip).limit(limit).all()
        return [ResourceResponse.model_validate(r) for r in rows]

    def create(self, data: ResourceCreate) -> ResourceResponse:
        from src.orm.resource.resource_orm import ResourceORM
        row = ResourceORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ResourceResponse.model_validate(row)

    def update(self, item_id: int, data: ResourceUpdate) -> Optional[ResourceResponse]:
        from src.orm.resource.resource_orm import ResourceORM
        row = self._session.get(ResourceORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ResourceResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        from src.orm.resource.resource_orm import ResourceORM
        row = self._session.get(ResourceORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True