from __future__ import annotations

from typing import Optional
from sqlalchemy.orm import Session

from src.dto.authentication_attempt.authentication_attempt_dto import AuthenticationAttemptCreate, AuthenticationAttemptResponse
from src.infra.authentication_attempt.authentication_attempt_repo_impl import SQLAlchemyAuthenticationAttemptRepository


class AuthenticationAttemptService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = SQLAlchemyAuthenticationAttemptRepository(session)

    def create_attempt(self, data: AuthenticationAttemptCreate) -> AuthenticationAttemptResponse:
        return self._repo.create(data)

    def list_attempts(self, skip: int = 0, limit: int = 100) -> list[AuthenticationAttemptResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def get_attempt(self, attempt_id: str) -> Optional[AuthenticationAttemptResponse]:
        return self._repo.get_by_id(attempt_id)
