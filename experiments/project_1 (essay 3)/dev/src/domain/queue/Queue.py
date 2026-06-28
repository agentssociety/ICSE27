from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime

if TYPE_CHECKING:
    from src.domain.patient import Patient
    from src.domain.urgency_level import UrgencyLevel

"""
Domain layer for the Queue domain class

Package: domain.queue
Layer: domain
Related tasks: #55, #56, #57, #58
Requirement coverage:
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
- Real-time live dashboard displaying urgency and wait time
"""

@dataclass
class Queue:
    items: list[QueueItem]
    patient: Optional[Patient] = None
    urgencyLevel: Optional[UrgencyLevel] = None

    def sortItems(self, items: list[QueueItem]) -> list[QueueItem]:
        # Sort by urgency (highest first = descending), then by time (oldest first = ascending)
        return sorted(
            items,
            key=lambda item: (-item.urgency.level, item.timestamp)
        )

    def findItemById(self, itemId: str) -> QueueItem:
        for item in self.items:
            if item.id == itemId:
                return item
        raise ValueError(f"QueueItem with id '{itemId}' not found")

    def addItem(self, item: QueueItem) -> None:
        self.items.append(item)
        self.items = self.sortItems(self.items)

    def removeItem(self, itemId: str) -> QueueItem:
        item = self.findItemById(itemId)
        self.items.remove(item)
        return item

    def getNextPatient(self) -> QueueItem:
        if not self.items:
            raise ValueError("Queue is empty")
        self.items = self.sortItems(self.items)
        return self.items[0]

    def reorderOnUrgencyChange(self, itemId: str, newUrgency: UrgencyLevel) -> None:
        item = self.findItemById(itemId)
        item.updateUrgency(newUrgency)
        self.items = self.sortItems(self.items)

@dataclass
class QueueItem:
    id: str
    urgency: UrgencyLevel
    timestamp: datetime
    queue: Queue

    def compareUrgency(self, item1: QueueItem, item2: QueueItem) -> int:
        if item1.urgency.level > item2.urgency.level:
            return -1
        elif item1.urgency.level < item2.urgency.level:
            return 1
        return 0

    def compareTimestamp(self, item1: QueueItem, item2: QueueItem) -> int:
        if item1.timestamp < item2.timestamp:
            return -1
        elif item1.timestamp > item2.timestamp:
            return 1
        return 0

    def compareId(self, item1: QueueItem, item2: QueueItem) -> int:
        if item1.id < item2.id:
            return -1
        elif item1.id > item2.id:
            return 1
        return 0

    def updateUrgency(self, newUrgency: UrgencyLevel) -> None:
        self.urgency = newUrgency

@dataclass
class QueueId:
    pass

@dataclass
class QueueCreatedEvent:
    pass

@dataclass
class QueueUpdatedEvent:
    pass
