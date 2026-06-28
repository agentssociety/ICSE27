from __future__ import annotations
import pytest
from decimal import Decimal
from datetime import datetime
from unittest.mock import MagicMock, patch
from src.dto.flagged_transaction.flagged_transaction_dto import FlaggedTransactionResponse, FlaggedTransactionListResponse
from src.service.flagged_transaction.flagged_transaction_service import FlaggedTransactionService
from src.domain.flagged_transaction.FlaggedTransaction import FlaggedTransaction, FlagStatus, DetectionEngine
from src.infra.flagged_transaction.flagged_transaction_repo_impl import SQLAlchemyFlaggedTransactionRepository
class TestFlaggedTransactionService:
    def test_flag_withdrawal_triggers_flag(self) -> None:
        mock_session = MagicMock()
        service = FlaggedTransactionService(session=mock_session)
        now = datetime.utcnow()
        wds = [
            {'account_id': 'acc-001', 'amount': 100, 'timestamp': now},
            {'account_id': 'acc-001', 'amount': 100, 'timestamp': now},
            {'account_id': 'acc-001', 'amount': 100, 'timestamp': now},
            {'account_id': 'acc-001', 'amount': 100, 'timestamp': now},
        ]
        result = service.flag_withdrawal(
            withdrawal_id='wd-005',
            account_id='acc-001',
            amount=100,
            timestamp=now,
            all_withdrawals=wds,
        )
        assert result is not None
        assert result.status == FlagStatus.UNREVIEWED.value
        assert 'velocity' in result.reason
        mock_session.commit.assert_called()
    def test_flag_withdrawal_threshold(self) -> None:
        mock_session = MagicMock()
        service = FlaggedTransactionService(session=mock_session)
        result = service.flag_withdrawal(
            withdrawal_id='wd-big',
            account_id='acc-001',
            amount=25000,
            timestamp=datetime.utcnow(),
            all_withdrawals=[],
        )
        assert result is not None
        assert 'threshold' in result.reason
    def test_flag_withdrawal_no_flag(self) -> None:
        mock_session = MagicMock()
        service = FlaggedTransactionService(session=mock_session)
        result = service.flag_withdrawal(
            withdrawal_id='wd-normal',
            account_id='acc-001',
            amount=100,
            timestamp=datetime.utcnow(),
            all_withdrawals=[],
        )
        assert result is None
    def test_get_flagged_transactions(self) -> None:
        mock_session = MagicMock()
        service = FlaggedTransactionService(session=mock_session)
        result = service.get_flagged_transactions()
        assert result is not None
        assert isinstance(result, FlaggedTransactionListResponse)
    def test_get_flagged_transaction_by_id_not_found(self) -> None:
        mock_session = MagicMock()
        service = FlaggedTransactionService(session=mock_session)
        with patch.object(SQLAlchemyFlaggedTransactionRepository, 'get_by_id', return_value=None):
            result = service.get_flagged_transaction_by_id('nonexistent')
            assert result is None
    def test_review_flagged_transaction_updates_status(self) -> None:
        mock_session = MagicMock()
        service = FlaggedTransactionService(session=mock_session)
        flagged = FlaggedTransaction.create(withdrawal_id='wd-001', reason='threshold')
        dto = FlaggedTransactionResponse(
            id=flagged.id,
            withdrawal_id=flagged.withdrawal_id,
            reason=flagged.reason,
            flagged_at=flagged.flagged_at,
            reviewed_by=None,
            status=flagged.status.value,
        )
        with patch.object(service._repo, 'get_by_id', return_value=dto):
            with patch.object(service._repo, 'update_review', return_value=FlaggedTransactionResponse(
                id=flagged.id,
                withdrawal_id=flagged.withdrawal_id,
                reason=flagged.reason,
                flagged_at=flagged.flagged_at,
                reviewed_by='reviewer-01',
                status='reviewed',
            )):
                result = service.review_flagged_transaction(transaction_id=flagged.id, reviewer_id='reviewer-01')
                assert result is not None
                assert result.status == 'reviewed'
                assert result.reviewed_by == 'reviewer-01'
