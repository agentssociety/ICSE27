"""Flask routes for the Blood Bank Management Application.

This module defines all RESTful endpoints and page routes for inventory
management, transfusion requests, dashboard, and stock alerts. It uses
Flask blueprints to organize routes logically.
"""

from datetime import datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import func

from app.forms import (
    AddBloodUnitForm,
    InventoryFilterForm,
    RequestFilterForm,
    TransfusionRequestForm,
)
from app.matching_service import MatchingService
from app.models import (
    BloodUnit,
    Reservation,
    StockAlert,
    TransfusionRequest,
    db,
)

# -----------------------------------------------------------------------------
# Blueprint registration
# -----------------------------------------------------------------------------
main_bp = Blueprint('main', __name__, template_folder='../templates')


# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------
@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    """Display the main dashboard with stock summary, expiring units,
    open requests, and active alerts.

    Returns:
        Rendered HTML template.
    """
    # Aggregate stock by blood type and Rh factor for available units
    stock_counts = (
        db.session.query(
            BloodUnit.abo_type,
            BloodUnit.rh_factor,
            func.count(BloodUnit.id).label('count'),
        )
        .filter(BloodUnit.status == 'available',
                BloodUnit.expiry_date > datetime.utcnow())
        .group_by(BloodUnit.abo_type, BloodUnit.rh_factor)
        .all()
    )
    stock_summary = [
        {
            'abo_type': row.abo_type,
            'rh_factor': row.rh_factor,
            'count': row.count,
        }
        for row in stock_counts
    ]

    # Units expiring within the next 7 days (available or reserved)
    seven_days = datetime.utcnow().date().isoformat()
    from datetime import timedelta
    expiring_soon = (
        BloodUnit.query
        .filter(BloodUnit.expiry_date <= datetime.utcnow() + timedelta(days=7),
                BloodUnit.expiry_date > datetime.utcnow(),
                BloodUnit.status.in_(['available', 'reserved']))
        .order_by(BloodUnit.expiry_date.asc())
        .all()
    )

    # Open (pending) transfusion requests
    open_requests = (
        TransfusionRequest.query
        .filter(TransfusionRequest.status == 'pending')
        .order_by(TransfusionRequest.created_at.desc())
        .all()
    )

    # Active alerts
    active_alerts = (
        StockAlert.query
        .filter(StockAlert.active == True)   # noqa: E712
        .order_by(StockAlert.created_at.desc())
        .all()
    )

    return render_template(
        'dashboard.html',
        stock_summary=stock_summary,
        expiring_soon=expiring_soon,
        open_requests=open_requests,
        active_alerts=active_alerts,
    )


# -----------------------------------------------------------------------------
# Inventory routes
# -----------------------------------------------------------------------------
@main_bp.route('/inventory', methods=['GET'])
def inventory():
    """List blood units with optional filters.

    Query parameters:
        status (str): Filter by status (available, reserved, issued, expired).
        abo_type (str): Filter by ABO type.
        rh_factor (str): Filter by Rh factor.

    Returns:
        Rendered HTML page.
    """
    filter_form = InventoryFilterForm(request.args)
    query = BloodUnit.query

    if filter_form.status.data:
        query = query.filter(BloodUnit.status == filter_form.status.data)
    if filter_form.abo_type.data:
        query = query.filter(BloodUnit.abo_type == filter_form.abo_type.data)
    if filter_form.rh_factor.data:
        query = query.filter(BloodUnit.rh_factor == filter_form.rh_factor.data)

    units = query.order_by(BloodUnit.collection_date.desc()).all()
    add_form = AddBloodUnitForm()

    return render_template(
        'inventory.html',
        units=units,
        add_form=add_form,
        filter_form=filter_form,
    )


@main_bp.route('/inventory/add', methods=['POST'])
def add_blood_unit():
    """Add a new blood unit to the inventory.

    Expects form data: abo_type, rh_factor, collection_date.
    Validates using AddBloodUnitForm and saves to database.

    Returns:
        Redirect to inventory page with success/error message.
    """
    form = AddBloodUnitForm()
    if form.validate_on_submit():
        try:
            unit = BloodUnit(
                abo_type=form.abo_type.data,
                rh_factor=form.rh_factor.data,
                collection_date=datetime.combine(
                    form.collection_date.data, datetime.min.time()
                ),
            )
            db.session.add(unit)
            db.session.commit()
            flash('Blood unit added successfully.', 'success')
            current_app.logger.info(f'Added blood unit {unit.id}')
        except Exception as exc:
            db.session.rollback()
            current_app.logger.error(f'Failed to add blood unit: {exc}')
            flash('Failed to add blood unit. Please try again.', 'danger')
    else:
        # Collect validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('main.inventory'))


