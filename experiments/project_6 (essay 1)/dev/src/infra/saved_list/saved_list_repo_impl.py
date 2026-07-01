from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.saved_list.saved_list_dto import SavedListCreate, SavedListUpdate, SavedListResponse
from src.orm.saved_list.saved_list_orm import SavedListORM


class SQLAlchemySavedListRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SavedListResponse]:
        row = self._session.get(SavedListORM, item_id)
        return SavedListResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SavedListResponse]:
        rows = self._session.query(SavedListORM).offset(skip).limit(limit).all()
        return [SavedListResponse.model_validate(r) for r in rows]

    def create(self, data: SavedListCreate) -> SavedListResponse:
        row = SavedListORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SavedListResponse.model_validate(row)

    def update(self, item_id: int, data: SavedListUpdate) -> Optional[SavedListResponse]:
        row = self._session.get(SavedListORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SavedListResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SavedListORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
