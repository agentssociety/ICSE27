from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.it_team.it_team_dto import IT_TeamCreate, IT_TeamUpdate, IT_TeamResponse
from src.orm.it_team.it_team_orm import IT_TeamORM


class SQLAlchemyIT_TeamRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[IT_TeamResponse]:
        row = self._session.get(IT_TeamORM, item_id)
        return IT_TeamResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[IT_TeamResponse]:
        rows = self._session.query(IT_TeamORM).offset(skip).limit(limit).all()
        return [IT_TeamResponse.model_validate(r) for r in rows]

    def create(self, data: IT_TeamCreate) -> IT_TeamResponse:
        row = IT_TeamORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return IT_TeamResponse.model_validate(row)

    def update(self, item_id: int, data: IT_TeamUpdate) -> Optional[IT_TeamResponse]:
        row = self._session.get(IT_TeamORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return IT_TeamResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(IT_TeamORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
