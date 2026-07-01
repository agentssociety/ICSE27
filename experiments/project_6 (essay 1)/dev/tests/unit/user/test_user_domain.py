from __future__ import annotations

import pytest
from src.domain.user.User import UserAccount, AccountStatus, EmailConfirmation, Actor, Permission, User, UserCreatedEvent, UserUpdatedEvent


class TestUserAccount:
    def test_create_user_account_with_pending_status(self) -> None:
        actor = Actor(mayPerform={Permission.WRITE})
        account = UserAccount(email="test@example.com", password="hashed_pw", status=AccountStatus.PENDING, owner=actor, accessible={actor})
        assert account.email == "test@example.com"
        assert account.status == AccountStatus.PENDING

    def test_check_status_returns_correct_status(self) -> None:
        actor = Actor(mayPerform={Permission.WRITE})
        account = UserAccount(email="test@example.com", password="pw", status=AccountStatus.PENDING, owner=actor, accessible={actor})
        assert account.checkStatus() == AccountStatus.PENDING

    def test_set_status_updates_status(self) -> None:
        actor = Actor(mayPerform={Permission.WRITE})
        account = UserAccount(email="test@example.com", password="pw", status=AccountStatus.PENDING, owner=actor, accessible={actor})
        account.setStatus(AccountStatus.VERIFIED)
        assert account.status == AccountStatus.VERIFIED


class TestActor:
    def test_check_permission_returns_true_when_allowed(self) -> None:
        actor = Actor(mayPerform={Permission.WRITE})
        assert actor.checkPermission(actor, Permission.WRITE) is True

    def test_check_permission_returns_false_when_not_allowed(self) -> None:
        actor = Actor(mayPerform={Permission.READ})
        assert actor.checkPermission(actor, Permission.WRITE) is False


class TestEmailConfirmation:
    def test_create_sets_sent_to_true(self) -> None:
        actor = Actor(mayPerform=set())
        account = UserAccount(email="a@b.com", password="pw", status=AccountStatus.PENDING, owner=actor, accessible=set())
        confirmation = EmailConfirmation(sent=False)
        confirmation.create(account, None)
        assert confirmation.sent is True


class TestUser:
    def _make_user(self) -> User:
        return User(
            loggedIn=True, role=None, userId="1", isAuthenticated=True, id="1",
            authentication_status=None, identity="test", onlineStatus=None,
            abstract_mustBeLoggedIn=True, abstract_cannotSendRequestToSelf_recipient=None,
            mayPerform=set(), username="test", field_isLoggedIn=True, loginStatus=None,
            rolePermissions=[], passwordHash="", email="test@example.com",
            accountStatus="active", permissions=[], name="Test",
            notificationEnabled=True
        )

    def test_validate_email_format_valid(self) -> None:
        user = self._make_user()
        assert user.validateEmailFormat("valid@example.com") is True
        assert user.validateEmailFormat("invalid") is False

    def test_is_logged_in(self) -> None:
        user = self._make_user()
        assert user.isLoggedIn() is True
