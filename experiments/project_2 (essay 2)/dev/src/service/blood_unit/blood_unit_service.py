from __future__ import annotations

from datetime import date, timedelta, datetime
from typing import Any, Optional

from src.domain.blood_unit.BloodUnit import ABOType, RhFactor, BloodUnitStatus
from src.dto.blood_unit.blood_unit_dto import BloodUnitCreate, BloodUnitUpdate, BloodUnitResponse
from src.infra.blood_unit.blood_unit_repo_impl import SQLAlchemyBloodUnitRepository
from src.infra.transfusion_request.transfusion_request_repo_impl import SQLAlchemyTransfusionRequestRepository


class BloodUnitService:
    """Service for tracking blood units by ABO type, Rh factor, collection date, and expiry."""

    def __init__(self, repo: SQLAlchemyBloodUnitRepository,
                 transfusion_repo: Optional[SQLAlchemyTransfusionRequestRepository] = None) -> None:
        self._repo = repo
        self._transfusion_repo = transfusion_repo

    def calculate_expiry_date(self, collection_date: date) -> date:
        """Calculate expiry date as 42 days from collection."""
        return collection_date + timedelta(days=42)

    def create_blood_unit(self, data: BloodUnitCreate) -> BloodUnitResponse:
        """Create a new blood unit with auto-calculated expiry and default status."""
        expiry_date = self.calculate_expiry_date(data.collectionDate)
        return self._repo.create(data, expiryDate=expiry_date, status="available")

    def get_inventory_summary(self) -> dict[str, int]:
        """Get current inventory levels per ABO/Rh type (only available units)."""
        all_units = self._repo.get_all()
        summary: dict[str, int] = {}
        for unit in all_units:
            if unit.status == "available":
                key = f"{unit.aboType}/{unit.rhFactor}"
                summary[key] = summary.get(key, 0) + 1
        return summary

    def check_low_stock_alerts(self, threshold: int = 5) -> list[str]:
        """Check inventory and return alert messages for blood types below threshold."""
        summary = self.get_inventory_summary()
        alerts = []
        for blood_type, count in summary.items():
            if count < threshold:
                alerts.append(
                    f"Low stock alert: {blood_type} has only {count} unit(s). "
                    f"Threshold is {threshold}. Please initiate restocking."
                )
        # Also alert types with zero stock
        all_abo_rh = ["A/positive", "A/negative", "B/positive", "B/negative",
                       "AB/positive", "AB/negative", "O/positive", "O/negative"]
        for combo in all_abo_rh:
            if combo not in summary:
                alerts.append(
                    f"Low stock alert: {combo} has 0 units. "
                    f"Threshold is {threshold}. Please initiate restocking."
                )
        return alerts

    def change_status(self, unit_id: int, new_status: str) -> Optional[BloodUnitResponse]:
        """Change the status of a blood unit."""
        update_data = BloodUnitUpdate(status=new_status)
        return self._repo.update(unit_id, update_data)

    def get_near_expiry_units(self, days_threshold: int = 7) -> list[BloodUnitResponse]:
        """Return blood units nearing expiry within the given threshold (default 7 days)."""
        today = date.today()
        threshold_date = today + timedelta(days=days_threshold)
        all_units = self._repo.get_all()
        near_expiry = []
        for unit in all_units:
            if unit.status == "available" and unit.expiryDate <= threshold_date and unit.expiryDate >= today:
                near_expiry.append(unit)
        return near_expiry

    def get_open_transfusion_requests(self) -> list[dict[str, Any]]:
        """Return pending transfusion requests as dicts."""
        if self._transfusion_repo is None:
            return []
        stored = self._transfusion_repo.get_all()
        return [
            {
                "id": "",
                "bloodType": r.bloodType,
                "rhFactor": r.rhFactor,
                "quantity": r.quantity,
            }
            for r in stored
        ]

    def get_dashboard_data(self) -> dict[str, Any]:
        """Return full dashboard data: stock levels, near-expiry units, and open requests."""
        return {
            "stock_levels": self.get_inventory_summary(),
            "near_expiry_units": [
                {
                    "id": u.id,
                    "uniqueID": u.uniqueID,
                    "aboType": u.aboType,
                    "rhFactor": u.rhFactor,
                    "collectionDate": u.collectionDate.isoformat(),
                    "expiryDate": u.expiryDate.isoformat(),
                    "status": u.status,
                }
                for u in self.get_near_expiry_units()
            ],
            "open_transfusion_requests": self.get_open_transfusion_requests(),
            "low_stock_alerts": self.check_low_stock_alerts(),
        }

    @staticmethod
    def get_compatible_blood_types(abo_type: str, rh_factor: str) -> list[tuple[str, str]]:
        """Return list of compatible (abo_type, rh_factor) tuples.

        Exact match is always first. Compatible types for transfusion:
        - O- is universal donor
        - O+ can give to O+, A+, B+, AB+
        - A- can give to A-, A+, AB-, AB+
        - A+ can give to A+, AB+
        - B- can give to B-, B+, AB-, AB+
        - B+ can give to B+, AB+
        - AB- can give to AB-, AB+
        - AB+ can give to AB+ only
        """
        # First priority: exact match
        exact = (abo_type.lower(), rh_factor.lower())
        compat = [exact]

        # Expand based on donor type rules
        abo = abo_type.upper()
        rh = rh_factor.lower()

        if abo == "O" and rh == "negative":
            # O- is universal donor: can give to anyone, but exact match is priority
            pass  # Already have exact; other types would be less priority
        elif abo == "O" and rh == "positive":
            compat.append(("O", "negative"))  # O+ donors can also give to O- (same ABO)
        elif abo == "A" and rh == "negative":
            compat.append(("A", "positive"))
        elif abo == "A" and rh == "positive":
            compat.append(("A", "negative"))
        elif abo == "B" and rh == "negative":
            compat.append(("B", "positive"))
        elif abo == "B" and rh == "positive":
            compat.append(("B", "negative"))
        elif abo == "AB" and rh == "negative":
            compat.append(("AB", "positive"))
        elif abo == "AB" and rh == "positive":
            compat.append(("AB", "negative"))

        return compat

    def find_matching_units(self, request_blood_type: str, request_rh_factor: str) -> list[dict[str, Any]]:
        """Find matching blood units for a transfusion request.

        Priority:
        1. Exact ABO/Rh match, sorted by closest expiry date.
        2. Compatible types, sorted by closest expiry date.
        3. Excludes units that have not passed cross-match (status != 'available').

        Returns list of unit dicts sorted by priority.
        """
        all_units = self._repo.get_all()
        # Filter to only available units
        available = [u for u in all_units if u.status == "available"]

        # Get compatible types in priority order
        compat_types = self.get_compatible_blood_types(request_blood_type, request_rh_factor)
        # Remove duplicates while preserving order
        seen = set()
        unique_types = []
        for t in compat_types:
            if t not in seen:
                seen.add(t)
                unique_types.append(t)

        # Group units by type priority
        exact_units = []
        other_compat = []

        for unit in available:
            unit_type = (unit.aboType.lower(), unit.rhFactor.lower())
            if unit_type == unique_types[0]:
                exact_units.append(unit)
            elif unit_type in unique_types[1:]:
                other_compat.append(unit)

        # Sort each group by expiry date (closest first)
        exact_units.sort(key=lambda u: u.expiryDate)
        other_compat.sort(key=lambda u: u.expiryDate)

        # Build result
        result = []
        for unit in exact_units + other_compat:
            result.append({
                "id": unit.id,
                "uniqueID": unit.uniqueID,
                "aboType": unit.aboType,
                "rhFactor": unit.rhFactor,
                "collectionDate": unit.collectionDate.isoformat(),
                "expiryDate": unit.expiryDate.isoformat(),
                "status": unit.status,
                "match_type": "exact" if unit in exact_units else "compatible",
            })
        return result

    def check_and_expire_units(self) -> int:
        """Mark all units past expiry date as expired. Returns number of expired units."""
        today = date.today()
        all_units = self._repo.get_all()
        expired_count = 0
        for unit in all_units:
            if unit.status != "expired" and unit.expiryDate < today:
                self._repo.update(unit.id, BloodUnitUpdate(status="expired"))
                expired_count += 1
        return expired_count
