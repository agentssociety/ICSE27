from __future__ import annotations

from typing import Any

"""
Api layer for the Alert domain class

Package: api.alert
Layer: api
Related tasks: #30
Requirement coverage:
- Blood Stock Alert System
"""

class InventoryApiAdapter:
    def __init__(self, apiEndpoint: str | None = None) -> None:
        self.apiEndpoint = apiEndpoint

class NotificationGatewayAdapter:
    def __init__(self) -> None:
        pass
