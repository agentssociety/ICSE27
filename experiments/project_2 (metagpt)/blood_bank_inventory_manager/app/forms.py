"""Flask-WTF forms for the Blood Bank Management Application.

This module defines form classes for adding blood units and creating transfusion
requests. Forms are validated both client-side (via HTML5) and server-side.
"""

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, NumberRange, Optional

# Constants matching database constraints
ABO_TYPES = [
    ('A', 'A'),
    ('B', 'B'),
    ('AB', 'AB'),
    ('O', 'O'),
]

RH_FACTORS = [
    ('positive', 'Positive'),
    ('negative', 'Negative'),
]

BLOOD_UNIT_STATUSES = [
    ('available', 'Available'),
    ('reserved', 'Reserved'),
    ('issued', 'Issued'),
    ('expired', 'Expired'),
]

TRANSFUSION_REQUEST_STATUSES = [
    ('pending', 'Pending'),
    ('fulfilled', 'Fulfilled'),
    ('cancelled', 'Cancelled'),
]


class AddBloodUnitForm(FlaskForm):
    """Form for adding a new blood unit to inventory.

    Fields:
        abo_type: Blood group (A, B, AB, O).
        rh_factor: Rh factor (positive/negative).
        collection_date: Date of blood collection.
        submit: Submit button.
    """

    abo_type = SelectField(
        'Blood Type (ABO)',
        choices=ABO_TYPES,
        validators=[DataRequired(message='Please select an ABO type.')],
        render_kw={'class': 'form-select'}
    )
    rh_factor = SelectField(
        'Rh Factor',
        choices=RH_FACTORS,
        validators=[DataRequired(message='Please select Rh factor.')],
        render_kw={'class': 'form-select'}
    )
    collection_date = DateField(
        'Collection Date',
        validators=[DataRequired(message='Please enter the collection date.')],
        render_kw={'class': 'form-control', 'type': 'date'}
    )
    submit = SubmitField('Add Blood Unit', render_kw={'class': 'btn btn-primary'})

    def validate_collection_date(self, field):
        """Ensure collection date is not in the future."""
        from datetime import date
        if field.data and field.data > date.today():
            raise ValidationError('Collection date cannot be in the future.')


class TransfusionRequestForm(FlaskForm):
    """Form for creating a new transfusion request with auto-matching.

    Fields:
        abo_type: Requested blood group.
        rh_factor: Requested Rh factor.
        quantity: Number of units requested (>=1).
        submit: Submit button.
    """

    abo_type = SelectField(
        'Required Blood Type (ABO)',
        choices=ABO_TYPES,
        validators=[DataRequired(message='Please select an ABO type.')],
        render_kw={'class': 'form-select'}
    )
    rh_factor = SelectField(
        'Required Rh Factor',
        choices=RH_FACTORS,
        validators=[DataRequired(message='Please select Rh factor.')],
        render_kw={'class': 'form-select'}
    )
    quantity = IntegerField(
        'Number of Units Required',
        validators=[
            DataRequired(message='Please enter the quantity.'),
            NumberRange(min=1, message='Quantity must be at least 1.')
        ],
        render_kw={'class': 'form-control', 'type': 'number', 'min': '1'}
    )
    submit = SubmitField('Submit Request', render_kw={'class': 'btn btn-primary'})


class InventoryFilterForm(FlaskForm):
    """Form/helper for filtering the inventory list (not submitted to API)."""

    status = SelectField(
        'Status',
        choices=[('', 'All')] + BLOOD_UNIT_STATUSES,
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    abo_type = SelectField(
        'Blood Type',
        choices=[('', 'All')] + ABO_TYPES,
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    rh_factor = SelectField(
        'Rh Factor',
        choices=[('', 'All')] + RH_FACTORS,
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    submit = SubmitField('Filter', render_kw={'class': 'btn btn-outline-secondary'})


class RequestFilterForm(FlaskForm):
    """Form/helper for filtering transfusion requests list."""

    status = SelectField(
        'Status',
        choices=[('', 'All')] + TRANSFUSION_REQUEST_STATUSES,
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    submit = SubmitField('Filter', render_kw={'class': 'btn btn-outline-secondary'})
