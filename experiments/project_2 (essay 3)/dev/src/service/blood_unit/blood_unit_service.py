from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Optional, Protocol

from src.domain.blood_unit.BloodUnit import BloodUnit
from src.dto.blood_unit.blood_unit_dto import BloodUnitCreate, BloodUnitUpdate, BloodUnitResponse
from src.repository.blood_unit.blood_unit_repository import BloodUnitRepository

# Default shelf life for red blood cells: 42 days
DEFAULT_SHELF_LIFE_DAYS = 42
# Minimum units per blood type before alert
MIN_INVENTORY_THRESHOLD = 5
# Days before expiration to consider a unit "nearing expiration"
NEARING_EXPIRATION_DAYS = 5

# ABO/Rh compatibility rules
# Maps recipient blood type to list of compatible donor blood types
ABO_RH_COMPATIBILITY: dict[str, list[str]] = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
}


class InventoryAlert:
    """Represents an alert for low inventory of a specific blood type."""
    def __init__(self, blood_type: str, current_count: int, threshold: int = MIN_INVENTORY_THRESHOLD) -> None:
        self.blood_type = blood_type
        self.current_count = current_count
        self.threshold = threshold

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InventoryAlert):
            return NotImplemented
        return (self.blood_type == other.blood_type and
                self.current_count == other.current_count and
                self.threshold == other.threshold)

    def __repr__(self) -> str:
        return f"InventoryAlert(blood_type='{self.blood_type}', current_count={self.current_count}, threshold={self.threshold})"


class NearingExpirationUnit:
    """Represents a blood unit nearing its expiration date."""
    def __init__(self, unit_id: int, blood_type: str, expiration_date: date, days_until_expiry: int) -> None:
        self.unit_id = unit_id
        self.blood_type = blood_type
        self.expiration_date = expiration_date
        self.days_until_expiry = days_until_expiry


class DashboardData:
    """Aggregated data for the inventory dashboard."""
    def __init__(
        self,
        stock_levels: dict[str, int],
        nearing_expiration: list[NearingExpirationUnit],
        open_requests: list[dict],
    ) -> None:
        self.stock_levels = stock_levels
        self.nearing_expiration = nearing_expiration
        self.open_requests = open_requests


class BloodUnitService(Protocol):
    """Protocol for BloodUnit service operations."""

    def create_blood_unit(self, data: BloodUnitCreate) -> BloodUnitResponse:
        """Create a new blood unit."""
        ...

    def get_blood_unit(self, unit_id: int) -> Optional[BloodUnitResponse]:
        """Get a blood unit by ID."""
        ...

    def list_blood_units(self, skip: int = 0, limit: int = 100) -> list[BloodUnitResponse]:
        """List all blood units."""
        ...

    def update_blood_unit(self, unit_id: int, data: BloodUnitUpdate) -> Optional[BloodUnitResponse]:
        """Update a blood unit."""
        ...

    def delete_blood_unit(self, unit_id: int) -> bool:
        """Delete a blood unit."""
        ...

    def check_expired_units(self) -> int:
        """Check all blood units and mark expired ones. Returns count of expired units."""
        ...

    def check_inventory_levels(self) -> list[InventoryAlert]:
        """Check inventory levels and return alerts for blood types below threshold."""
        ...

    def find_compatible_units(self, patient_abo_rh: str) -> list[BloodUnitResponse]:
        """Find all non-expired blood units compatible with the given patient ABO/Rh type."""
        ...

    def get_dashboard_data(self) -> DashboardData:
        """Get aggregated dashboard data."""
        ...


class BloodUnitServiceImpl:
    """Service implementation for blood unit operations."""

    def __init__(self, repository: BloodUnitRepository) -> None:
        self._repository = repository

    def create_blood_unit(self, data: BloodUnitCreate) -> BloodUnitResponse:
        domain = BloodUnit(
            abo_rh_type=data.abo_rh_type,
            collection_date=data.collection_date,
        )
        return self._repository.create(data)

    def get_blood_unit(self, unit_id: int) -> Optional[BloodUnitResponse]:
        return self._repository.get_by_id(unit_id)

    def list_blood_units(self, skip: int = 0, limit: int = 100) -> list[BloodUnitResponse]:
        return self._repository.get_all(skip=skip, limit=limit)

    def update_blood_unit(self, unit_id: int, data: BloodUnitUpdate) -> Optional[BloodUnitResponse]:
        return self._repository.update(unit_id, data)

    def delete_blood_unit(self, unit_id: int) -> bool:
        return self._repository.delete(unit_id)

    def check_expired_units(self) -> int:
        """Check all blood units and mark expired ones based on shelf life."""
        units = self._repository.get_all(skip=0, limit=10000)
        today = date.today()
        expired_count = 0
        for unit in units:
            if not unit.is_expired:
                shelf_life_end = unit.collection_date + timedelta(days=DEFAULT_SHELF_LIFE_DAYS)
                if today > shelf_life_end:
                    update_data = BloodUnitUpdate(is_expired=True)
                    self._repository.update(unit.id, update_data)
                    expired_count += 1
        return expired_count

    def check_inventory_levels(self) -> list[InventoryAlert]:
        """Check inventory levels and return alerts for blood types below threshold."""
        units = self._repository.get_all(skip=0, limit=10000)
        type_counts: Counter = Counter()
        for unit in units:
            if not unit.is_expired:
                type_counts[unit.abo_rh_type] += 1

        alerts: list[InventoryAlert] = []
        for blood_type, count in type_counts.items():
            if count < MIN_INVENTORY_THRESHOLD:
                alerts.append(InventoryAlert(blood_type=blood_type, current_count=count))
        return alerts

    def find_compatible_units(self, patient_abo_rh: str) -> list[BloodUnitResponse]:
        """Find all non-expired blood units compatible with the given patient ABO/Rh type."""
        if patient_abo_rh not in ABO_RH_COMPATIBILITY:
            raise ValueError(f"Unknown ABO/Rh type: {patient_abo_rh}")

        compatible_types = ABO_RH_COMPATIBILITY[patient_abo_rh]
        all_units = self._repository.get_all(skip=0, limit=10000)
        return [
            unit for unit in all_units
            if not unit.is_expired and unit.abo_rh_type in compatible_types
        ]

    def get_dashboard_data(self) -> DashboardData:
        """Get aggregated dashboard data."""
        units = self._repository.get_all(skip=0, limit=10000)
        today = date.today()

        # Stock levels: count non-expired units by type
        stock_levels: dict[str, int] = {}
        # Units nearing expiration
        nearing_expiration: list[NearingExpirationUnit] = []

        for unit in units:
            if not unit.is_expired:
                stock_levels[unit.abo_rh_type] = stock_levels.get(unit.abo_rh_type, 0) + 1

                shelf_life_end = unit.collection_date + timedelta(days=DEFAULT_SHELF_LIFE_DAYS)
                days_until_expiry = (shelf_life_end - today).days
                if 0 <= days_until_expiry <= NEARING_EXPIRATION_DAYS:
                    nearing_expiration.append(NearingExpirationUnit(
                        unit_id=unit.id,
                        blood_type=unit.abo_rh_type,
                        expiration_date=shelf_life_end,
                        days_until_expiry=days_until_expiry,
                    ))

        # Open requests (simulated - in real app would come from TransfusionRequestRepository)
        open_requests: list[dict] = []

        return DashboardData(
            stock_levels=stock_levels,
            nearing_expiration=nearing_expiration,
            open_requests=open_requests,
        )

