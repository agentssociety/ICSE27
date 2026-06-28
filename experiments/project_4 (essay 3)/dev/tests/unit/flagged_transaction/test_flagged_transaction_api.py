from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from src.api.flagged_transaction.flagged_transaction_router import router
from src.dto.flagged_transaction.flagged_transaction_dto import FlaggedTransactionResponse, FlaggedTransactionListResponse, FlagReviewRequest
class TestFlaggedTransactionAPI:
    def test_router_exists(self) -> None:
        assert router is not None
        assert len(router.routes) > 0
    def test_list_endpoint_exists(self) -> None:
        from src.api.flagged_transaction.flagged_transaction_router import list_flagged_transactions
        assert list_flagged_transactions is not None
    def test_get_endpoint_exists(self) -> None:
        from src.api.flagged_transaction.flagged_transaction_router import get_flagged_transaction
        assert get_flagged_transaction is not None
    def test_review_endpoint_exists(self) -> None:
        from src.api.flagged_transaction.flagged_transaction_router import review_flagged_transaction
        assert review_flagged_transaction is not None
    def test_flag_review_request_validates(self) -> None:
        req = FlagReviewRequest(reviewer_id='admin-001')
        assert req.reviewer_id == 'admin-001'
    def test_flag_review_request_requires_reviewer_id(self) -> None:
        with pytest.raises(ValueError):
            FlagReviewRequest()
