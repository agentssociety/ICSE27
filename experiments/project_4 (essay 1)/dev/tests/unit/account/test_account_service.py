from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from src.service.account.account_service import AuthenticationFlow, AccountManagementService


class TestAccountAuthenticationFlow:
    def test_authenticate_no_accounts(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = []
        flow = AuthenticationFlow(mock_repo)
        result = flow.authenticate("card", "pin")
        assert result is False


class TestAccountManagementService:
    def test_lock_account_not_found_returns_false(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None
        service = AccountManagementService(mock_repo)
        result = service.lock_account(999, "suspicious activity")
        assert result is False
        mock_repo.get_by_id.assert_called_once_with(999)
        mock_repo.update.assert_not_called()

    def test_lock_account_found_returns_true_and_updates(self) -> None:
        from src.dto.account.account_dto import AccountResponse

        mock_repo = MagicMock()
        # Create a mock AccountResponse with required fields
        response = AccountResponse(
            id=1,
            failedAttempts=0,
            balance=100.0,
            daily_withdrawal_limit=1000.0,
            withdrawn_today=0.0,
            user_id=1,
        )
        mock_repo.get_by_id.return_value = response
        mock_repo.update.return_value = response

        service = AccountManagementService(mock_repo)
        result = service.lock_account(1, "suspicious activity")
        assert result is True
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.update.assert_called_once()

    def test_unlock_account_not_found_returns_false(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None
        service = AccountManagementService(mock_repo)
        result = service.unlock_account(999)
        assert result is False
        mock_repo.get_by_id.assert_called_once_with(999)
        mock_repo.update.assert_not_called()

    def test_unlock_account_found_returns_true_and_updates(self) -> None:
        from src.dto.account.account_dto import AccountResponse

        mock_repo = MagicMock()
        response = AccountResponse(
            id=1,
            failedAttempts=0,
            balance=100.0,
            daily_withdrawal_limit=1000.0,
            withdrawn_today=0.0,
            user_id=1,
        )
        mock_repo.get_by_id.return_value = response
        mock_repo.update.return_value = response

        service = AccountManagementService(mock_repo)
        result = service.unlock_account(1)
        assert result is True
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.update.assert_called_once()

    def test_get_account_state_not_found_returns_none(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None
        service = AccountManagementService(mock_repo)
        result = service.get_account_state(999)
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(999)

    def test_get_account_state_active(self) -> None:
        from src.dto.account.account_dto import AccountResponse

        mock_repo = MagicMock()
        response = AccountResponse(
            id=1,
            failedAttempts=0,
            balance=100.0,
            daily_withdrawal_limit=1000.0,
            withdrawn_today=0.0,
            state="active",
            user_id=1,
        )
        mock_repo.get_by_id.return_value = response
        service = AccountManagementService(mock_repo)
        result = service.get_account_state(1)
        assert result == "active"
        mock_repo.get_by_id.assert_called_once_with(1)
