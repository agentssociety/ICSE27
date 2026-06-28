"""Database models for Blood Bank Management Application.

This module defines the SQLAlchemy ORM models for blood units, transfusion
requests, reservations, and stock alerts. All models share a common
SQLAlchemy instance (db) which is initialized here.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

# Global database instance (initialized in main.py with app)
db = SQLAlchemy()


class BloodUnit(db.Model):
    """Represents a single unit of donated blood.

    Attributes:
        id: Unique identifier.
        abo_type: Blood group (A, B, AB, O).
        rh_factor: Rh factor ('positive' or 'negative').
        collection_date: Date when blood was collected.
        expiry_date: Calculated as collection_date + 42 days, unless provided.
        status: Current status: 'available', 'reserved', 'issued', 'expired'.
        reservation_id: Foreign key to Reservation if reserved.
        reservation: Relationship to Reservation (one-to-one).
    """

    __tablename__ = 'blood_units'

    id = Column(Integer, primary_key=True, autoincrement=True)
    abo_type = Column(String(2), nullable=False)
    rh_factor = Column(String(8), nullable=False)
    collection_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(
        String(10),
        nullable=False,
        default='available',
        index=True
    )
    reservation_id = Column(
        Integer,
        ForeignKey('reservations.id'),
        nullable=True,
        unique=True
    )

    # One-to-one with Reservation (blood unit belongs to reservation)
    reservation = relationship(
        'Reservation',
        backref='blood_unit',
        uselist=False,
        foreign_keys=[reservation_id],
        lazy='joined'
    )

    def __init__(
        self,
        abo_type: str,
        rh_factor: str,
        collection_date: datetime,
        expiry_date: Optional[datetime] = None
    ) -> None:
        """Initialize a new blood unit.

        Args:
            abo_type: Blood group (A, B, AB, O).
            rh_factor: Rh factor ('positive' or 'negative').
            collection_date: Date of collection.
            expiry_date: Optional explicit expiry date.
                        Defaults to collection_date + 42 days.
        """
        self.abo_type = abo_type
        self.rh_factor = rh_factor
        self.collection_date = collection_date
        self.expiry_date = expiry_date or (collection_date + timedelta(days=42))
        self.status = 'available'

    def expire(self) -> bool:
        """Mark this unit as expired.

        Does NOT commit; caller must handle commit.

        Returns:
            True if status changed to 'expired', False otherwise.
        """
        if self.status in ('available', 'reserved'):
            self.status = 'expired'
            if self.reservation:
                # Keep reservation record for auditing but mark as expired
                self.reservation.confirmed = False
                self.reservation_id = None
            return True
        return False

    def reserve(self, request_id: int) -> bool:
        """Reserve this unit for a transfusion request.

        Creates a Reservation entry and updates status. Does NOT commit;
        caller must manage transaction.

        Args:
            request_id: ID of the TransfusionRequest.

        Returns:
            True if reservation succeeded, False if unit not available.
        """
        if self.status != 'available':
            return False
        reservation = Reservation(request_id=request_id, unit_id=self.id)
        db.session.add(reservation)
        self.status = 'reserved'
        self.reservation_id = reservation.id
        db.session.flush()
        return True

    def issue(self) -> bool:
        """Issue this unit (mark as issued).

        Unit must be in 'reserved' status. The reservation is set as confirmed.
        Does NOT commit; caller must handle commit.

        Returns:
            True if issued successfully, False otherwise.
        """
        if self.status != 'reserved' or not self.reservation:
            return False
        self.status = 'issued'
        self.reservation.confirmed = True
        return True

    def release(self) -> bool:
        """Release this unit from reservation, making it available again.

        Does NOT commit; caller must handle commit.

        Returns:
            True if released, False if not reserved.
        """
        if self.status != 'reserved' or not self.reservation:
            return False
        # Keep reservation record for auditing but mark as released
        self.reservation.confirmed = False
        self.reservation.released_at = datetime.utcnow()
        self.reservation_id = None
        self.status = 'available'
        return True


class TransfusionRequest(db.Model):
    """Represents a request for blood transfusion.

    Attributes:
        id: Unique identifier.
        abo_type: Requested blood group.
        rh_factor: Requested Rh factor.
        quantity: Number of units requested.
        status: 'pending', 'fulfilled', 'cancelled'.
        created_at: Timestamp of creation.
        reservations: List of Reservation objects for matched units.
        matched_units: Derived list of BloodUnit through reservations.
    """

    __tablename__ = 'transfusion_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    abo_type = Column(String(2), nullable=False)
    rh_factor = Column(String(8), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(
        String(10),
        nullable=False,
        default='pending',
        index=True
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # One-to-many with Reservation
    reservations = relationship(
        'Reservation',
        backref='request',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @property
    def matched_units(self) -> List['BloodUnit']:
        """List of BloodUnit objects matched to this request via reservations."""
        return [res.blood_unit for res in self.reservations if res.blood_unit]

    def __init__(
        self,
        abo_type: str,
        rh_factor: str,
        quantity: int
    ) -> None:
        """Initialize a new transfusion request.

        Args:
            abo_type: Blood group.
            rh_factor: Rh factor.
            quantity: Number of units needed.
        """
        self.abo_type = abo_type
        self.rh_factor = rh_factor
        self.quantity = quantity
        self.status = 'pending'
        self.created_at = datetime.utcnow()

    def fulfill(self) -> bool:
        """Mark this request as fulfilled.

        Does NOT commit; caller must handle commit.

        Returns:
            True if changed to fulfilled, False otherwise.
        """
        if self.status != 'pending':
            return False
        self.status = 'fulfilled'
        return True

    def cancel(self) -> bool:
        """Cancel this request and release all reserved units.

        Does NOT commit; caller must handle commit.

        Returns:
            True if cancelled, False if already fulfilled or cancelled.
        """
        if self.status != 'pending':
            return False
        self.status = 'cancelled'
        # Release all reservations for this request
        for res in list(self.reservations):
            if res.blood_unit:
                res.blood_unit.status = 'available'
                res.blood_unit.reservation_id = None
                res.released_at = datetime.utcnow()
                res.confirmed = False
        return True


class Reservation(db.Model):
    """Links a BloodUnit to a TransfusionRequest with temporal state.

    Attributes:
        id: Unique identifier.
        request_id: Foreign key to TransfusionRequest.
        unit_id: Foreign key to BloodUnit.
        reserved_at: Timestamp when reservation was made.
        released_at: Timestamp when reservation was released (if applicable).
        confirmed: Whether the unit has been issued (confirmed usage).
    """

    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(
        Integer,
        ForeignKey('transfusion_requests.id'),
        nullable=False
    )
    unit_id = Column(
        Integer,
        ForeignKey('blood_units.id'),
        nullable=False
    )
    reserved_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    released_at = Column(DateTime, nullable=True)
    confirmed = Column(Boolean, nullable=False, default=False)

    def __init__(
        self,
        request_id: int,
        unit_id: int
    ) -> None:
        self.request_id = request_id
        self.unit_id = unit_id
        self.reserved_at = datetime.utcnow()
        self.released_at = None
        self.confirmed = False

    def release_after(self) -> datetime:
        """Return the datetime after which this reservation should be released.

        Uses the application-wide configurable timeout from config.py.

        Returns:
            Datetime = reserved_at + configurable timeout.
        """
        # Import here to avoid circular import at module level
        from config import Config
        return self.reserved_at + timedelta(minutes=Config.RESERVATION_RELEASE_MINUTES)

    def confirm(self) -> None:
        """Mark reservation as confirmed (blood unit issued).

        Does NOT commit; caller must handle commit.
        """
        self.confirmed = True

    def expire(self) -> bool:
        """Handle expiration of this reservation (release unit, mark inactive).

        This is called by the scheduler for unconfirmed reservations.
        It releases the associated blood unit and marks the reservation as expired.
        Does NOT commit; caller is responsible.

        Returns:
            True if expired successfully, False if already confirmed.
        """
        if self.confirmed:
            return False
        if self.blood_unit:
            self.blood_unit.status = 'available'
            self.blood_unit.reservation_id = None
        self.released_at = datetime.utcnow()
        self.confirmed = False
        return True


class StockAlert(db.Model):
    """Raised when stock of a specific blood type falls below threshold.

    Attributes:
        id: Unique identifier.
        abo_type: Blood group.
        rh_factor: Rh factor.
        current_stock: Stock level at time of alert creation.
        created_at: Timestamp.
        active: Whether the alert is still unresolved.
    """

    __tablename__ = 'stock_alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    abo_type = Column(String(2), nullable=False)
    rh_factor = Column(String(8), nullable=False)
    current_stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    active = Column(Boolean, nullable=False, default=True)

    def __init__(
        self,
        abo_type: str,
        rh_factor: str,
        current_stock: int
    ) -> None:
        self.abo_type = abo_type
        self.rh_factor = rh_factor
        self.current_stock = current_stock
        self.created_at = datetime.utcnow()
        self.active = True

    def resolve(self) -> None:
        """Mark this alert as resolved (stock restored).

        Does NOT commit; caller must handle commit.
        """
        self.active = False
