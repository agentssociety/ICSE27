from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from src.service.user.admin_service import AdminService


class TestAdminService:

    def test_list_all_withdrawals_not_admin(self) -> None:
        mock_session = MagicMock()
        service = AdminService(session=mock_session)

        # This should raise PermissionError because the user doesn't exist
        with pytest.raises(PermissionError, match="User not found"):
            service.list_all_withdrawals(admin_user_id="nonexistent_user")

    def test_list_all_flagged_not_admin(self) -> None:
        mock_session = MagicMock()
        service = AdminService(session=mock_session)

        with pytest.raises(PermissionError, match="User not found"):
            service.list_all_flagged_transactions(admin_user_id="nonexistent_user")

    def test_get_withdrawal_detail_not_admin(self) -> None:
        mock_session = MagicMock()
        service = AdminService(session=mock_session)

        with pytest.raises(PermissionError, match="User not found"):
            service.get_withdrawal_detail(
                admin_user_id="nonexistent",
                withdrawal_id="wd-001",
            )

    def test_review_flagged_transaction_not_admin(self) -> None:
        mock_session = MagicMock()
        service = AdminService(session=mock_session)

        with pytest.raises(PermissionError, match="User not found"):
            service.review_flagged_transaction(
                admin_user_id="nonexistent",
                flagged_id="fl-001",
            )
