"""Matching service for blood bank management.

This module implements the core matching logic to find compatible blood units
for transfusion requests and manage reservations.
"""

from datetime import datetime
from typing import List

from app.models import BloodUnit, TransfusionRequest, Reservation, db


class MatchingService:
    """Service for matching blood units to transfusion requests.

    Provides methods to find compatible units, reserve them, and perform
    automated matching and reservation in a single transaction.
    """

    @staticmethod
    def find_compatible_units(
        abo_type: str,
        rh_factor: str,
        quantity: int,
    ) -> List[BloodUnit]:
        """Find compatible available blood units for a given blood type and Rh factor.

        Compatibility follows standard transfusion guidelines:
        - ABO: O is universal donor, AB is universal recipient.
        - Rh: Rh-negative can only receive Rh-negative; Rh-positive can receive both.

        Results are ordered by:
            1. Exact match (same ABO and Rh)
            2. Same ABO but compatible Rh (for Rh-positive recipients)
            3. Compatible ABO (O for A/B/AB, A for AB, B for AB) and compatible Rh
            4. Within each tier, units expiring soonest first (FIFO).

        Args:
            abo_type: Requested ABO type ('A', 'B', 'AB', 'O').
            rh_factor: Requested Rh factor ('positive' or 'negative').
            quantity: Number of units needed.

        Returns:
            List of available BloodUnit objects (up to quantity) ordered by
            compatibility and expiry.

        Raises:
            ValueError: If abo_type or rh_factor are invalid.
        """
        # Validate inputs
        valid_abo = {'A', 'B', 'AB', 'O'}
        valid_rh = {'positive', 'negative'}
        if abo_type not in valid_abo:
            raise ValueError(f"Invalid ABO type: {abo_type}")
        if rh_factor not in valid_rh:
            raise ValueError(f"Invalid Rh factor: {rh_factor}")

        # Determine compatible ABO types for the given type
        abo_compatibility = {
            'O': {'O'},
            'A': {'A', 'O'},
            'B': {'B', 'O'},
            'AB': {'A', 'B', 'AB', 'O'},
        }
        compatible_abo = abo_compatibility[abo_type]

        # Determine compatible Rh factors
        if rh_factor == 'negative':
            compatible_rh = {'negative'}
        else:
            compatible_rh = {'positive', 'negative'}

        # Query available units with compatible types
        units = BloodUnit.query.filter(
            BloodUnit.status == 'available',
            BloodUnit.abo_type.in_(compatible_abo),
            BloodUnit.rh_factor.in_(compatible_rh),
            BloodUnit.expiry_date > datetime.utcnow(),  # not already expired
        ).all()

        # Define sorting key: priority (lower = higher) then expiry date
        def sort_key(unit: BloodUnit) -> tuple:
            same_abo = (unit.abo_type == abo_type)
            same_rh = (unit.rh_factor == rh_factor)
            if same_abo and same_rh:
                priority = 0
            elif same_abo:
                priority = 1
            elif same_rh:
                priority = 2
            else:
                priority = 3
            return (priority, unit.expiry_date)

        units.sort(key=sort_key)
        return units[:quantity]

    @staticmethod
    def reserve_units(
        request: TransfusionRequest,
        units: List[BloodUnit],
    ) -> bool:
        """Reserve a list of blood units for a transfusion request.

        Creates Reservation records and updates BloodUnit status to 'reserved'.
        This method does NOT commit; it relies on the caller to manage the
        database transaction.

        Args:
            request: The TransfusionRequest object (must already be in DB).
            units: List of BloodUnit objects to reserve.

        Returns:
            True if all units were successfully reserved, False if any unit
            is not available or already reserved.
        """
        if request.status != 'pending':
            return False

        # Pre-check all units are available
        for unit in units:
            if unit.status != 'available':
                return False

        # Create reservations and update units
        for unit in units:
            reservation = Reservation(
                request_id=request.id,
                unit_id=unit.id
            )
            db.session.add(reservation)
            unit.status = 'reserved'
            unit.reservation_id = reservation.id

        db.session.flush()
        return True

    @staticmethod
    def auto_match_and_reserve(
        request: TransfusionRequest,
    ) -> bool:
        """Perform automatic matching and reservation for a transfusion request.

        Uses find_compatible_units to locate available units, then reserve_units
        to lock them. Runs inside a database transaction.

        Args:
            request: TransfusionRequest object (should be in pending state).

        Returns:
            True if request was fully satisfied (all units reserved),
            False if insufficient units or transaction failed.
        """
        # Ensure request is in DB (has an ID)
        if not request.id:
            db.session.add(request)
            db.session.flush()

        if request.status != 'pending':
            return False

        # Find compatible units
        units = MatchingService.find_compatible_units(
            request.abo_type,
            request.rh_factor,
            request.quantity
        )

        if len(units) < request.quantity:
            return False

        # Reserve units
        if not MatchingService.reserve_units(request, units):
            return False

        # Mark request as fulfilled since all units are reserved
        request.fulfill()

        return True
