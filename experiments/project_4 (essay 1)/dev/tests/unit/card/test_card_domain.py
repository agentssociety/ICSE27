from __future__ import annotations

import pytest
from src.domain.card import Card, CardId, CardCreatedEvent, CardUpdatedEvent, Actor, AccountState, Permission


class TestCardDomain:
    def test_card_validation(self) -> None:
        actor = Actor(mayPerform={Permission.READ}, id="actor1", name="Test Actor")
        card = Card(owner=actor)
        assert card.validate("test_data") is True
