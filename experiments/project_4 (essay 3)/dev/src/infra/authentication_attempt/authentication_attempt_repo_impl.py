from __future__ import annotations

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from src.dto.authentication_attempt.authentication_attempt_dto import AuthenticationAttemptCreate, AuthenticationAttemptResponse
from src.orm.authentication_attempt.authentication_attempt_orm import AuthenticationAttemptORM


class SQLAlchemyAuthenticationAttemptRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[AuthenticationAttemptResponse]:
        row = self._session.get(AuthenticationAttemptORM, item_id)
        if row is None:
            return None
        return AuthenticationAttemptResponse.model_validate(row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AuthenticationAttemptResponse]:
        rows = self._session.query(AuthenticationAttemptORM).order_by(AuthenticationAttemptORM.timestamp.desc()).offset(skip).limit(limit).all()
        return [AuthenticationAttemptResponse.model_validate(r) for r in rows]

    def create(self, data: AuthenticationAttemptCreate) -> AuthenticationAttemptResponse:
        from src.domain.authentication_attempt.AuthenticationAttempt import AuthenticationAttempt, AuthenticationOutcome, AuthenticationMethod
        outcome = AuthenticationOutcome.SUCCESS if data.outcome == "success" else AuthenticationOutcome.FAILURE
        method = AuthenticationMethod(data.method)
        attempt = AuthenticationAttempt.create(
            user_id=data.user_id,
            outcome=outcome,
            method=method,
            ip_address=data.ip_address,
        )
        row = AuthenticationAttemptORM(
            id=attempt.id,
            user_id=attempt.user_id,
            outcome=attempt.outcome.value,
            method=attempt.method.value,
            ip_address=attempt.ip_address,
            timestamp=attempt.timestamp,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AuthenticationAttemptResponse.model_validate(row)

    def delete(self, item_id: str) -> bool:
        row = self._session.get(AuthenticationAttemptORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
