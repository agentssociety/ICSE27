from __future__ import annotations

import pytest
from src.domain.account.Account import (
    Account, AccountStatus, LockStatus, Permission,
    UserAccount, Admin, FailedAttempt, SecurityTeam,
    MAX_FAILED_PIN_ATTEMPTS
)

"""
Unit tests for Account across domain, service, and API layers

Related tasks: #89, #90, #94
"""


class MockUser:
    def __init__(self):
        self.userId = "test-user"


def test_account_initial_unlocked() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=100,
        dailyLimit=200,
        usedToday=0,
        user=MockUser(),
    )
    assert acc.lockStatus == LockStatus.UNLOCKED
    assert acc.balance == 100
    assert acc.dailyLimit == 200
    assert acc.usedToday == 0


def test_check_sufficient_funds() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=100,
        dailyLimit=200,
        usedToday=0,
        user=MockUser(),
    )
    assert acc.checkSufficientFunds(100, 50) is True
    assert acc.checkSufficientFunds(100, 150) is False


def test_check_daily_limit() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=100,
        dailyLimit=200,
        usedToday=180,
        user=MockUser(),
    )
    assert acc.checkDailyLimit(180, 200, 20) is True
    assert acc.checkDailyLimit(180, 200, 30) is False
    assert acc.checkDailyLimit(0, 200, 150) is True


def test_record_failed_attempt_locks_after_three() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=100,
        dailyLimit=200,
        usedToday=0,
        user=MockUser(),
    )
    assert acc.lockStatus == LockStatus.UNLOCKED
    acc.record_failed_attempt()
    assert acc.consecutiveFailedCount == 1
    assert acc.failedAttemptCount == 1
    assert acc.lockStatus == LockStatus.UNLOCKED
    
    acc.record_failed_attempt()
    assert acc.consecutiveFailedCount == 2
    assert acc.lockStatus == LockStatus.UNLOCKED
    
    acc.record_failed_attempt()
    assert acc.consecutiveFailedCount == 3
    assert acc.lockStatus == LockStatus.LOCKED


def test_reset_failed_attempts() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=1,
        consecutiveFailedCount=2,
        field_invariants=None,
        balance=100,
        dailyLimit=200,
        usedToday=0,
        user=MockUser(),
    )
    acc.reset_failed_attempts()
    assert acc.consecutiveFailedCount == 0
    # failedAttemptCount remains (total count)


def test_user_account_lock_unlock() -> None:
    admin = Admin()
    ua = UserAccount(status=AccountStatus.ACTIVE, abstract_owner=admin)
    assert ua.getStatus() == AccountStatus.ACTIVE
    
    ua.lock()
    assert ua.getStatus() == AccountStatus.LOCKED
    
    ua.unlock()
    assert ua.getStatus() == AccountStatus.ACTIVE


def test_update_balance_reduces_balance() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=100,
        dailyLimit=200,
        usedToday=0,
        user=MockUser(),
    )
    updated = acc.updateBalance(30)
    assert updated.balance == 70
    assert updated.usedToday == 30


def test_authorization_with_all_conditions_met() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=150,
        dailyLimit=200,
        usedToday=50,
        user=MockUser(),
    )
    assert acc.checkSufficientFunds(150, 100) is True
    assert acc.checkDailyLimit(50, 200, 100) is True


def test_authorization_rejected_insufficient_funds() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=100,
        dailyLimit=200,
        usedToday=0,
        user=MockUser(),
    )
    assert acc.checkSufficientFunds(100, 120) is False


def test_authorization_rejected_exceeds_daily_limit() -> None:
    acc = Account(
        lockStatus=LockStatus.UNLOCKED,
        failedAttemptCount=0,
        consecutiveFailedCount=0,
        field_invariants=None,
        balance=200,
        dailyLimit=200,
        usedToday=180,
        user=MockUser(),
    )
    assert acc.checkDailyLimit(180, 200, 30) is False
