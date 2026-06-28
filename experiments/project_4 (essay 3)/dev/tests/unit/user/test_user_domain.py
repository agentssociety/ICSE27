from __future__ import annotations

import pytest
from datetime import datetime
from src.domain.user.User import User, UserRole, UserStatus


class TestUserDomain:

    def test_create_regular_user(self) -> None:
        user = User.create(
            username="john_doe",
            email="john@example.com",
            password_hash="hashed_password_123",
            role=UserRole.REGULAR_USER,
        )
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.password_hash == "hashed_password_123"
        assert user.role == UserRole.REGULAR_USER
        assert user.status == UserStatus.ACTIVE
        assert user.id is not None
        assert len(user.id) > 0
        assert user.created_at is not None
        assert user.updated_at is not None
        assert user.is_admin() is False
        assert user.is_active() is True

    def test_create_admin_user(self) -> None:
        user = User.create(
            username="admin_user",
            email="admin@bank.com",
            password_hash="admin_hash",
            role=UserRole.ADMIN,
        )
        assert user.role == UserRole.ADMIN
        assert user.is_admin() is True

    def test_create_with_empty_username_raises(self) -> None:
        with pytest.raises(ValueError, match="Username is required"):
            User.create(
                username="",
                email="test@test.com",
                password_hash="hash",
            )

    def test_create_with_invalid_email_raises(self) -> None:
        with pytest.raises(ValueError, match="Valid email is required"):
            User.create(
                username="testuser",
                email="notanemail",
                password_hash="hash",
            )

    def test_create_with_empty_password_hash_raises(self) -> None:
        with pytest.raises(ValueError, match="Password hash is required"):
            User.create(
                username="testuser",
                email="test@test.com",
                password_hash="",
            )

    def test_update_user(self) -> None:
        user = User.create(
            username="original",
            email="orig@test.com",
            password_hash="hash1",
        )
        user.update(username="updated", email="new@test.com")
        assert user.username == "updated"
        assert user.email == "new@test.com"
        assert user.updated_at > user.created_at

    def test_deactivate_user(self) -> None:
        user = User.create(
            username="active_user",
            email="active@test.com",
            password_hash="hash",
        )
        assert user.is_active() is True
        user.deactivate()
        assert user.is_active() is False
        assert user.status == UserStatus.INACTIVE

    def test_activate_user(self) -> None:
        user = User.create(
            username="inactive_user",
            email="inactive@test.com",
            password_hash="hash",
        )
        user.deactivate()
        assert user.is_active() is False
        user.activate()
        assert user.is_active() is True
        assert user.status == UserStatus.ACTIVE

    def test_update_role(self) -> None:
        user = User.create(
            username="normal",
            email="normal@test.com",
            password_hash="hash",
            role=UserRole.REGULAR_USER,
        )
        assert user.is_admin() is False
        user.update(role=UserRole.ADMIN)
        assert user.is_admin() is True
