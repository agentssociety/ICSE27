"""
Authentication routes for the social media platform.
Handles user registration, login, logout, email verification, and password reset.
"""

from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from extensions import db
from models import User
from forms import (
    RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
)
from utils import (
    send_verification_email, send_password_reset_email,
    confirm_token, generate_confirmation_token
)

# Create the auth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """
    Handle user registration.
    GET: Display registration form.
    POST: Validate form, create user, send verification email, redirect to login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Send verification email
        if send_verification_email(user):
            flash('Account created! Please check your email to verify your account.', 'success')
        else:
            flash('Account created but verification email could not be sent. Contact support.', 'warning')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> str:
    """
    Handle user login.
    GET: Display login form.
    POST: Validate credentials, check email verification, log in user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html', title='Login', form=form)

        if not user.email_verified:
            flash('Please verify your email before logging in.', 'warning')
            return render_template('auth/login.html', title='Login', form=form)

        if not user.is_active or user.is_deleted:
            flash('This account has been deactivated or deleted.', 'danger')
            return render_template('auth/login.html', title='Login', form=form)

        login_user(user, remember=form.remember.data)

        # Redirect to the next page if provided, else to feed
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.feed')
        return redirect(next_page)

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout')
@login_required
def logout() -> str:
    """Log out the current user and redirect to home."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/verify-email/<token>')
def verify_email(token: str) -> str:
    """
    Verify user's email using a secure token.
    If token is valid and not expired, mark email as verified.
    """
    email = confirm_token(token, expiration=3600)  # 1 hour expiration
    if email is None:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))

    if user.email_verified:
        flash('Email already verified. Please log in.', 'info')
    else:
        user.verify_email()
        flash('Your email has been verified! You can now log in.', 'success')

    return redirect(url_for('auth.login'))


@auth_bp.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification() -> str:
    """
    Allow users to request a new verification email.
    GET: Display form.
    POST: Find user by email, resend verification email.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))

    form = PasswordResetRequestForm()  # Reuse email-only form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and not user.email_verified:
            if send_verification_email(user):
                flash('A new verification email has been sent.', 'success')
            else:
                flash('Failed to send verification email. Please try again later.', 'danger')
        else:
            # Don't reveal if email exists or already verified
            flash('If the email is registered and not verified, a new verification email has been sent.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/resend_verification.html', title='Resend Verification', form=form)


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request() -> str:
    """
    Handle password reset request.
    GET: Display form to enter email.
    POST: Send password reset email if user exists.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))

    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if send_password_reset_email(user):
                flash('A password reset email has been sent.', 'success')
            else:
                flash('Failed to send password reset email. Please try again later.', 'danger')
        else:
            # Don't reveal if email exists
            flash('If the email is registered, a password reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token: str) -> str:
    """
    Handle password reset with token.
    GET: Display form to enter new password.
    POST: Validate token, update password.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))

    email = confirm_token(token, expiration=3600)  # 1 hour expiration
    if email is None:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', title='Reset Password', form=form, token=token)
