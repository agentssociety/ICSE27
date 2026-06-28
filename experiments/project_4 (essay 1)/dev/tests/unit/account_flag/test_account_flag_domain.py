from __future__ import annotations

import pytest
from datetime import datetime
from src.domain.account_flag import AccountFlag, FlagReason


class TestAccountFlagDomain:
    def test_account_flag_default_reason(self) -> None:
        flag = AccountFlag(account_id=1)
        assert flag.reason == FlagReason.MANUAL_REVIEW

    def test_account_flag_custom_reason(self) -> None:
        flag = AccountFlag(account_id=1, reason=FlagReason.UNUSUAL_AMOUNT)
        assert flag.reason == FlagReason.UNUSUAL_AMOUNT

    def test_account_flag_matches_reason(self) -> None:
        flag = AccountFlag(account_id=1, reason=FlagReason.RAPID_CONSECUTIVE_WITHDRAWALS)
        assert flag.matches_reason(FlagReason.RAPID_CONSECUTIVE_WITHDRAWALS) is True
        assert flag.matches_reason(FlagReason.UNUSUAL_AMOUNT) is False

    def test_account_flag_transaction_id(self) -> None:
        flag = AccountFlag(account_id=1, transaction_id="txn-123")
        assert flag.transaction_id == "txn-123"

    def test_account_flag_timestamp_defaults_to_now(self) -> None:
        flag = AccountFlag(account_id=1)
        assert flag.timestamp is not None
        parsed = datetime.fromisoformat(flag.timestamp)
        assert parsed is not None
