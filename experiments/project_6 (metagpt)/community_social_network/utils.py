"""
Utility functions for the social media platform.
Handles image processing, email sending, notification creation, and pagination.
"""

import os
from typing import Optional, Tuple, List, Any

from flask import current_app, url_for, render_template
from PIL import Image
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message

from extensions import mail, db
from models import Notification


def save_image(file: Any, subfolder: str = 'uploads', max_size: Tuple[int, int] = (1200, 1200),
               thumbnail: bool = False, thumbnail_size: Tuple[int, int] = (300, 300)) -> Optional[str]:
    """
    Save an uploaded image using Pillow, resize to max_size, and return the relative path.

    Args:
        file: File object from request.files (must have read() method).
        subfolder: Subdirectory under the app's upload folder (e.g., 'profile_pictures').
        max_size: Maximum width/height tuple. Image will be downscaled to fit within these bounds.
        thumbnail: If True, also save a thumbnail version with `_thumb` suffix.
        thumbnail_size: Size for the thumbnail.

    Returns:
        Relative file path (e.g., 'uploads/profile_pictures/filename.jpg') or None on failure.
    """
    if not file or not file.filename:
        return None

    # Ensure the upload directory exists
    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_folder, exist_ok=True)

    # Generate a safe filename (simple approach: use original name; production should use UUID)
    filename = file.filename
    # Basic sanitization: remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    # Add timestamp to avoid collisions
    import time
    name, ext = os.path.splitext(filename)
    safe_filename = f"{name}_{int(time.time())}{ext}"

    filepath = os.path.join(upload_folder, safe_filename)

    try:
        img = Image.open(file)
        # Ensure RGB mode for JPEG compatibility
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Resize while maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(filepath, optimize=True, quality=85)

        # Optionally create a thumbnail
        if thumbnail:
            thumb_filename = f"{name}_{int(time.time())}_thumb{ext}"
            thumb_path = os.path.join(upload_folder, thumb_filename)
            thumb_img = img.copy()
            thumb_img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            thumb_img.save(thumb_path, optimize=True, quality=70)

        # Return relative path from static folder or uploads root
        # Here we return path relative to the UPLOAD_FOLDER
        relative_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder, safe_filename)
        return relative_path.replace('\\', '/')
    except Exception as e:
        current_app.logger.error(f"Image saving failed: {e}")
        return None


def generate_confirmation_token(email: str) -> str:
    """Generate a secure token for email verification using itsdangerous."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')


def confirm_token(token: str, expiration: int = 3600) -> Optional[str]:
    """Verify a token and return the original email if valid and not expired."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return None
    return email


def send_verification_email(user: 'User') -> bool:
    """
    Send a verification email to the user.

    Args:
        user: User model instance (must have email attribute).

    Returns:
        True if email sent successfully, False otherwise.
    """
    token = generate_confirmation_token(user.email)
    verify_url = url_for('auth.verify_email', token=token, _external=True)

    msg = Message(
        subject='Email Verification - Social Platform',
        recipients=[user.email],
        html=render_template('email/verify_email.html', user=user, verify_url=verify_url)
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email to {user.email}: {e}")
        return False


def send_password_reset_email(user: 'User') -> bool:
    """
    Send a password reset email to the user.

    Args:
        user: User model instance.

    Returns:
        True if email sent successfully, False otherwise.
    """
    token = generate_confirmation_token(user.email)
    reset_url = url_for('auth.reset_password', token=token, _external=True)

    msg = Message(
        subject='Password Reset - Social Platform',
        recipients=[user.email],
        html=render_template('email/reset_password.html', user=user, reset_url=reset_url)
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send password reset email to {user.email}: {e}")
        return False


def create_notification(user_id: int, notification_type: str, source_id: Optional[int] = None,
                        message: str = '') -> Optional[Notification]:
    """
    Create and save a new notification for a user.

    Args:
        user_id: ID of the user to notify.
        notification_type: Type of notification (e.g., 'like', 'comment', 'friend_request', 'group_invite').
        source_id: ID of the related object (post, comment, request, etc.) or None.
        message: Human-readable message for the notification.

    Returns:
        Notification instance if created successfully, None otherwise.
    """
    if not user_id:
        return None

    notification = Notification(
        user_id=user_id,
        type=notification_type,
        source_id=source_id,
        message=message
    )
    try:
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to create notification for user {user_id}: {e}")
        return None


def paginate_query(query, page: int = 1, per_page: int = 20) -> Tuple[List[Any], bool, bool]:
    """
    Paginate a SQLAlchemy query and return results along with pagination metadata.

    Args:
        query: SQLAlchemy query object (e.g., Post.query.order_by(Post.created_at.desc())).
        page: Current page number (1-indexed).
        per_page: Number of items per page.

    Returns:
        Tuple containing:
            - List of items for the current page.
            - Boolean indicating if there is a next page.
            - Boolean indicating if there is a previous page.
    """
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 1

    total = query.count()
    offset = (page - 1) * per_page
    items = query.limit(per_page).offset(offset).all()

    has_next = (offset + per_page) < total
    has_prev = page > 1

    return items, has_next, has_prev


def get_pagination_metadata(page: int, per_page: int, total: int) -> dict:
    """
    Generate pagination metadata dictionary for API responses.

    Args:
        page: Current page number.
        per_page: Items per page.
        total: Total number of items.

    Returns:
        Dictionary with keys: page, per_page, total, pages, has_prev, has_next.
    """
    pages = (total + per_page - 1) // per_page if total > 0 else 1
    return {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': pages,
        'has_prev': page > 1,
        'has_next': page < pages
    }
