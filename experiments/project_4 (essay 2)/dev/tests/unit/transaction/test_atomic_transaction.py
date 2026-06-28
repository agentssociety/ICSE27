from __future__ import annotations

import pytest
from unittest.mock import MagicMock, create_autospec
from sqlalchemy.orm import Session

from src.infra.transaction.atomic_transaction_manager import AtomicTransactionManager

"""
Unit tests for atomic transaction support

Related tasks: #91
"""


def test_atomic_commit_on_success() -> None:
    """Given all operations succeed, the transaction is committed."""
    session = create_autospec(Session)
    mgr = AtomicTransactionManager(session)

    def operation(sess: Session) -> str:
        return "success"

    result = mgr.execute_in_transaction(operation)
    assert result == "success"
    session.commit.assert_called_once()
    session.rollback.assert_not_called()


def test_atomic_rollback_on_failure() -> None:
    """Given an operation fails, the transaction is rolled back."""
    session = create_autospec(Session)
    mgr = AtomicTransactionManager(session)

    def failing_operation(sess: Session) -> None:
        raise ValueError("Operation failed")

    with pytest.raises(ValueError, match="Operation failed"):
        mgr.execute_in_transaction(failing_operation)

    session.rollback.assert_called_once()
    session.commit.assert_not_called()


def test_context_manager_commit() -> None:
    """Using the context manager commits on success."""
    session = create_autospec(Session)
    mgr = AtomicTransactionManager(session)

    with mgr.atomic() as sess:
        sess.add("test")

    session.commit.assert_called_once()
    session.rollback.assert_not_called()


def test_context_manager_rollback() -> None:
    """Using the context manager rolls back on failure."""
    session = create_autospec(Session)
    mgr = AtomicTransactionManager(session)

    with pytest.raises(RuntimeError, match="Something went wrong"):
        with mgr.atomic() as sess:
            sess.add("test")
            raise RuntimeError("Something went wrong")

    session.rollback.assert_called_once()
    session.commit.assert_not_called()


def test_ensure_consistency_all_succeed() -> None:
    """Multiple operations all succeed and are committed."""
    session = create_autospec(Session)
    mgr = AtomicTransactionManager(session)

    results = []
    ops = [
        lambda s: results.append(1),
        lambda s: results.append(2),
        lambda s: results.append(3),
    ]

    mgr.ensure_consistency(ops)
    assert results == [1, 2, 3]
    session.commit.assert_called_once()
    session.rollback.assert_not_called()


def test_ensure_consistency_rollback_on_failure() -> None:
    """When one operation fails, all are rolled back and no results persist."""
    session = create_autospec(Session)
    mgr = AtomicTransactionManager(session)

    ops = [
        lambda s: None,  # succeeds
        lambda s: None,  # succeeds
        lambda s: (_ for _ in ()).throw(ValueError("Operation 3 failed")),  # fails
    ]

    with pytest.raises(ValueError, match="Operation 3 failed"):
        mgr.ensure_consistency(ops)

    session.rollback.assert_called_once()
    session.commit.assert_not_called()
