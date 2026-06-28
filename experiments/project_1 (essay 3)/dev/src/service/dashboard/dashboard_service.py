from __future__ import annotations

from typing import Any, Protocol
from datetime import datetime, timezone

"""
Service layer for the Dashboard domain class

Package: service.dashboard
Layer: service
Related tasks: #58
Requirement coverage:
- Real-time live dashboard displaying urgency and wait time
"""

from src.domain.queue.Queue import Queue, QueueItem
from src.domain.urgency_level.UrgencyLevel import UrgencyLevel


class DashboardService(Protocol):
    """Protocol for dashboard service operations."""
    def get_dashboard_data(self, queue: Queue) -> dict:
        ...
    
    def get_item_wait_time(self, item: QueueItem) -> float:
        ...


class DashboardServiceImpl:
    """Implementation of dashboard service providing real-time queue status."""

    def __init__(self) -> None:
        pass

    def get_item_wait_time(self, item: QueueItem) -> float:
        """Calculate wait time in minutes since the item was added."""
        now = datetime.now(timezone.utc)
        # Handle both timezone-aware and naive datetimes
        item_time = item.timestamp
        if item_time.tzinfo is None:
            item_time = item_time.replace(tzinfo=timezone.utc)
        delta = now - item_time
        return delta.total_seconds() / 60.0

    def get_dashboard_data(self, queue: Queue) -> dict:
        """Get the current dashboard data for a queue."""
        sorted_items = queue.sortItems(queue.items)
        
        items_data = []
        for item in sorted_items:
            wait_time = self.get_item_wait_time(item)
            items_data.append({
                "item_id": item.id,
                "urgency_level": item.urgency.level,
                "urgency_label": item.urgency.label,
                "wait_time_minutes": round(wait_time, 1),
                "timestamp": item.timestamp.isoformat() if hasattr(item.timestamp, 'isoformat') else str(item.timestamp),
            })
        
        return {
            "total_items": len(sorted_items),
            "items": items_data,
            "next_patient": items_data[0] if items_data else None,
        }
