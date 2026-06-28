from __future__ import annotations

from typing import Any
from datetime import datetime

"""
Api layer for the Queue domain class

Package: api.queue
Layer: api
Related tasks: #55, #56, #57, #58
Requirement coverage:
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
- Real-time live dashboard displaying urgency and wait time
"""

from src.domain.queue.Queue import Queue, QueueItem
from src.service.queue.queue_service import QueueServiceImpl


class QueueRouter:
    """Router for queue-related API endpoints."""

    def __init__(self) -> None:
        self._service = QueueServiceImpl()
        self._queues: dict[str, Queue] = {}

    def create_queue(self, queue_id: str) -> dict:
        queue = self._service.create_queue()
        self._queues[queue_id] = queue
        return {"queue_id": queue_id, "status": "created"}

    def add_item(self, queue_id: str, item_id: str, urgency_level: int, timestamp: str) -> dict:
        queue = self._queues.get(queue_id)
        if queue is None:
            return {"error": f"Queue '{queue_id}' not found"}
        
        dt = datetime.fromisoformat(timestamp)
        item = self._service.add_item_to_queue(queue, item_id, urgency_level, dt)
        return {
            "item_id": item.id,
            "urgency_level": item.urgency.level,
            "timestamp": item.timestamp.isoformat(),
            "status": "added"
        }

    def get_next(self, queue_id: str) -> dict:
        queue = self._queues.get(queue_id)
        if queue is None:
            return {"error": f"Queue '{queue_id}' not found"}
        
        try:
            item = self._service.get_next_item(queue)
            return {
                "item_id": item.id,
                "urgency_level": item.urgency.level,
                "timestamp": item.timestamp.isoformat()
            }
        except ValueError as e:
            return {"error": str(e)}

    def update_urgency(self, queue_id: str, item_id: str, new_urgency_level: int) -> dict:
        queue = self._queues.get(queue_id)
        if queue is None:
            return {"error": f"Queue '{queue_id}' not found"}
        
        try:
            self._service.update_item_urgency(queue, item_id, new_urgency_level)
            return {"item_id": item_id, "new_urgency_level": new_urgency_level, "status": "updated"}
        except ValueError as e:
            return {"error": str(e)}

    def remove_item(self, queue_id: str, item_id: str) -> dict:
        queue = self._queues.get(queue_id)
        if queue is None:
            return {"error": f"Queue '{queue_id}' not found"}
        
        try:
            item = self._service.remove_item(queue, item_id)
            return {"item_id": item.id, "status": "removed"}
        except ValueError as e:
            return {"error": str(e)}

    def list_queue(self, queue_id: str) -> dict:
        queue = self._queues.get(queue_id)
        if queue is None:
            return {"error": f"Queue '{queue_id}' not found"}
        
        items = [
            {
                "item_id": item.id,
                "urgency_level": item.urgency.level,
                "timestamp": item.timestamp.isoformat()
            }
            for item in queue.items
        ]
        return {"queue_id": queue_id, "items": items}
