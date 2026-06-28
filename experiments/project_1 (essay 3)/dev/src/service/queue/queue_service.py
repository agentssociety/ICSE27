from __future__ import annotations

from typing import Any, Protocol, Optional
from datetime import datetime

"""
Service layer for the Queue domain class

Package: service.queue
Layer: service
Related tasks: #55, #56, #57, #58
Requirement coverage:
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
- Real-time live dashboard displaying urgency and wait time
"""

from src.domain.queue.Queue import Queue, QueueItem
from src.domain.urgency_level.UrgencyLevel import UrgencyLevel


class QueueService(Protocol):
    """Protocol for queue service operations."""
    def create_queue(self) -> Queue:
        ...
    
    def add_item_to_queue(self, queue: Queue, item_id: str, urgency_level: int, timestamp: datetime) -> QueueItem:
        ...
    
    def get_next_item(self, queue: Queue) -> QueueItem:
        ...
    
    def update_item_urgency(self, queue: Queue, item_id: str, new_urgency_level: int) -> None:
        ...
    
    def remove_item(self, queue: Queue, item_id: str) -> QueueItem:
        ...


class QueueServiceImpl:
    """Implementation of queue service."""

    def __init__(self) -> None:
        pass

    def create_queue(self) -> Queue:
        return Queue(items=[])

    def add_item_to_queue(self, queue: Queue, item_id: str, urgency_level: int, timestamp: datetime) -> QueueItem:
        urgency = UrgencyLevel(level=urgency_level)
        item = QueueItem(
            id=item_id,
            urgency=urgency,
            timestamp=timestamp,
            queue=queue,
        )
        queue.addItem(item)
        return item

    def get_next_item(self, queue: Queue) -> QueueItem:
        return queue.getNextPatient()

    def update_item_urgency(self, queue: Queue, item_id: str, new_urgency_level: int) -> None:
        new_urgency = UrgencyLevel(level=new_urgency_level)
        queue.reorderOnUrgencyChange(item_id, new_urgency)

    def remove_item(self, queue: Queue, item_id: str) -> QueueItem:
        return queue.removeItem(item_id)
