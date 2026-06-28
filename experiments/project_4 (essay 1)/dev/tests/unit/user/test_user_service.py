from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from src.service.user.user_service import AuthenticationFlow, AuthenticationResult


class TestAuthenticationFlow:
    def test_authenticate_success(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = MagicMock()
        flow = AuthenticationFlow(mock_repo)
        result = flow.authenticate("card123", "pin456")
        assert result.success is True
        assert result.reason == "Authenticated"

    def test_authenticate_failure_no_user(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None
        flow = AuthenticationFlow(mock_repo)
        result = flow.authenticate("card123", "pin456")
        assert result.success is False
        assert result.reason == "User not found"
