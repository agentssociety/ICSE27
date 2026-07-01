from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.photo.photo_dto import PhotoCreate, PhotoUpdate, PhotoResponse
from src.orm.photo.photo_orm import PhotoORM


class SQLAlchemyPhotoRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PhotoResponse]:
        row = self._session.get(PhotoORM, item_id)
        return PhotoResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PhotoResponse]:
        rows = self._session.query(PhotoORM).offset(skip).limit(limit).all()
        return [PhotoResponse.model_validate(r) for r in rows]

    def create(self, data: PhotoCreate) -> PhotoResponse:
        row = PhotoORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PhotoResponse.model_validate(row)

    def update(self, item_id: int, data: PhotoUpdate) -> Optional[PhotoResponse]:
        row = self._session.get(PhotoORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PhotoResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PhotoORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
