from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.post.post_dto import PostCreateDTO, PostUpdateDTO, PostResponseDTO
from src.orm.post.post_orm import PostORM


class SQLAlchemyPostRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PostResponseDTO]:
        row = self._session.get(PostORM, item_id)
        return PostResponseDTO.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PostResponseDTO]:
        rows = self._session.query(PostORM).offset(skip).limit(limit).all()
        return [PostResponseDTO.model_validate(r) for r in rows]

    def create(self, data: PostCreateDTO) -> PostResponseDTO:
        row = PostORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PostResponseDTO.model_validate(row)

    def update(self, item_id: int, data: PostUpdateDTO) -> Optional[PostResponseDTO]:
        row = self._session.get(PostORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PostResponseDTO.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PostORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True