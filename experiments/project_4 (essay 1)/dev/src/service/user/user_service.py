from __future__ import annotations

from typing import Any, Optional

# Import removed to avoid broken dependency chain
# from src.infra.user.user_repo_impl import SQLAlchemyUserRepository


class AuthenticationResult:
    success: bool
    reason: str | None

    def __init__(self, success: bool, reason: str | None = None) -> None:
        self.success = success
        self.reason = reason


class AuthenticationFlow:
    def __init__(self, repo: "SQLAlchemyUserRepository") -> None:
        self._repo = repo
        self._max_failed_attempts = 3

    def authenticate(self, cardData: str, pinData: str) -> AuthenticationResult:
        user = self._repo.get_by_id(1)
        if user is None:
            return AuthenticationResult(False, "User not found")

        card_valid = self._validate_card(cardData)
        if not card_valid:
            return AuthenticationResult(False, "Invalid card")

        pin_valid = self._validate_pin(pinData)
        if not pin_valid:
            self._record_failed_attempt(user)
            return AuthenticationResult(False, "Invalid PIN")

        return AuthenticationResult(True, "Authenticated")

    def false(self, expired: Any) -> None:
        pass

    def _validate_card(self, cardData: str) -> bool:
        return bool(cardData)

    def _validate_pin(self, pinData: str) -> bool:
        return bool(pinData)

    def _record_failed_attempt(self, user: Any) -> None:
        pass