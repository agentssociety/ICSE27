from __future__ import annotations

import pytest
from datetime import datetime
from src.api.queue.queue_router import QueueRouter


class TestQueueRouter:
    def test_create_queue(self):
        """Test creating a queue via the router."""
        router = QueueRouter()
        result = router.create_queue("queue1")
        assert result["queue_id"] == "queue1"
        assert result["status"] == "created"

    def test_add_item(self):
        """Test adding an item to a queue via the router."""
        router = QueueRouter()
        router.create_queue("queue1")
        
        result = router.add_item("queue1", "item1", 3, "2024-01-15T10:00:00")
        assert result["item_id"] == "item1"
        assert result["urgency_level"] == 3
        assert result["status"] == "added"

    def test_add_item_nonexistent_queue(self):
        """Test adding item to nonexistent queue returns error."""
        router = QueueRouter()
        result = router.add_item("nonexistent", "item1", 3, "2024-01-15T10:00:00")
        assert "error" in result

    def test_get_next(self):
        """Test getting the next item from the queue."""
        router = QueueRouter()
        router.create_queue("queue1")
        router.add_item("queue1", "low", 1, "2024-01-15T10:00:00")
        router.add_item("queue1", "high", 5, "2024-01-15T09:00:00")
        
        result = router.get_next("queue1")
        assert result["item_id"] == "high"
        assert result["urgency_level"] == 5

    def test_get_next_empty_queue(self):
        """Test getting next from empty queue returns error."""
        router = QueueRouter()
        router.create_queue("queue1")
        
        result = router.get_next("queue1")
        assert "error" in result

    def test_get_next_nonexistent_queue(self):
        """Test getting next from nonexistent queue returns error."""
        router = QueueRouter()
        result = router.get_next("nonexistent")
        assert "error" in result

    def test_update_urgency(self):
        """Test updating urgency of an item."""
        router = QueueRouter()
        router.create_queue("queue1")
        router.add_item("queue1", "item1", 1, "2024-01-15T10:00:00")
        
        result = router.update_urgency("queue1", "item1", 5)
        assert result["item_id"] == "item1"
        assert result["new_urgency_level"] == 5
        assert result["status"] == "updated"

    def test_update_urgency_nonexistent_queue(self):
        """Test updating urgency on nonexistent queue returns error."""
        router = QueueRouter()
        result = router.update_urgency("nonexistent", "item1", 5)
        assert "error" in result

    def test_update_urgency_nonexistent_item(self):
        """Test updating urgency on nonexistent item returns error."""
        router = QueueRouter()
        router.create_queue("queue1")
        result = router.update_urgency("queue1", "nonexistent", 5)
        assert "error" in result

    def test_remove_item(self):
        """Test removing an item from the queue."""
        router = QueueRouter()
        router.create_queue("queue1")
        router.add_item("queue1", "item1", 3, "2024-01-15T10:00:00")
        
        result = router.remove_item("queue1", "item1")
        assert result["item_id"] == "item1"
        assert result["status"] == "removed"

    def test_remove_item_nonexistent_queue(self):
        """Test removing item from nonexistent queue returns error."""
        router = QueueRouter()
        result = router.remove_item("nonexistent", "item1")
        assert "error" in result

    def test_list_queue(self):
        """Test listing all items in a queue."""
        router = QueueRouter()
        router.create_queue("queue1")
        router.add_item("queue1", "item1", 1, "2024-01-15T10:00:00")
        router.add_item("queue1", "item2", 5, "2024-01-15T09:00:00")
        
        result = router.list_queue("queue1")
        assert result["queue_id"] == "queue1"
        assert len(result["items"]) == 2
        # Should be sorted: item2 (urgency 5) first, then item1 (urgency 1)
        assert result["items"][0]["item_id"] == "item2"
        assert result["items"][1]["item_id"] == "item1"

    def test_list_queue_nonexistent(self):
        """Test listing nonexistent queue returns error."""
        router = QueueRouter()
        result = router.list_queue("nonexistent")
        assert "error" in result
