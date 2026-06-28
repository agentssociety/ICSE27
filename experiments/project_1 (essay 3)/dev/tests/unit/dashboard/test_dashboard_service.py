from __future__ import annotations

import pytest
from datetime import datetime, timezone, timedelta
from src.domain.queue.Queue import Queue, QueueItem
from src.domain.urgency_level.UrgencyLevel import UrgencyLevel
from src.service.dashboard.dashboard_service import DashboardServiceImpl


class TestDashboardService:
    def test_get_item_wait_time_recent(self):
        """Test wait time for a recently added item."""
        service = DashboardServiceImpl()
        queue = Queue(items=[])
        now = datetime.now(timezone.utc)
        item = QueueItem(id="item1", urgency=UrgencyLevel(level=3), timestamp=now, queue=queue)
        
        wait_time = service.get_item_wait_time(item)
        assert wait_time >= 0
        assert wait_time < 1  # Less than 1 minute

    def test_get_item_wait_time_older(self):
        """Test wait time for an older item."""
        service = DashboardServiceImpl()
        queue = Queue(items=[])
        past_time = datetime.now(timezone.utc) - timedelta(minutes=30)
        item = QueueItem(id="item1", urgency=UrgencyLevel(level=3), timestamp=past_time, queue=queue)
        
        wait_time = service.get_item_wait_time(item)
        assert wait_time >= 29  # Should be approximately 30 minutes
        assert wait_time <= 31

    def test_get_dashboard_data_empty_queue(self):
        """Test dashboard data for an empty queue."""
        service = DashboardServiceImpl()
        queue = Queue(items=[])
        
        data = service.get_dashboard_data(queue)
        assert data["total_items"] == 0
        assert data["items"] == []
        assert data["next_patient"] is None

    def test_get_dashboard_data_with_items(self):
        """Test dashboard data with items in the queue."""
        service = DashboardServiceImpl()
        queue = Queue(items=[])
        
        now = datetime.now(timezone.utc)
        item1 = QueueItem(id="item1", urgency=UrgencyLevel(level=1), timestamp=now - timedelta(minutes=10), queue=queue)
        item2 = QueueItem(id="item2", urgency=UrgencyLevel(level=5), timestamp=now - timedelta(minutes=5), queue=queue)
        
        queue.addItem(item1)
        queue.addItem(item2)
        
        data = service.get_dashboard_data(queue)
        assert data["total_items"] == 2
        assert len(data["items"]) == 2
        
        # item2 has higher urgency, should be first
        assert data["items"][0]["item_id"] == "item2"
        assert data["items"][0]["urgency_level"] == 5
        assert data["items"][0]["urgency_label"] == "Highest"
        
        # item1 has lower urgency, should be second
        assert data["items"][1]["item_id"] == "item1"
        assert data["items"][1]["urgency_level"] == 1
        assert data["items"][1]["urgency_label"] == "Lowest"
        
        # Next patient should be the highest urgency item
        assert data["next_patient"]["item_id"] == "item2"

    def test_get_dashboard_data_same_urgency_sorted_by_time(self):
        """Test dashboard sorts by time when urgency is the same."""
        service = DashboardServiceImpl()
        queue = Queue(items=[])
        
        now = datetime.now(timezone.utc)
        item1 = QueueItem(id="early", urgency=UrgencyLevel(level=3), timestamp=now - timedelta(minutes=20), queue=queue)
        item2 = QueueItem(id="late", urgency=UrgencyLevel(level=3), timestamp=now - timedelta(minutes=5), queue=queue)
        
        queue.addItem(item1)
        queue.addItem(item2)
        
        data = service.get_dashboard_data(queue)
        # Same urgency, earlier time should be first
        assert data["items"][0]["item_id"] == "early"
        assert data["items"][1]["item_id"] == "late"
        
        # Earlier item should have longer wait time
        assert data["items"][0]["wait_time_minutes"] > data["items"][1]["wait_time_minutes"]

    def test_dashboard_with_naive_datetime(self):
        """Test dashboard works with naive datetimes (no timezone)."""
        service = DashboardServiceImpl()
        queue = Queue(items=[])
        
        naive_time = datetime(2024, 1, 15, 10, 0, 0)
        item = QueueItem(id="item1", urgency=UrgencyLevel(level=3), timestamp=naive_time, queue=queue)
        
        # Should not raise an error
        wait_time = service.get_item_wait_time(item)
        assert isinstance(wait_time, float)

    def test_dashboard_data_structure(self):
        """Test the structure of dashboard data."""
        service = DashboardServiceImpl()
        queue = Queue(items=[])
        
        now = datetime.now(timezone.utc)
        item = QueueItem(id="test_item", urgency=UrgencyLevel(level=4), timestamp=now, queue=queue)
        queue.addItem(item)
        
        data = service.get_dashboard_data(queue)
        
        # Check all required fields exist
        assert "total_items" in data
        assert "items" in data
        assert "next_patient" in data
        
        item_data = data["items"][0]
        assert "item_id" in item_data
        assert "urgency_level" in item_data
        assert "urgency_label" in item_data
        assert "wait_time_minutes" in item_data
        assert "timestamp" in item_data
