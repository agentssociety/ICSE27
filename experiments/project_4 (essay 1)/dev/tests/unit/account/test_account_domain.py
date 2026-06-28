from __future__ import annotations

import pytest
from src.domain.account import Account, AccountState, AccountId, AccountCreatedEvent, AccountUpdatedEvent


class TestAccountDomain:
    def test_account_initial_state(self) -> None:
        account = Account()
        assert account.state == AccountState.ACTIVE
        assert account.failedAttempts == 0

    def test_account_authenticate_active(self) -> None:
        account = Account()
        assert account.authenticate() is True

    def test_account_authenticate_locked(self) -> None:
        account = Account(state=AccountState.LOCKED)
        assert account.authenticate() is False

    def test_record_failed_attempt(self) -> None:
        account = Account()
        account.recordFailedAttempt()
        assert account.failedAttempts == 1

    def test_account_locks_after_3_failures(self) -> None:
        account = Account()
        for _ in range(3):
            account.recordFailedAttempt()
        assert account.state == AccountState.LOCKED

    # ----- Balance and daily limit validation tests -----

    def test_has_sufficient_balance_returns_true_when_balance_is_enough(self) -> None:
        account = Account(balance=100.0)
        assert account.has_sufficient_balance(50.0) is True

    def test_has_sufficient_balance_returns_false_when_balance_is_insufficient(self) -> None:
        account = Account(balance=30.0)
        assert account.has_sufficient_balance(50.0) is False

    def test_has_sufficient_balance_returns_true_when_amount_equals_balance(self) -> None:
        account = Account(balance=50.0)
        assert account.has_sufficient_balance(50.0) is True

    def test_has_daily_limit_remaining_returns_true_when_within_limit(self) -> None:
        account = Account(daily_withdrawal_limit=1000.0, withdrawn_today=200.0)
        assert account.has_daily_limit_remaining(500.0) is True

    def test_has_daily_limit_remaining_returns_false_when_limit_exceeded(self) -> None:
        account = Account(daily_withdrawal_limit=1000.0, withdrawn_today=800.0)
        assert account.has_daily_limit_remaining(300.0) is False

    def test_has_daily_limit_remaining_returns_true_when_exactly_at_limit(self) -> None:
        account = Account(daily_withdrawal_limit=1000.0, withdrawn_today=600.0)
        assert account.has_daily_limit_remaining(400.0) is True

    def test_can_withdraw_returns_true_when_both_checks_pass(self) -> None:
        account = Account(balance=500.0, daily_withdrawal_limit=1000.0, withdrawn_today=100.0)
        assert account.can_withdraw(200.0) is True

    def test_can_withdraw_returns_false_when_balance_insufficient(self) -> None:
        account = Account(balance=50.0, daily_withdrawal_limit=1000.0, withdrawn_today=100.0)
        assert account.can_withdraw(200.0) is False

    def test_can_withdraw_returns_false_when_daily_limit_exceeded(self) -> None:
        account = Account(balance=500.0, daily_withdrawal_limit=1000.0, withdrawn_today=900.0)
        assert account.can_withdraw(200.0) is False

    def test_deduct_balance_reduces_balance(self) -> None:
        account = Account(balance=100.0)
        account.deduct_balance(40.0)
        assert account.balance == 60.0

    def test_deduct_balance_raises_error_on_insufficient_funds(self) -> None:
        account = Account(balance=30.0)
        with pytest.raises(ValueError, match="Insufficient balance"):
            account.deduct_balance(50.0)

    def test_record_withdrawal_increases_withdrawn_today(self) -> None:
        account = Account(daily_withdrawal_limit=1000.0, withdrawn_today=100.0)
        account.record_withdrawal(200.0)
        assert account.withdrawn_today == 300.0

    def test_daily_withdrawal_limit_has_default_value(self) -> None:
        account = Account()
        assert account.daily_withdrawal_limit == 1000.0

    def test_withdrawn_today_defaults_to_zero(self) -> None:
        account = Account()
        assert account.withdrawn_today == 0.0

    # ----- Admin lock/unlock tests (Task 85) -----

    def test_lock_account_changes_state_to_locked(self) -> None:
        account = Account()
        account.lock(reason="suspicious activity")
        assert account.state == AccountState.LOCKED

    def test_lock_account_records_reason(self) -> None:
        account = Account()
        account.lock(reason="suspicious activity")
        assert account.locked_reason == "suspicious activity"

    def test_lock_with_empty_reason_sets_locked_reason_to_none(self) -> None:
        account = Account()
        account.lock()
        assert account.state == AccountState.LOCKED
        assert account.locked_reason is None

    def test_locked_account_cannot_authenticate(self) -> None:
        account = Account()
        account.lock(reason="fraud detected")
        assert account.authenticate() is False

    def test_unlock_account_changes_state_to_active(self) -> None:
        account = Account(state=AccountState.LOCKED, locked_reason="resolved")
        account.unlock()
        assert account.state == AccountState.ACTIVE

    def test_unlock_account_clears_locked_reason(self) -> None:
        account = Account(state=AccountState.LOCKED, locked_reason="resolved")
        account.unlock()
        assert account.locked_reason is None

    def test_unlocked_account_can_authenticate(self) -> None:
        account = Account(state=AccountState.LOCKED)
        account.unlock()
        assert account.authenticate() is True

    def test_lock_unlock_cycle(self) -> None:
        """Full cycle: active -> locked -> active."""
        account = Account()
        assert account.state == AccountState.ACTIVE
        assert account.authenticate() is True

        account.lock(reason="suspicious activity")
        assert account.state == AccountState.LOCKED
        assert account.authenticate() is False

        account.unlock()
        assert account.state == AccountState.ACTIVE
        assert account.authenticate() is True
        assert account.locked_reason is None
