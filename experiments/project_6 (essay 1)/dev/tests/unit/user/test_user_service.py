from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from src.dto.user.user_dto import RegistrationRequest, UserResponse, UserUpdate
from src.service.user.user_service import UserServiceImpl


class TestUserServiceImpl:
    def test_register_creates_user(self) -> None:
        mock_repo = MagicMock()
        mock_repo.find_by_email.return_value = None
        mock_repo.create.return_value = UserResponse(id=1, email="n@e.com", name="N", accountStatus="pending", isAuthenticated=False)
        svc = UserServiceImpl(repo=mock_repo)
        resp = svc.register(RegistrationRequest(email="n@e.com", password="pw", name="N"))
        assert resp.email == "n@e.com"

    def test_register_raises_on_duplicate(self) -> None:
        mock_repo = MagicMock()
        mock_repo.find_by_email.return_value = UserResponse(id=1, email="x@y.com", name="X", accountStatus="active", isAuthenticated=True)
        svc = UserServiceImpl(repo=mock_repo)
        with pytest.raises(ValueError):
            svc.register(RegistrationRequest(email="x@y.com", password="pw", name="X"))

    def test_soft_delete_sets_account_status_deleted(self) -> None:
        mock_repo = MagicMock()
        mock_repo.update.return_value = UserResponse(id=1, email="u@t.com", name="U", accountStatus="deleted", isAuthenticated=False)
        svc = UserServiceImpl(repo=mock_repo)
        result = svc.soft_delete(1)
        assert result is not None
        assert result.accountStatus == "deleted"

    def test_recover_sets_account_status_active(self) -> None:
        mock_repo = MagicMock()
        mock_repo.update.return_value = UserResponse(id=1, email="u@t.com", name="U", accountStatus="active", isAuthenticated=False)
        svc = UserServiceImpl(repo=mock_repo)
        result = svc.recover(1)
        assert result is not None
        assert result.accountStatus == "active"

    def test_get_by_id(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = UserResponse(id=1, email="a@b.com", name="A", accountStatus="active", isAuthenticated=True)
        svc = UserServiceImpl(repo=mock_repo)
        assert svc.get_by_id(1).email == "a@b.com"

    def test_delete(self) -> None:
        mock_repo = MagicMock()
        mock_repo.delete.return_value = True
        svc = UserServiceImpl(repo=mock_repo)
        assert svc.delete(1) is True
