from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from src.service.account_flag.account_flag_service import AccountFlagServiceImpl
from src.dto.account_flag.account_flag_dto import AccountFlagCreate, AccountFlagResponse


class MockTransaction:
    def __init__(self, transaction_id, amount, timestamp, account_id=1):
        self.transaction_id = transaction_id
        self.amount = amount
        self.timestamp = timestamp
        self.account_id = account_id
        self.id = 1
        self.user_id = account_id
        self.status = "completed"


class TestAccountFlagService:
    def setup_method(self):
        self._mock_flag_repo = MagicMock()
        self._mock_txn_repo = MagicMock()
        self._service = AccountFlagServiceImpl(
            account_flag_repo=self._mock_flag_repo,
            transaction_repo=self._mock_txn_repo,
        )

    def test_detect_rapid_withdrawals_returns_true_when_more_than_3_in_5_min(self):
        now = datetime.now()
        timestamps = [
            (now - timedelta(minutes=1)).isoformat(),
            (now - timedelta(minutes=2)).isoformat(),
            (now - timedelta(minutes=3)).isoformat(),
            (now - timedelta(minutes=4)).isoformat(),
        ]
        mock_txns = [MockTransaction("txn-1", 50.0, ts) for ts in timestamps]
        self._mock_txn_repo.get_by_user_id.return_value = mock_txns
        result = self._service.detect_rapid_consecutive_withdrawals(
            account_id=1, timestamp=now.isoformat()
        )
        assert result is True

    def test_detect_rapid_withdrawals_returns_false_when_3_or_less(self):
        now = datetime.now()
        timestamps = [
            (now - timedelta(minutes=1)).isoformat(),
            (now - timedelta(minutes=2)).isoformat(),
            (now - timedelta(minutes=4)).isoformat(),
        ]
        mock_txns = [MockTransaction("txn-1", 50.0, ts) for ts in timestamps]
        self._mock_txn_repo.get_by_user_id.return_value = mock_txns
        result = self._service.detect_rapid_consecutive_withdrawals(
            account_id=1, timestamp=now.isoformat()
        )
        assert result is False

    def test_detect_rapid_withdrawals_no_transactions(self):
        self._mock_txn_repo.get_by_user_id.return_value = []
        result = self._service.detect_rapid_consecutive_withdrawals(
            account_id=1, timestamp=datetime.now().isoformat()
        )
        assert result is False

    def test_detect_unusual_amount_returns_true_when_10x_average(self):
        mock_txns = [
            MockTransaction("txn-1", 50.0, datetime.now().isoformat()),
            MockTransaction("txn-2", 60.0, datetime.now().isoformat()),
            MockTransaction("txn-3", 40.0, datetime.now().isoformat()),
        ]
        self._mock_txn_repo.get_by_user_id.return_value = mock_txns
        result = self._service.detect_unusual_amount(
            account_id=1, amount=600.0
        )
        assert result is True

    def test_detect_unusual_amount_returns_false_when_within_normal_range(self):
        mock_txns = [
            MockTransaction("txn-1", 50.0, datetime.now().isoformat()),
            MockTransaction("txn-2", 60.0, datetime.now().isoformat()),
        ]
        self._mock_txn_repo.get_by_user_id.return_value = mock_txns
        result = self._service.detect_unusual_amount(
            account_id=1, amount=100.0
        )
        assert result is False

    def test_detect_unusual_amount_no_history(self):
        self._mock_txn_repo.get_by_user_id.return_value = []
        result = self._service.detect_unusual_amount(
            account_id=1, amount=1000.0
        )
        assert result is False

    def test_detect_and_flag_returns_none_when_no_pattern_detected(self):
        self._mock_txn_repo.get_by_user_id.return_value = []
        result = self._service.detect_and_flag(
            account_id=1, transaction_id="txn-1", amount=50.0,
            timestamp=datetime.now().isoformat()
        )
        assert result is None
        self._mock_flag_repo.create.assert_not_called()

    def test_detect_and_flag_creates_flag_for_rapid_withdrawals(self):
        now = datetime.now()
        timestamps = [
            (now - timedelta(minutes=1)).isoformat(),
            (now - timedelta(minutes=2)).isoformat(),
            (now - timedelta(minutes=3)).isoformat(),
            (now - timedelta(minutes=4)).isoformat(),
        ]
        mock_txns = [MockTransaction("txn-1", 50.0, ts) for ts in timestamps]
        self._mock_txn_repo.get_by_user_id.return_value = mock_txns
        mock_flag_response = AccountFlagResponse(
            id=1, account_id=1, transaction_id="txn-new"
        )
        self._mock_flag_repo.create.return_value = mock_flag_response
        result = self._service.detect_and_flag(
            account_id=1, transaction_id="txn-new", amount=50.0,
            timestamp=now.isoformat()
        )
        assert result is not None
        assert result.id == 1
        self._mock_flag_repo.create.assert_called_once()

    def test_detect_and_flag_creates_flag_for_unusual_amount(self):
        mock_txns = [
            MockTransaction("txn-1", 50.0, datetime.now().isoformat()),
            MockTransaction("txn-2", 60.0, datetime.now().isoformat()),
        ]
        self._mock_txn_repo.get_by_user_id.return_value = mock_txns
        mock_flag_response = AccountFlagResponse(
            id=1, account_id=1, transaction_id="txn-large"
        )
        self._mock_flag_repo.create.return_value = mock_flag_response
        result = self._service.detect_and_flag(
            account_id=1, transaction_id="txn-large", amount=600.0,
            timestamp=datetime.now().isoformat()
        )
        assert result is not None
        assert result.id == 1
        self._mock_flag_repo.create.assert_called_once()

    def test_detect_and_flag_rapid_withdrawals_takes_precedence(self):
        now = datetime.now()
        timestamps = [
            (now - timedelta(minutes=1)).isoformat(),
            (now - timedelta(minutes=2)).isoformat(),
            (now - timedelta(minutes=3)).isoformat(),
            (now - timedelta(minutes=4)).isoformat(),
        ]
        mock_txns = [MockTransaction("txn-1", 50.0, ts) for ts in timestamps]
        self._mock_txn_repo.get_by_user_id.return_value = mock_txns
        mock_flag_response = AccountFlagResponse(
            id=1, account_id=1, transaction_id="txn-new"
        )
        self._mock_flag_repo.create.return_value = mock_flag_response
        result = self._service.detect_and_flag(
            account_id=1, transaction_id="txn-new", amount=1000.0,
            timestamp=now.isoformat()
        )
        assert result is not None
        self._mock_flag_repo.create.assert_called_once()

    def test_get_flags_for_account_returns_matching_flags(self):
        self._mock_flag_repo.get_all.return_value = [
            AccountFlagResponse(id=1, account_id=1, transaction_id="txn-1"),
            AccountFlagResponse(id=2, account_id=2, transaction_id="txn-2"),
            AccountFlagResponse(id=3, account_id=1, transaction_id="txn-3"),
        ]
        result = self._service.get_flags_for_account(account_id=1)
        assert len(result) == 2
        assert all(f.account_id == 1 for f in result)

    def test_get_flags_for_account_empty_when_no_flags(self):
        self._mock_flag_repo.get_all.return_value = []
        result = self._service.get_flags_for_account(account_id=1)
        assert result == []

    def test_get_all_flags_returns_all(self):
        expected = [
            AccountFlagResponse(id=1, account_id=1, transaction_id="txn-1"),
            AccountFlagResponse(id=2, account_id=2, transaction_id="txn-2"),
        ]
        self._mock_flag_repo.get_all.return_value = expected
        result = self._service.get_all_flags()
        assert result == expected