@main_bp.route('/inventory/<int:unit_id>/issue', methods=['POST'])
def issue_blood_unit(unit_id):
    """Issue a reserved blood unit (confirm usage).

    Only units in 'reserved' status can be issued. The reservation is marked
    as confirmed and the unit status changes to 'issued'.

    Args:
        unit_id: ID of the blood unit to issue.

    Returns:
        Redirect to inventory page with message.
    """
    unit = BloodUnit.query.get_or_404(unit_id)
    if unit.status != 'reserved':
        flash('Only reserved units can be issued.', 'warning')
        return redirect(url_for('main.inventory'))

    try:
        if unit.issue():
            db.session.commit()
            flash(f'Blood unit {unit.id} has been issued.', 'success')
            current_app.logger.info(f'Issued blood unit {unit.id}')
        else:
            flash('Failed to issue blood unit.', 'danger')
    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f'Error issuing unit {unit_id}: {exc}')
        flash('An error occurred while issuing the unit.', 'danger')

    return redirect(url_for('main.inventory'))


# -----------------------------------------------------------------------------
# Transfusion request routes
# -----------------------------------------------------------------------------
@main_bp.route('/requests', methods=['GET'])
def requests():
    """List transfusion requests with optional filter.

    Query parameters:
        status (str): Filter by status (pending, fulfilled, cancelled).

    Returns:
        Rendered HTML page with request list and new request form.
    """
    filter_form = RequestFilterForm(request.args)
    query = TransfusionRequest.query

    if filter_form.status.data:
        query = query.filter(TransfusionRequest.status == filter_form.status.data)

    request_list = query.order_by(TransfusionRequest.created_at.desc()).all()
    new_request_form = TransfusionRequestForm()

    return render_template(
        'requests.html',
        request_list=request_list,
        new_request_form=new_request_form,
        filter_form=filter_form,
    )


@main_bp.route('/requests/new', methods=['POST'])
def new_request():
    """Create a new transfusion request and perform auto-matching.

    Expects form data: abo_type, rh_factor, quantity.
    Runs the matching service to reserve compatible units.

    Returns:
        Redirect to dashboard with result message.
    """
    form = TransfusionRequestForm()
    if form.validate_on_submit():
        request_obj = TransfusionRequest(
            abo_type=form.abo_type.data,
            rh_factor=form.rh_factor.data,
            quantity=form.quantity.data,
        )

        try:
            # Use matching service to auto-match and reserve
            success = MatchingService.auto_match_and_reserve(request_obj)
            if success:
                db.session.commit()
                flash(
                    f'Request #{request_obj.id} created and fulfilled '
                    f'({request_obj.quantity} units reserved).',
                    'success',
                )
                current_app.logger.info(
                    f'Request {request_obj.id} fulfilled with auto-match.'
                )
            else:
                # If not enough units, save the request as pending
                db.session.add(request_obj)
                db.session.commit()
                flash(
                    f'Request #{request_obj.id} created but not enough '
                    f'compatible units available. Status: pending.',
                    'warning',
                )
                current_app.logger.info(
                    f'Request {request_obj.id} created (pending) - '
                    f'insufficient units.'
                )
        except Exception as exc:
            db.session.rollback()
            current_app.logger.error(f'Error creating request: {exc}')
            flash('Failed to create transfusion request.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('main.dashboard'))


@main_bp.route('/requests/<int:request_id>/cancel', methods=['POST'])
def cancel_request(request_id):
    """Cancel a pending transfusion request and release all reserved units.

    Only requests in 'pending' status can be cancelled.

    Args:
        request_id: ID of the transfusion request to cancel.

    Returns:
        Redirect to requests page with message.
    """
    request_obj = TransfusionRequest.query.get_or_404(request_id)
    if request_obj.status != 'pending':
        flash('Only pending requests can be cancelled.', 'warning')
        return redirect(url_for('main.requests'))

    try:
        if request_obj.cancel():
            db.session.commit()
            flash(f'Request #{request_id} cancelled and units released.', 'success')
            current_app.logger.info(f'Request {request_id} cancelled.')
        else:
            flash('Failed to cancel request.', 'danger')
    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f'Error cancelling request {request_id}: {exc}')
        flash('An error occurred while cancelling the request.', 'danger')

    return redirect(url_for('main.requests'))


# -----------------------------------------------------------------------------
# Alerts route
# -----------------------------------------------------------------------------
@main_bp.route('/alerts')
def alerts():
    """Display all stock alerts (active and resolved), newest first.

    Returns:
        Rendered HTML page.
    """
    alert_list = (
        StockAlert.query
        .order_by(StockAlert.created_at.desc())
        .all()
    )
    return render_template('alerts.html', alert_list=alert_list)


# -----------------------------------------------------------------------------
# (Optional) Resolve an alert manually
# -----------------------------------------------------------------------------
@main_bp.route('/alerts/<int:alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Mark a stock alert as resolved.

    Args:
        alert_id: ID of the alert to resolve.

    Returns:
        Redirect to alerts page.
    """
    alert = StockAlert.query.get_or_404(alert_id)
    try:
        alert.resolve()
        db.session.commit()
        flash(f'Alert #{alert_id} resolved.', 'success')
    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f'Error resolving alert {alert_id}: {exc}')
        flash('Failed to resolve alert.', 'danger')
    return redirect(url_for('main.alerts'))
