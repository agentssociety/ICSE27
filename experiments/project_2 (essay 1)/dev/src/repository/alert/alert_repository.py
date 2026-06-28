from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the Alert domain class

Package: repository.alert
Layer: repository
Related tasks: #30
Requirement coverage:
- Blood Stock Alert System
"""

class Channel(Protocol):
    ...

class InventoryPort(Protocol):
    ...

class NotificationPort(Protocol):
    def sendAlert(self, channels: [Email, SMS: Any, message: Any) -> None:
        ...
