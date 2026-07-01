```python
## models.py
"""
Data models for the social media platform.
All models are defined with clear relationships and use soft-delete where appropriate.
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id: str):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model with profile, authentication, and status fields."""
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash: str = db.Column(db.String(256), nullable=False)
    email_verified: bool = db.Column(db.Boolean, default=False)
    profile_picture: str = db.Column(db.String(200), nullable=True, default=None)
    cover_photo: str = db.Column(db.String(200), nullable=True, default=None)
    bio: str = db.Column(db.Text, nullable=True, default='')
    location: str = db.Column(db.String(100), nullable=True, default='')
    is_private: bool = db.Column(db.Boolean, default=False)
    is_admin: bool = db.Column(db.Boolean, default=False)
    is_verified: bool = db.Column(db.Boolean, default=False)
    is_active: bool = db.Column(db.Boolean, default=True)
    is_deleted: bool = db.Column(db.Boolean, default=False)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                     onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic',
                            foreign_keys='Post.user_id')
    comments = db.relationship('Comment', backref='author', lazy='dynamic',
                               foreign_keys='Comment.user_id')
    likes = db.relationship('Like', backref='user', lazy='dynamic',
                            foreign_keys='Like.user_id')
    sent_friend_requests = db.relationship('FriendRequest', backref='sender', lazy='dynamic',
                                           foreign_keys='FriendRequest.sender_id')
    received_friend_requests = db.relationship('FriendRequest', backref='receiver', lazy='dynamic',
                                               foreign_keys='FriendRequest.receiver_id')
    followers = db.relationship('Follow', backref='followed_user', lazy='dynamic',
                                foreign_keys='Follow.followed_id')
    following = db.relationship('Follow', backref='follower_user', lazy='dynamic',
                                foreign_keys='Follow.follower_id')
    created_groups = db.relationship('Group', backref='creator', lazy='dynamic',
                                     foreign_keys='Group.creator_id')
    group_memberships = db.relationship('GroupMembership', backref='user', lazy='dynamic',
                                        foreign_keys='GroupMembership.user_id')
    group_join_requests = db.relationship('GroupJoinRequest', backref='user', lazy='dynamic',
                                          foreign_keys='GroupJoinRequest.user_id')
    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic',
                                    foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', backref='receiver', lazy='dynamic',
                                        foreign_keys='Message.receiver_id')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic',
                                    foreign_keys='Notification.user_id')
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic',
                                foreign_keys='Bookmark.user_id')
    reports = db.relationship('Report', backref='reporter', lazy='dynamic',
                              foreign_keys='Report.reporter_id')
    admin_logs = db.relationship('AdminLog', backref='admin', lazy='dynamic',
                                 foreign_keys='AdminLog.admin_id')
    blocks_initiated = db.relationship('Block', backref='blocker', lazy='dynamic',
                                       foreign_keys='Block.blocker_id')
    blocks_received = db.relationship('Block', backref='blocked', lazy='dynamic',
                                      foreign_keys='Block.blocked_id')
    notification_preference = db.relationship('NotificationPreference', backref='user',
                                              uselist=False, lazy='joined')

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the user's password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def verify_email(self) -> None:
        """Mark the user's email as verified."""
        self.email_verified = True
        db.session.commit()

    def soft_delete(self) -> None:
        """Soft delete the user and all their content."""
        self.is_deleted = True
        self.is_active = False
        # Soft delete all posts
        for post in self.posts:
            post.soft_delete()
        # Soft delete all comments
        for comment in self.comments:
            comment.soft_delete()
        db.session.commit()

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Post(db.Model):
    """Post model with content, images, and group association."""
    __tablename__ = 'posts'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content: str = db.Column(db.Text, nullable=False)
    images: str = db.Column(db.Text, nullable=True, default='[]')  # JSON list of image paths
    group_id: int = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True, index=True)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                     onupdate=lambda: datetime.now(timezone.utc))
    is_deleted: bool = db.Column(db.Boolean, default=False)

    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic',
                               foreign_keys='Comment.post_id')
    likes = db.relationship('Like', backref='post', lazy='dynamic',
                            foreign_keys='Like.post_id')
    bookmarks = db.relationship('Bookmark', backref='post', lazy='dynamic',
                                foreign_keys='Bookmark.post_id')
    reports = db.relationship('Report', backref='post', lazy='dynamic',
                              foreign_keys='Report.post_id')

    def soft_delete(self) -> None:
        """Soft delete the post and its comments."""
        self.is_deleted = True
        for comment in self.comments:
            comment.soft_delete()
        db.session.commit()

    def __repr__(self) -> str:
        return f'<Post {self.id} by User {self.user_id}>'


class Comment(db.Model):
    """Comment model associated with a post and user."""
    __tablename__ = 'comments'

    id: int = db.Column(db.Integer, primary_key=True)
    post_id: int = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content: str = db.Column(db.Text, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                     onupdate=lambda: datetime.now(timezone.utc))
    is_deleted: bool = db.Column(db.Boolean, default=False)

    def soft_delete(self) -> None:
        """Soft delete the comment."""
        self.is_deleted = True
        db.session.commit()

    def __repr__(self) -> str:
        return f'<Comment {self.id} on Post {self.post_id}>'


class Like(db.Model):
    """Like model for tracking post likes."""
    __tablename__ = 'likes'

    id: int = db.Column(db.Integer, primary_key=True)
    post_id: int = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_like'),)

    def __repr__(self) -> str:
        return f'<Like {self.id} by User {self.user_id} on Post {self.post_id}>'


class FriendRequest(db.Model):
    """Friend request model with status tracking."""
    __tablename__ = 'friend_requests'

    id: int = db.Column(db.Integer, primary_key=True)
    sender_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    status: str = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                     onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<FriendRequest {self.id}: {self.sender_id} -> {self.receiver_id} ({self.status})>'


class Follow(db.Model):
    """Follow model for user follow relationships."""
    __tablename__ = 'follows'

    id: int = db.Column(db.Integer, primary_key=True)
    follower_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    followed_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),)

    def __repr__(self) -> str:
        return f'<Follow {self.follower_id} -> {self.followed_id}>'


class Group(db.Model):
    """Group model for community groups."""
    __tablename__ = 'groups'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False, index=True)
    description: str = db.Column(db.Text, nullable=True, default='')
    is_public: bool = db.Column(db.Boolean, default=True)
    creator_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_deleted: bool = db.Column(db.Boolean, default=False)

    # Relationships
    posts = db.relationship('Post', backref='group', lazy='dynamic',
                            foreign_keys='Post.group_id')
    memberships = db.relationship('GroupMembership', backref='group', lazy='dynamic',
                                  foreign_keys='GroupMembership.group_id')
    join_requests = db.relationship('GroupJoinRequest', backref='group', lazy='dynamic',
                                    foreign_keys='GroupJoinRequest.group_id')

    def __repr__(self) -> str:
        return f'<Group {self.name}>'


class GroupMembership(db.Model):
    """Group membership model with role tracking."""
    __tablename__ = 'group_memberships'

    id: int = db.Column(db.Integer, primary_key=True)
    group_id: int = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False, index=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role: str = db.Column(db.String(20), default='member')  # member, admin
    joined_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('group_id', 'user_id', name='unique_membership'),)

    def __repr__(self) -> str:
        return f'<GroupMembership User {self.user_id} in Group {self.group_id} as {self.role}>'


class GroupJoinRequest(db.Model):
    """Group join request model with status tracking."""
    __tablename__ = 'group_join_requests'

    id: int = db.Column(db.Integer, primary_key=True)
    group_id: int = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False, index=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    status: str = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<GroupJoinRequest User {self.user_id} -> Group {self.group_id} ({self.status})>'


class Message(db.Model):
    """Private message model between users."""
    __tablename__ = 'messages'

    id: int = db.Column(db.Integer, primary_key=True)
    sender_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content: str = db.Column(db.Text, nullable=False)
    sent_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_read: bool = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<Message {self.id} from {self.sender_id} to {self.receiver_id}>'


class Notification(db.Model):
    """Notification model for in-app notifications."""
    __tablename__ = 'notifications'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    type: str = db.Column(db.String(50), nullable=False)  # like, comment, friend_request, group_invite
    source_id: int = db.Column(db.Integer, nullable=True)  # id of related object
    message: str = db.Column(db.Text, nullable=False)
    is_read: bool = db.Column(db.Boolean, default=False)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<Notification {self.id} for User {self.user_id} ({self.type})>'


class Bookmark(db.Model):
    """Bookmark model for saving posts."""
    __tablename__ = 'bookmarks'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    post_id: int = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_bookmark'),)

    def __repr__(self) -> str:
        return f'<Bookmark User {self.user_id} on Post {self.post_id}>'


class Report(db.Model):
    """Report model for reporting posts."""
    __tablename__ = 'reports'

    id: int = db.Column(db.Integer, primary_key=True)
    reporter_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    post_id: int = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    reason: str = db.Column(db.Text, nullable=False)
    status: str = db.Column(db.String(20), default='pending')  # pending, reviewed, dismissed
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<Report {self.id} by User {self.reporter_id} on Post {self.post_id} ({self.status})>'


class AdminLog(db.Model):
    """Admin activity log for tracking administrative actions."""
    __tablename__ = 'admin_logs'

    id: int = db.Column(db.Integer, primary_key=True)
    admin_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action: str = db.Column(db.String(100), nullable=False)  # ban, delete, verify, etc.
    target_type: str = db.Column(db.String(50), nullable=False)  # user, post, comment
    target_id: int = db.Column(db.Integer, nullable=False)
    details: str = db.Column(db.Text, nullable=True, default='')
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f'<AdminLog {self.id}: {self.action} on {self.target_type} {self.target_id}>'


class Block(db.Model):
    """Block model for user blocking relationships."""
    __tablename__ = 'blocks'

    id: int = db.Column(db.Integer, primary_key=True)
    blocker_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    blocked_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('blocker_id', 'blocked_id', name='unique_block'),)

    def __repr__(self) -> str:
        return f'<Block {self.blocker_id} blocked {self.blocked_id}>'


class NotificationPreference(db.Model):
    """Notification preferences model for controlling in-app notifications."""
    __tablename__ = 'notification_preferences'

