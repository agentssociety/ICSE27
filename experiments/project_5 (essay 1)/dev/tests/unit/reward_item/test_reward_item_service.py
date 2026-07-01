from __future__ import annotations

import pytest
from src.service.reward_item.reward_item_service import RewardItemService


class TestRewardItemService:
    def test_get_all_items_empty(self) -> None:
        svc = RewardItemService()
        assert svc.get_all_items() == []

    def test_get_item_by_id_none(self) -> None:
        svc = RewardItemService()
        assert svc.get_item_by_id("item_1") is None

    def test_create_item(self) -> None:
        svc = RewardItemService()
        result = svc.create_item("Book", 50.0, "A great book")
        assert result["name"] == "Book"
        assert result["cost"] == 50.0
        assert result["description"] == "A great book"

    def test_create_item_default_description(self) -> None:
        svc = RewardItemService()
        result = svc.create_item("Pen", 10.0)
        assert result["description"] == ""
