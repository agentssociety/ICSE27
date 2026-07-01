"""
Admin routes for the social media platform.
Provides admin dashboard, user management, post management,
report handling, and admin activity logs.
Only users with is_admin=True can access these routes.
"""

from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_required, current_user
from werkzeug.exceptions import Forbidden

from extensions import db
from models import (
    User, Post, Comment, Report, AdminLog
)
from forms import AdminUserEditForm
from utils import paginate_query

# Create the admin blueprint with URL prefix /admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ----------------------------------------------------------------------
# Admin access control decorator (used as a before_request hook)
# ----------------------------------------------------------------------
def admin_required():
    """Raise Forbidden if current user is not an admin."""
    if not current_user.is_authenticated or not current_user.is_admin:
        raise Forbidden("You do not have permission to access this page.")


# Register before_request to check admin for all admin routes
@admin_bp.before_request
def before_admin_request():
    """Check admin status before every admin route."""
    # Skip the check for static files or login? Not needed for admin views only.
    admin_required()


# ----------------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------------
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Admin dashboard showing key statistics.
    """
    total_users = User.query.count()
    active_users = User.query.filter_by(is_deleted=False, is_active=True).count()
    total_posts = Post.query.filter_by(is_deleted=False).count()
    total_reports = Report.query.filter_by(status='pending').count()
    total_logs = AdminLog.query.count()

    recent_logs = AdminLog.query.order_by(AdminLog.created_at.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard',
        total_users=total_users,
        active_users=active_users,
        total_posts=total_posts,
        total_reports=total_reports,
        total_logs=total_logs,
        recent_logs=recent_logs
    )


# ----------------------------------------------------------------------
# User Management
# ----------------------------------------------------------------------
@admin_bp.route('/users')
@login_required
def manage_users():
    """
    List all users (including soft-deleted) with pagination.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = User.query.order_by(User.created_at.desc())
    users, has_next, has_prev = paginate_query(query, page, per_page)

    return render_template(
        'admin/manage_users.html',
        title='User Management',
        users=users,
        page=page,
        per_page=per_page,
        has_next=has_next,
        has_prev=has_prev
    )


@admin_bp.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id: int):
    """
    View and edit a specific user's admin-level attributes (active, verified, admin).
    """
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm(obj=user)

    if form.validate_on_submit():
        user.is_active = form.is_active.data
        user.is_verified = form.is_verified.data
        user.is_admin = form.is_admin.data
        db.session.commit()

        # Log the action
        log = AdminLog(
            admin_id=current_user.id,
            action='edit_user',
            target_type='user',
            target_id=user.id,
            details=f'Updated user {user.username}: active={user.is_active}, verified={user.is_verified}, admin={user.is_admin}'
        )
        db.session.add(log)
        db.session.commit()

        flash(f'User {user.username} updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template(
        'admin/edit_user.html',
        title='Edit User',
        user=user,
        form=form
    )


