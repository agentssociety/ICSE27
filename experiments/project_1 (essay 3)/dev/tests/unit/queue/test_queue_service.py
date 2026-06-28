from __future__ import annotations

import pytest
from datetime import datetime
from src.domain.queue.Queue import Queue, QueueItem
from src.domain.urgency_level.UrgencyLevel import UrgencyLevel
from src.service.queue.queue_service import QueueServiceImpl


class TestQueueService:
    def test_create_queue(self):
        """Test creating a new queue."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        assert isinstance(queue, Queue)
        assert len(queue.items) == 0

    def test_add_item_to_queue(self):
        """Test adding an item to the queue."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        timestamp = datetime(2024, 1, 15, 10, 0, 0)
        
        item = service.add_item_to_queue(queue, "item1", 3, timestamp)
        assert item.id == "item1"
        assert item.urgency.level == 3
        assert item.timestamp == timestamp
        assert len(queue.items) == 1

    def test_add_multiple_items_sorted(self):
        """Test adding multiple items maintains sort order."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        service.add_item_to_queue(queue, "low", 1, datetime(2024, 1, 15, 10, 0, 0))
        service.add_item_to_queue(queue, "high", 5, datetime(2024, 1, 15, 9, 0, 0))
        service.add_item_to_queue(queue, "medium", 3, datetime(2024, 1, 15, 11, 0, 0))
        
        # Should be sorted: high (5), medium (3), low (1)
        assert queue.items[0].id == "high"
        assert queue.items[1].id == "medium"
        assert queue.items[2].id == "low"

    def test_get_next_item(self):
        """Test getting the next item from the queue."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        service.add_item_to_queue(queue, "item1", 1, datetime(2024, 1, 15, 10, 0, 0))
        service.add_item_to_queue(queue, "item2", 5, datetime(2024, 1, 15, 9, 0, 0))
        
        next_item = service.get_next_item(queue)
        assert next_item.id == "item2"

    def test_get_next_item_empty_queue(self):
        """Test getting next item from empty queue raises error."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        with pytest.raises(ValueError, match="empty"):
            service.get_next_item(queue)

    def test_update_item_urgency(self):
        """Test updating urgency of an item."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        service.add_item_to_queue(queue, "item1", 1, datetime(2024, 1, 15, 10, 0, 0))
        service.add_item_to_queue(queue, "item2", 5, datetime(2024, 1, 15, 9, 0, 0))
        
        # Change item1 urgency to 5
        service.update_item_urgency(queue, "item1", 5)
        
        # item2 has earlier time, so should still be first
        assert queue.items[0].id == "item2"
        assert queue.items[1].id == "item1"
        assert queue.items[1].urgency.level == 5

    def test_update_item_urgency_reorders(self):
        """Test that updating urgency reorders the queue."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        service.add_item_to_queue(queue, "item1", 1, datetime(2024, 1, 15, 10, 0, 0))
        service.add_item_to_queue(queue, "item2", 3, datetime(2024, 1, 15, 9, 0, 0))
        
        # item1 was last, now make it highest urgency
        service.update_item_urgency(queue, "item1", 5)
        
        # item1 should now be first
        assert queue.items[0].id == "item1"
        assert queue.items[0].urgency.level == 5

    def test_remove_item(self):
        """Test removing an item from the queue."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        service.add_item_to_queue(queue, "item1", 3, datetime(2024, 1, 15, 10, 0, 0))
        service.add_item_to_queue(queue, "item2", 5, datetime(2024, 1, 15, 9, 0, 0))
        
        removed = service.remove_item(queue, "item1")
        assert removed.id == "item1"
        assert len(queue.items) == 1
        assert queue.items[0].id == "item2"

    def test_remove_nonexistent_item(self):
        """Test removing a nonexistent item raises error."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        with pytest.raises(ValueError):
            service.remove_item(queue, "nonexistent")

    def test_invalid_urgency_level(self):
        """Test that invalid urgency levels are rejected."""
        service = QueueServiceImpl()
        queue = service.create_queue()
        
        with pytest.raises(ValueError):
            service.add_item_to_queue(queue, "item1", 0, datetime.now())
        
        with pytest.raises(ValueError):
            service.add_item_to_queue(queue, "item2", 6, datetime.now())
