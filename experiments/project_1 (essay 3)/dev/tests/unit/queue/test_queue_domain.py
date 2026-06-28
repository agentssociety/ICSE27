from __future__ import annotations

import pytest
from datetime import datetime
from src.domain.queue.Queue import Queue, QueueItem
from src.domain.urgency_level.UrgencyLevel import UrgencyLevel


class TestQueueDomain:
    def test_create_queue(self):
        """Test creating an empty queue."""
        queue = Queue(items=[])
        assert len(queue.items) == 0

    def test_create_queue_item(self):
        """Test creating a queue item."""
        queue = Queue(items=[])
        urgency = UrgencyLevel(level=3)
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        item = QueueItem(id="item1", urgency=urgency, timestamp=timestamp, queue=queue)
        assert item.id == "item1"
        assert item.urgency.level == 3
        assert item.timestamp == timestamp
        assert item.queue == queue

    def test_add_item_to_queue(self):
        """Test adding an item to the queue maintains sort order."""
        queue = Queue(items=[])
        urgency1 = UrgencyLevel(level=2)
        urgency2 = UrgencyLevel(level=5)
        urgency3 = UrgencyLevel(level=3)
        
        item1 = QueueItem(id="item1", urgency=urgency1, timestamp=datetime(2024, 1, 15, 10, 0, 0), queue=queue)
        item2 = QueueItem(id="item2", urgency=urgency2, timestamp=datetime(2024, 1, 15, 10, 5, 0), queue=queue)
        item3 = QueueItem(id="item3", urgency=urgency3, timestamp=datetime(2024, 1, 15, 10, 10, 0), queue=queue)
        
        queue.addItem(item1)
        queue.addItem(item2)
        queue.addItem(item3)
        
        # Should be sorted by urgency descending: item2 (5), item3 (3), item1 (2)
        assert queue.items[0].id == "item2"
        assert queue.items[1].id == "item3"
        assert queue.items[2].id == "item1"

    def test_sort_items_by_urgency_then_time(self):
        """Test sorting by urgency (desc) then by time (asc)."""
        queue = Queue(items=[])
        urgency_high = UrgencyLevel(level=5)
        urgency_low = UrgencyLevel(level=1)
        
        item1 = QueueItem(id="item1", urgency=urgency_low, timestamp=datetime(2024, 1, 15, 9, 0, 0), queue=queue)
        item2 = QueueItem(id="item2", urgency=urgency_high, timestamp=datetime(2024, 1, 15, 10, 0, 0), queue=queue)
        item3 = QueueItem(id="item3", urgency=urgency_high, timestamp=datetime(2024, 1, 15, 8, 0, 0), queue=queue)
        
        sorted_items = queue.sortItems([item1, item2, item3])
        
        # item3 (urgency 5, earlier time) should be first, then item2 (urgency 5, later time), then item1 (urgency 1)
        assert sorted_items[0].id == "item3"
        assert sorted_items[1].id == "item2"
        assert sorted_items[2].id == "item1"

    def test_find_item_by_id(self):
        """Test finding an item by its ID."""
        queue = Queue(items=[])
        urgency = UrgencyLevel(level=3)
        item = QueueItem(id="findme", urgency=urgency, timestamp=datetime.now(), queue=queue)
        queue.addItem(item)
        
        found = queue.findItemById("findme")
        assert found.id == "findme"
        
        with pytest.raises(ValueError):
            queue.findItemById("nonexistent")

    def test_remove_item(self):
        """Test removing an item from the queue."""
        queue = Queue(items=[])
        urgency = UrgencyLevel(level=3)
        item = QueueItem(id="remove_me", urgency=urgency, timestamp=datetime.now(), queue=queue)
        queue.addItem(item)
        assert len(queue.items) == 1
        
        removed = queue.removeItem("remove_me")
        assert removed.id == "remove_me"
        assert len(queue.items) == 0

    def test_get_next_patient(self):
        """Test getting the next patient (highest urgency, earliest time)."""
        queue = Queue(items=[])
        urgency_low = UrgencyLevel(level=1)
        urgency_high = UrgencyLevel(level=5)
        
        item1 = QueueItem(id="low_urg", urgency=urgency_low, timestamp=datetime(2024, 1, 15, 10, 0, 0), queue=queue)
        item2 = QueueItem(id="high_urg_early", urgency=urgency_high, timestamp=datetime(2024, 1, 15, 9, 0, 0), queue=queue)
        item3 = QueueItem(id="high_urg_late", urgency=urgency_high, timestamp=datetime(2024, 1, 15, 11, 0, 0), queue=queue)
        
        queue.addItem(item1)
        queue.addItem(item2)
        queue.addItem(item3)
        
        next_item = queue.getNextPatient()
        assert next_item.id == "high_urg_early"

    def test_get_next_patient_empty_queue(self):
        """Test getting next patient from empty queue raises error."""
        queue = Queue(items=[])
        with pytest.raises(ValueError, match="empty"):
            queue.getNextPatient()

    def test_reorder_on_urgency_change(self):
        """Test reordering when urgency changes."""
        queue = Queue(items=[])
        urgency_low = UrgencyLevel(level=1)
        urgency_high = UrgencyLevel(level=5)
        
        item1 = QueueItem(id="item1", urgency=urgency_low, timestamp=datetime(2024, 1, 15, 10, 0, 0), queue=queue)
        item2 = QueueItem(id="item2", urgency=urgency_high, timestamp=datetime(2024, 1, 15, 9, 0, 0), queue=queue)
        
        queue.addItem(item1)
        queue.addItem(item2)
        
        # item1 was last, now change its urgency to highest
        queue.reorderOnUrgencyChange("item1", UrgencyLevel(level=5))
        
        # item1 should now be first (same urgency as item2, but item2 has earlier time)
        assert queue.items[0].id == "item2"
        assert queue.items[1].id == "item1"

    def test_update_urgency(self):
        """Test updating urgency on a queue item."""
        queue = Queue(items=[])
        urgency = UrgencyLevel(level=2)
        item = QueueItem(id="item1", urgency=urgency, timestamp=datetime.now(), queue=queue)
        
        assert item.urgency.level == 2
        item.updateUrgency(UrgencyLevel(level=5))
        assert item.urgency.level == 5

    def test_compare_urgency(self):
        """Test comparing urgency between two items."""
        queue = Queue(items=[])
        item1 = QueueItem(id="a", urgency=UrgencyLevel(level=1), timestamp=datetime.now(), queue=queue)
        item2 = QueueItem(id="b", urgency=UrgencyLevel(level=5), timestamp=datetime.now(), queue=queue)
        
        # item2 has higher urgency, so compareUrgency should return 1 (item2 > item1)
        assert item1.compareUrgency(item1, item2) == 1
        assert item1.compareUrgency(item2, item1) == -1
        assert item1.compareUrgency(item1, item1) == 0

    def test_compare_timestamp(self):
        """Test comparing timestamps between two items."""
        queue = Queue(items=[])
        item1 = QueueItem(id="a", urgency=UrgencyLevel(level=3), timestamp=datetime(2024, 1, 15, 9, 0, 0), queue=queue)
        item2 = QueueItem(id="b", urgency=UrgencyLevel(level=3), timestamp=datetime(2024, 1, 15, 10, 0, 0), queue=queue)
        
        assert item1.compareTimestamp(item1, item2) == -1
        assert item1.compareTimestamp(item2, item1) == 1
        assert item1.compareTimestamp(item1, item1) == 0

    def test_compare_id(self):
        """Test comparing IDs between two items."""
        queue = Queue(items=[])
        item1 = QueueItem(id="aaa", urgency=UrgencyLevel(level=3), timestamp=datetime.now(), queue=queue)
        item2 = QueueItem(id="bbb", urgency=UrgencyLevel(level=3), timestamp=datetime.now(), queue=queue)
        
        assert item1.compareId(item1, item2) == -1
        assert item1.compareId(item2, item1) == 1
        assert item1.compareId(item1, item1) == 0
