from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.actor.actor_dto import ActorCreate, ActorUpdate, ActorResponse

try:
    from src.orm.actor.actor_orm import ActorORM
except ImportError:
    ActorORM = None


class SQLAlchemyActorRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ActorResponse]:
        row = self._session.get(ActorORM, item_id)
        return ActorResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ActorResponse]:
        rows = self._session.query(ActorORM).offset(skip).limit(limit).all()
        return [ActorResponse.model_validate(r) for r in rows]

    def create(self, data: ActorCreate) -> ActorResponse:
        row = ActorORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ActorResponse.model_validate(row)

    def update(self, item_id: int, data: ActorUpdate) -> Optional[ActorResponse]:
        row = self._session.get(ActorORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ActorResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ActorORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True