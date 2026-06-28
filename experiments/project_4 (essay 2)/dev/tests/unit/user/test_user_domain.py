from __future__ import annotations

import pytest
from src.domain.user.User import Actor, Permission, User, Credential, Digit, State

"""
Unit tests for User across domain, service, and API layers

Related tasks: #88, #89, #93, #94, #95
"""


def test_actor_get_by_card() -> None:
    actor = Actor(mayPerform={Permission.READ})
    result = actor.getActorByCard("card123")
    assert result is not None
    assert Permission.READ in result.mayPerform


def test_actor_may_perform_with_admin() -> None:
    actor = Actor(mayPerform={Permission.ADMIN})
    assert actor.checkPermission(None) is True


def test_actor_may_perform_without_admin() -> None:
    actor = Actor(mayPerform={Permission.READ})
    assert actor.checkPermission(None) is False


def test_user_creation() -> None:
    user = User(userId="u1", account="acc1", loginSession="sess1", account_owns=None)  # type: ignore
    assert user.userId == "u1"
    assert user.account == "acc1"
    assert user.loginSession == "sess1"
    assert user.transactions == []


def test_credential_get_credential() -> None:
    actor = Actor(mayPerform={Permission.READ})
    cred = Credential(actor=actor, pin=None)  # type: ignore
    result = cred.getCredential(actor)
    assert result.actor == actor


def test_digit_transition() -> None:
    digit = Digit(pin=None)  # type: ignore
    assert digit.transition(State.PRE1, State.POST1) is True