@admin_bp.route('/users/<int:user_id>/suspend', methods=['POST'])
@login_required
def suspend_user(user_id: int):
    """
    Toggle a user's active status (suspend/unsuspend).
    """
    user = User.query.get_or_404(user_id)
    if user.is_admin and user.id != current_user.id:
        flash('You cannot suspend another admin.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user.is_active = not user.is_active
    db.session.commit()

    action = 'suspended' if not user.is_active else 'unsuspended'
    log = AdminLog(
        admin_id=current_user.id,
        action=action,
        target_type='user',
        target_id=user.id,
        details=f'{action} user {user.username}'
    )
    db.session.add(log)
    db.session.commit()

    flash(f'User {user.username} has been {action}.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/users/<int:user_id>/verify', methods=['POST'])
@login_required
def toggle_verified(user_id: int):
    """
    Toggle the verified badge of a user.
    """
    user = User.query.get_or_404(user_id)
    user.is_verified = not user.is_verified
    db.session.commit()

    action = 'verified' if user.is_verified else 'unverified'
    log = AdminLog(
        admin_id=current_user.id,
        action=action,
        target_type='user',
        target_id=user.id,
        details=f'{action} user {user.username}'
    )
    db.session.add(log)
    db.session.commit()

    flash(f'User {user.username} has been {action}.', 'success')
    return redirect(url_for('admin.manage_users'))


# ----------------------------------------------------------------------
# Post Management
# ----------------------------------------------------------------------
@admin_bp.route('/posts')
@login_required
def manage_posts():
    """
    List all posts (including deleted) with pagination for admin review.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Post.query.order_by(Post.created_at.desc())
    posts, has_next, has_prev = paginate_query(query, page, per_page)

    return render_template(
        'admin/manage_posts.html',
        title='Post Management',
        posts=posts,
        page=page,
        per_page=per_page,
        has_next=has_next,
        has_prev=has_prev
    )


@admin_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id: int):
    """
    Soft-delete a post (admin action). Also logs to admin log.
    """
    post = Post.query.get_or_404(post_id)
    if post.is_deleted:
        flash('Post is already deleted.', 'info')
        return redirect(url_for('admin.manage_posts'))

    post.soft_delete()

    log = AdminLog(
        admin_id=current_user.id,
        action='delete_post',
        target_type='post',
        target_id=post.id,
        details=f'Deleted post {post.id} by user {post.user_id}'
    )
    db.session.add(log)
    db.session.commit()

    flash(f'Post {post.id} has been soft-deleted.', 'success')
    return redirect(url_for('admin.manage_posts'))


# ----------------------------------------------------------------------
# Report Management
# ----------------------------------------------------------------------
@admin_bp.route('/reports')
@login_required
def manage_reports():
    """
    List all reports with their status and related post/user info.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Report.query.order_by(
        Report.status.asc(),  # pending first
        Report.created_at.desc()
    )
    reports, has_next, has_prev = paginate_query(query, page, per_page)

    return render_template(
        'admin/manage_reports.html',
        title='Manage Reports',
        reports=reports,
        page=page,
        per_page=per_page,
        has_next=has_next,
        has_prev=has_prev
    )


@admin_bp.route('/reports/<int:report_id>/review', methods=['POST'])
@login_required
def review_report(report_id: int):
    """
    Mark a report as reviewed (without deleting the post).
    """
    report = Report.query.get_or_404(report_id)
    if report.status != 'pending':
        flash('Report has already been processed.', 'info')
        return redirect(url_for('admin.manage_reports'))

    report.status = 'reviewed'
    db.session.commit()

    log = AdminLog(
        admin_id=current_user.id,
        action='review_report',
        target_type='report',
        target_id=report.id,
        details=f'Reviewed report {report.id} on post {report.post_id}'
    )
    db.session.add(log)
    db.session.commit()

    flash(f'Report {report.id} marked as reviewed.', 'success')
    return redirect(url_for('admin.manage_reports'))


@admin_bp.route('/reports/<int:report_id>/dismiss', methods=['POST'])
@login_required
def dismiss_report(report_id: int):
    """
    Dismiss a report (no action taken on the post).
    """
    report = Report.query.get_or_404(report_id)
    if report.status != 'pending':
        flash('Report has already been processed.', 'info')
        return redirect(url_for('admin.manage_reports'))

    report.status = 'dismissed'
    db.session.commit()

    log = AdminLog(
        admin_id=current_user.id,
        action='dismiss_report',
        target_type='report',
        target_id=report.id,
        details=f'Dismissed report {report.id} on post {report.post_id}'
    )
    db.session.add(log)
    db.session.commit()

    flash(f'Report {report.id} dismissed.', 'success')
    return redirect(url_for('admin.manage_reports'))


@admin_bp.route('/reports/<int:report_id>/delete-post', methods=['POST'])
@login_required
def delete_reported_post(report_id: int):
    """
    Soft-delete the post associated with a report and mark report as reviewed.
    """
    report = Report.query.get_or_404(report_id)
    if report.status != 'pending':
        flash('Report has already been processed.', 'info')
        return redirect(url_for('admin.manage_reports'))

    post = Post.query.get(report.post_id)
    if post and not post.is_deleted:
        post.soft_delete()

    report.status = 'reviewed'
    db.session.commit()

    log = AdminLog(
        admin_id=current_user.id,
        action='delete_reported_post',
        target_type='post',
        target_id=report.post_id,
        details=f'Deleted post {report.post_id} due to report {report.id}'
    )
    db.session.add(log)
    db.session.commit()

    flash(f'Post {report.post_id} has been deleted and report {report.id} reviewed.', 'success')
    return redirect(url_for('admin.manage_reports'))


# ----------------------------------------------------------------------
# Admin Activity Logs
# ----------------------------------------------------------------------
@admin_bp.route('/logs')
@login_required
def view_logs():
    """
    Display paginated list of admin activity logs.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    query = AdminLog.query.order_by(AdminLog.created_at.desc())
    logs, has_next, has_prev = paginate_query(query, page, per_page)

    return render_template(
        'admin/admin_logs.html',
        title='Admin Logs',
        logs=logs,
        page=page,
        per_page=per_page,
        has_next=has_next,
        has_prev=has_prev
    )
