from __future__ import annotations

import pytest
from src.service.reward_store.reward_store_service import RewardStoreService


class TestRewardStoreService:
    def test_get_store_none(self) -> None:
        svc = RewardStoreService()
        assert svc.get_store("store_1") is None

    def test_list_available_items_empty(self) -> None:
        svc = RewardStoreService()
        assert svc.list_available_items() == []

    def test_add_item_to_store(self) -> None:
        svc = RewardStoreService()
        svc.add_item_to_store("store_1", {"name": "Book"})  # Should not raise
