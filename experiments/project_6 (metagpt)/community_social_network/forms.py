## forms.py
"""
WTForms definitions for the social media platform.
All forms use Flask-WTF with CSRF protection and appropriate validators.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField, FileAllowed, FileSize
from wtforms import (
    StringField, PasswordField, BooleanField, TextAreaField,
    SelectField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Optional, ValidationError
)
from models import User


class RegistrationForm(FlaskForm):
    """User registration form with email, username, and password fields."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required.'),
            Email(message='Please enter a valid email address.'),
            Length(max=120, message='Email must be at most 120 characters.')
        ]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=8, message='Password must be at least 8 characters.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password.'),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')

    def validate_email(self, field):
        """Check if email is already registered."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered.')

    def validate_username(self, field):
        """Check if username is already taken."""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already taken.')


class LoginForm(FlaskForm):
    """User login form with email and password fields."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required.'),
            Email(message='Please enter a valid email address.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Password is required.')]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    """Post creation form with content and optional image uploads (up to 5 images)."""
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message='Post content is required.'),
            Length(max=5000, message='Post content must be at most 5000 characters.')
        ]
    )
    images = MultipleFileField(
        'Images (max 5, each < 16MB)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only (jpg, jpeg, png, gif).')
            # FileSize is intentionally omitted here because it only checks the first file.
            # File size validation is handled per file in the route.
        ]
    )
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    """Comment creation form with content field."""
    content = TextAreaField(
        'Comment',
        validators=[
            DataRequired(message='Comment content is required.'),
            Length(max=2000, message='Comment must be at most 2000 characters.')
        ]
    )
    submit = SubmitField('Comment')


class GroupForm(FlaskForm):
    """Group creation form with name, description, and visibility."""
    name = StringField(
        'Group Name',
        validators=[
            DataRequired(message='Group name is required.'),
            Length(min=2, max=100, message='Group name must be between 2 and 100 characters.')
        ]
    )
    description = TextAreaField(
        'Description',
        validators=[
            Optional(),
            Length(max=2000, message='Description must be at most 2000 characters.')
        ]
    )
    is_public = BooleanField('Public Group', default=True)
    submit = SubmitField('Create Group')


class ProfileEditForm(FlaskForm):
    """Profile editing form with bio, location, and photo uploads."""
    bio = TextAreaField(
        'Bio',
        validators=[
            Optional(),
            Length(max=500, message='Bio must be at most 500 characters.')
        ]
    )
    location = StringField(
        'Location',
        validators=[
            Optional(),
            Length(max=100, message='Location must be at most 100 characters.')
        ]
    )
    profile_picture = FileField(
        'Profile Picture',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only (jpg, jpeg, png, gif).'),
            FileSize(max_size=5 * 1024 * 1024, message='Image must be less than 5 MB.')
        ]
    )
    cover_photo = FileField(
        'Cover Photo',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only (jpg, jpeg, png, gif).'),
            FileSize(max_size=10 * 1024 * 1024, message='Image must be less than 10 MB.')
        ]
    )
    is_private = BooleanField('Private Account')
    submit = SubmitField('Update Profile')


class NotificationPreferencesForm(FlaskForm):
    """Notification preferences form for controlling in-app notifications."""
    likes = BooleanField('Like Notifications', default=True)
    comments = BooleanField('Comment Notifications', default=True)
    friend_requests = BooleanField('Friend Request Notifications', default=True)
    submit = SubmitField('Save Preferences')


class SearchForm(FlaskForm):
    """Search form with query and type filter."""
    query = StringField(
        'Search',
        validators=[DataRequired(message='Search query is required.')]
    )
    search_type = SelectField(
        'Type',
        choices=[
            ('all', 'All'),
            ('users', 'Users'),
            ('posts', 'Posts'),
            ('groups', 'Groups')
        ],
        default='all'
    )
    submit = SubmitField('Search')


class PasswordResetRequestForm(FlaskForm):
    """Password reset request form with email field."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required.'),
            Email(message='Please enter a valid email address.')
        ]
    )
    submit = SubmitField('Request Password Reset')


class PasswordResetForm(FlaskForm):
    """Password reset form with new password and confirmation."""
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=8, message='Password must be at least 8 characters.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(message='Please confirm your password.'),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Reset Password')


class ReportForm(FlaskForm):
    """Report form for reporting posts with reason."""
    reason = TextAreaField(
        'Reason for Report',
        validators=[
            DataRequired(message='Please provide a reason for the report.'),
            Length(max=1000, message='Reason must be at most 1000 characters.')
        ]
    )
    submit = SubmitField('Submit Report')


class MessageForm(FlaskForm):
    """Private message form with content field."""
    content = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Message content is required.'),
            Length(max=5000, message='Message must be at most 5000 characters.')
        ]
    )
    submit = SubmitField('Send')


class AdminUserEditForm(FlaskForm):
    """Admin form for editing user status and verification."""
    is_active = BooleanField('Active')
    is_verified = BooleanField('Verified')
    is_admin = BooleanField('Admin')
    submit = SubmitField('Update User')
