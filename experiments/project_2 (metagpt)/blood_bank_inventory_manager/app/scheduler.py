"""Background scheduling jobs for Blood Bank Management Application.

This module provides the Scheduler class that defines three periodic jobs:
- Expire blood units whose expiry date has passed.
- Release unconfirmed reservations after a configurable timeout.
- Check stock levels and raise alerts when below threshold.

All jobs run within Flask application context and commit transactions.
"""

from datetime import datetime, timedelta
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app, Flask

from app.models import BloodUnit, Reservation, StockAlert, TransfusionRequest, db
from config import Config


class Scheduler:
    """Manages background tasks for the blood bank system.

    Encapsulates an APScheduler instance and provides methods that
    can be registered as jobs. The scheduler is started in the main
    application factory.
    """

    # Job intervals (in minutes, except where hours are used)
    _EXPIRATION_INTERVAL_HOURS = Config.EXPIRATION_CHECK_INTERVAL_HOURS
    _RELEASE_CHECK_INTERVAL_MINUTES = 10   # Check every 10 minutes for expired reservations
    _ALERT_INTERVAL_MINUTES = Config.ALERT_CHECK_INTERVAL_MINUTES

    def __init__(self, app: Flask) -> None:
        """Initialize the scheduler with a Flask application.

        Creates an APScheduler BackgroundScheduler and adds the three
        periodic jobs using the intervals defined in Config (or constants).
        Note: The release-unconfirmed-reservations job runs frequently (10min)
        to check for reservations that have passed the 24-hour timeout.

        Args:
            app: Flask application instance (used for app context).
        """
        self.app = app
        self.scheduler = BackgroundScheduler()

        # Register jobs with intervals from config
        self.scheduler.add_job(
            func=self.expire_units_job,
            trigger='interval',
            hours=self._EXPIRATION_INTERVAL_HOURS,
            id='expire_units_job',
            name='Expire outdated blood units',
            replace_existing=True,
        )

        # Run every 10 minutes to release reservations that have exceeded
        # the 24-hour confirmation window (RESERVATION_RELEASE_MINUTES).
        self.scheduler.add_job(
            func=self.release_unconfirmed_reservations,
            trigger='interval',
            minutes=self._RELEASE_CHECK_INTERVAL_MINUTES,
            id='release_unconfirmed_reservations',
            name='Release unconfirmed reservations',
            replace_existing=True,
        )

        self.scheduler.add_job(
            func=self.check_and_raise_alerts,
            trigger='interval',
            minutes=self._ALERT_INTERVAL_MINUTES,
            id='check_and_raise_alerts',
            name='Check stock levels and raise alerts',
            replace_existing=True,
        )

        # Start the scheduler (will be called after app is ready)
        self.scheduler.start()

    def _with_app_context(self, func: Callable[[], None]) -> None:
        """Execute a function within a Flask application context.

        This helper ensures that database operations are executed inside
        an application context, even when called by APScheduler background
        threads. It commits the transaction on success, rolls back on
        exception, and re-raises the exception for logging by APScheduler.

        Args:
            func: Callable to run inside the app context.
        """
        with self.app.app_context():
            try:
                func()
                db.session.commit()
            except Exception as e:
                current_app.logger.error(
                    f"Scheduler job failed: {e}", exc_info=True
                )
                db.session.rollback()
                raise

    def expire_units_job(self) -> None:
        """Mark all blood units as expired if their expiry date has passed.

        Only affects units with status 'available' or 'reserved'. For reserved
        units, the associated reservation is also released.
        """
        self._with_app_context(self._expire_units_impl)

    def _expire_units_impl(self) -> None:
        """Implementation of expire_units_job (inside app context)."""
        now = datetime.utcnow()
        units_to_expire = BloodUnit.query.filter(
            BloodUnit.expiry_date < now,
            BloodUnit.status.in_(['available', 'reserved'])
        ).all()

        for unit in units_to_expire:
            unit.expire()  # Sets status to 'expired', releases reservation if any

        if units_to_expire:
            current_app.logger.info(
                f"Expired {len(units_to_expire)} blood units."
            )

    def release_unconfirmed_reservations(self) -> None:
        """Release reservations that have not been confirmed within the timeout.

        The timeout (default 24 hours) is defined in Config.RESERVATION_RELEASE_MINUTES.
        Only reservations with confirmed=False and reserved_at older than the timeout
        are released. After release, the associated request's status is reverted to
        'pending' if all its reservations have been released.
        """
        self._with_app_context(self._release_unconfirmed_impl)

    def _release_unconfirmed_impl(self) -> None:
        """Implementation of release_unconfirmed_reservations (inside app context)."""
        threshold = datetime.utcnow() - timedelta(
            minutes=Config.RESERVATION_RELEASE_MINUTES
        )
        old_reservations = Reservation.query.filter(
            Reservation.confirmed == False,          # noqa: E712
            Reservation.reserved_at < threshold
        ).all()

        released_count = 0
        affected_request_ids = set()
        for reservation in old_reservations:
            if reservation.expire():  # Releases the blood unit
                released_count += 1
                affected_request_ids.add(reservation.request_id)

        # Optionally update associated request statuses
        for request_id in affected_request_ids:
            request = TransfusionRequest.query.get(request_id)
            if request and request.status == 'fulfilled':
                # If all reservations for this request have been released
                remaining_reservations = Reservation.query.filter(
                    Reservation.request_id == request_id,
                    Reservation.confirmed == False,
                    Reservation.released_at.is_(None)  # still active
                ).count()
                if remaining_reservations == 0:
                    request.status = 'pending'
                    current_app.logger.info(
                        f"Request {request_id} reverted to pending "
                        "after all reservations released."
                    )

        if released_count:
            current_app.logger.info(
                f"Released {released_count} unconfirmed reservations."
            )

    def check_and_raise_alerts(self) -> None:
        """Check stock levels and create alerts for types below threshold.

        Alerts are created only if no active alert already exists for the
        same blood type and Rh factor. Existing active alerts remain
        (they will be resolved manually via the UI or future automation).
        """
        self._with_app_context(self._check_alerts_impl)

    def _check_alerts_impl(self) -> None:
        """Implementation of check_and_raise_alerts (inside app context)."""
        threshold = Config.STOCK_ALERT_THRESHOLD
        # Query stock count per type and Rh factor for available units
        stock_counts = db.session.query(
            BloodUnit.abo_type,
            BloodUnit.rh_factor,
            db.func.count(BloodUnit.id).label('count')
        ).filter(
            BloodUnit.status == 'available',
            BloodUnit.expiry_date > datetime.utcnow()  # not expired
        ).group_by(
            BloodUnit.abo_type,
            BloodUnit.rh_factor
        ).all()

        # Build a dict for easy lookup
        stock_map = {(row.abo_type, row.rh_factor): row.count for row in stock_counts}

        # Check each possible combination (A,B,AB,O × positive,negative)
        for abo in ['A', 'B', 'AB', 'O']:
            for rh in ['positive', 'negative']:
                current_stock = stock_map.get((abo, rh), 0)
                if current_stock < threshold:
                    # Check if there is already an active alert for this type
                    existing_alert = StockAlert.query.filter(
                        StockAlert.abo_type == abo,
                        StockAlert.rh_factor == rh,
                        StockAlert.active == True  # noqa: E712
                    ).first()
                    if not existing_alert:
                        alert = StockAlert(
                            abo_type=abo,
                            rh_factor=rh,
                            current_stock=current_stock
                        )
                        db.session.add(alert)
                        current_app.logger.warning(
                            f"Stock alert created for {abo} {rh}: "
                            f"{current_stock} units (threshold {threshold})."
                        )

    def shutdown(self) -> None:
        """Gracefully shut down the scheduler.

        Should be called when the application is stopping to release
        background threads.
        """
        self.scheduler.shutdown(wait=False)
