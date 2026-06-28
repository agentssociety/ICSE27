from __future__ import annotations

import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock

from src.service.withdrawal_transaction.withdrawal_transaction_service import WithdrawalTransactionServiceImpl
from src.dto.withdrawal_transaction.withdrawal_transaction_dto import WithdrawalResponse
from src.domain.withdrawal_transaction.WithdrawalTransaction import WithdrawalStatus


class TestWithdrawalTransactionService:

    def test_happy_path_withdrawal(self) -> None:
        """Test that a valid withdrawal succeeds end-to-end."""
        # Setup mock session
        mock_session = MagicMock()
        
        # Create a mock ORM row that represents an account
        mock_account_orm = MagicMock()
        mock_account_orm.id = 1
        mock_account_orm.account_id = 'acc-001'
        mock_account_orm.balance = 1000.0
        mock_account_orm.locked = False
        mock_account_orm.failed_attempt_count = 0
        
        # Set up the query chain to return this mock
        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_account_orm
        
        # Create service
        service = WithdrawalTransactionServiceImpl(session=mock_session)
        
        # Call method
        result = service.create_withdrawal(
            account_id='acc-001',
            amount=Decimal('100.00')
        )
        
        assert result is not None
        assert result.status == WithdrawalStatus.COMPLETED.value
        assert result.account_id == 'acc-001'
        
        # Verify that session.commit was called
        mock_session.commit.assert_called_once()
        mock_session.flush.assert_called()

    def test_insufficient_funds_raises_error(self) -> None:
        """Test that insufficient funds causes rollback."""
        mock_session = MagicMock()
        
        # Account with low balance
        mock_account_orm = MagicMock()
        mock_account_orm.id = 1
        mock_account_orm.account_id = 'acc-001'
        mock_account_orm.balance = 50.0
        
        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_account_orm
        
        service = WithdrawalTransactionServiceImpl(session=mock_session)
        
        with pytest.raises(ValueError, match='Insufficient'):
            service.create_withdrawal(
                account_id='acc-001',
                amount=Decimal('100.00')
            )
        
        # Verify rollback was called
        mock_session.rollback.assert_called_once()
