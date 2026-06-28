from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator, Callable, TypeVar

from sqlalchemy.orm import Session

"""
Atomic transaction support with rollback capability.

This module provides utilities to ensure all-or-nothing execution
with proper rollback on failure.

Package: infra.transaction
Layer: infra
Related tasks: #91
"""

T = TypeVar("T")


class AtomicTransactionManager:
    """Manages atomic transactions with rollback capability.

    Provides a context manager that commits on success and rolls back on failure.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    @contextmanager
    def atomic(self) -> Generator[Session, None, None]:
        """Execute operations within an atomic transaction.

        If all operations succeed, the transaction is committed.
        If any operation fails, all changes are rolled back.

        Usage:
            with atomic_transaction_manager.atomic() as session:
                session.add(obj1)
                session.add(obj2)
        """
        try:
            yield self._session
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def execute_in_transaction(self, operation: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute a callable within an atomic transaction.

        Args:
            operation: A callable that takes session as the first argument.
            *args: Additional arguments passed to the operation.
            **kwargs: Additional keyword arguments passed to the operation.

        Returns:
            The return value of the operation.

        Raises:
            Exception: Re-raises any exception from the operation after rollback.
        """
        try:
            result = operation(self._session, *args, **kwargs)
            self._session.commit()
            return result
        except Exception:
            self._session.rollback()
            raise

    def ensure_consistency(self, operations: list[Callable[[Session], Any]]) -> list[Any]:
        """Execute multiple operations atomically.

        All operations share the same transaction. If any fails,
        all are rolled back.

        Args:
            operations: List of callables, each taking a Session.

        Returns:
            List of results from each operation.

        Raises:
            Exception: On first failure, rolls back all operations.
        """
        results: list[Any] = []
        try:
            for op in operations:
                results.append(op(self._session))
            self._session.commit()
            return results
        except Exception:
            self._session.rollback()
            raise
