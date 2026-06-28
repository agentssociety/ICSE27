from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.authentication_session.authentication_session_dto import AuthenticationSessionCreate, AuthenticationSessionUpdate, AuthenticationSessionResponse
from src.orm.authentication_session.authentication_session_orm import AuthenticationSessionORM


class SQLAlchemyAuthenticationSessionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AuthenticationSessionResponse]:
        row = self._session.get(AuthenticationSessionORM, item_id)
        return AuthenticationSessionResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuthenticationSessionResponse]:
        rows = self._session.query(AuthenticationSessionORM).offset(skip).limit(limit).all()
        return [AuthenticationSessionResponse.model_validate(r) for r in rows]

    def create(self, data: AuthenticationSessionCreate) -> AuthenticationSessionResponse:
        row = AuthenticationSessionORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AuthenticationSessionResponse.model_validate(row)

    def update(self, item_id: int, data: AuthenticationSessionUpdate) -> Optional[AuthenticationSessionResponse]:
        row = self._session.get(AuthenticationSessionORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AuthenticationSessionResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AuthenticationSessionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
