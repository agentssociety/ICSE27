```python
## routes_api.py
"""
API routes for the social media platform.
Provides RESTful endpoints for posts, users, groups, notifications, and search.
All responses are JSON-formatted.
"""

import json
from typing import Optional, Tuple, Any

from flask import (
    Blueprint, request, jsonify, current_app, abort, url_for
)
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.exceptions import Forbidden

from extensions import db
from models import (
    User, Post, Comment, Like, Group, GroupMembership, Notification,
    Bookmark, Report, Block, Follow
)
from forms import PostForm, CommentForm, GroupForm, SearchForm
from utils import (
    save_image, create_notification, paginate_query, get_pagination_metadata
)

# Create the API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def get_blocked_ids(user: User) -> set:
    """Return set of user IDs that block or are blocked by the given user."""
    blocked_by_me = {b.blocked_id for b in Block.query.filter_by(blocker_id=user.id).all()}
    blocked_me = {b.blocker_id for b in Block.query.filter_by(blocked_id=user.id).all()}
    return blocked_by_me | blocked_me


def user_to_dict(user: User) -> dict:
    """Convert a User object to a dictionary for API responses."""
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'email_verified': user.email_verified,
        'profile_picture': url_for('static', filename=user.profile_picture) if user.profile_picture else None,
        'cover_photo': url_for('static', filename=user.cover_photo) if user.cover_photo else None,
        'bio': user.bio,
        'location': user.location,
        'is_private': user.is_private,
        'is_verified': user.is_verified,
        'is_admin': user.is_admin,
        'is_active': user.is_active,
        'is_deleted': user.is_deleted,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat(),
        'followers_count': Follow.query.filter_by(followed_id=user.id).count(),
        'following_count': Follow.query.filter_by(follower_id=user.id).count(),
        'posts_count': Post.query.filter_by(user_id=user.id, is_deleted=False).count()
    }


def post_to_dict(post: Post) -> dict:
    """Convert a Post object to a dictionary for API responses."""
    return {
        'id': post.id,
        'user_id': post.user_id,
        'author': user_to_dict(post.author) if post.author else None,
        'content': post.content,
        'images': json.loads(post.images) if post.images else [],
        'group_id': post.group_id,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'is_deleted': post.is_deleted,
        'like_count': Like.query.filter_by(post_id=post.id).count(),
        'comment_count': Comment.query.filter_by(post_id=post.id, is_deleted=False).count(),
        'is_liked': current_user.is_authenticated and Like.query.filter_by(
            post_id=post.id, user_id=current_user.id).first() is not None,
        'is_bookmarked': current_user.is_authenticated and Bookmark.query.filter_by(
            post_id=post.id, user_id=current_user.id).first() is not None
    }


def group_to_dict(group: Group) -> dict:
    """Convert a Group object to a dictionary for API responses."""
    return {
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'is_public': group.is_public,
        'creator_id': group.creator_id,
        'created_at': group.created_at.isoformat(),
        'is_deleted': group.is_deleted,
        'members_count': GroupMembership.query.filter_by(group_id=group.id).count()
    }


def notification_to_dict(notif: Notification) -> dict:
    """Convert a Notification object to a dictionary for API responses."""
    return {
        'id': notif.id,
        'user_id': notif.user_id,
        'type': notif.type,
        'source_id': notif.source_id,
        'message': notif.message,
        'is_read': notif.is_read,
        'created_at': notif.created_at.isoformat()
    }


# ----------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------

@api_bp.route('/posts', methods=['GET'])
@login_required
def get_posts():
    """
    GET /api/posts?page=1&per_page=20
    Returns paginated feed posts. Excludes posts from blocked users and group posts.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 20

    blocked_ids = get_blocked_ids(current_user)
    followed_ids = [f.followed_id for f in
                    Follow.query.filter_by(follower_id=current_user.id).all()]
    feed_user_ids = set(followed_ids + [current_user.id]) - blocked_ids

    if feed_user_ids:
        query = Post.query.filter(
            Post.user_id.in_(feed_user_ids),
            Post.is_deleted == False,
            Post.group_id.is_(None)
        ).order_by(Post.created_at.desc())
    else:
        query = Post.query.filter(
            Post.is_deleted == False,
            Post.group_id.is_(None)
        ).order_by(Post.created_at.desc())

    total = query.count()
    items, has_next, has_prev = paginate_query(query, page, per_page)
    posts_list = [post_to_dict(p) for p in items]

    pagination = get_pagination_metadata(page, per_page, total)

    return jsonify({
        'success': True,
        'data': posts_list,
        'pagination': pagination
    })


@api_bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    """
    POST /api/posts
    Create a new post. Expects multipart/form-data with content and optional images.
    Returns the created post data.
    """
    content = request.form.get('content', '').strip()
    if not content:
        return jsonify({'success': False, 'error': 'Content is required.'}), 400

    # Process uploaded images
    uploaded_files = request.files.getlist('images')
    valid_files = [f for f in uploaded_files if f and f.filename]
    if len(valid_files) > 5:
        return jsonify({'success': False, 'error': 'Maximum 5 images allowed.'}), 400

    image_paths = []
    for file in valid_files:
        file.seek(0)  # Ensure file pointer is at start
        saved_path = save_image(file, subfolder='posts')
        if saved_path:
            image_paths.append(saved_path)

    post = Post(
        user_id=current_user.id,
        content=content,
        images=json.dumps(image_paths)
    )
    db.session.add(post)
    db.session.commit()

    # Notify followers about new post (based on their notification preferences)
    followers = Follow.query.filter_by(followed_id=current_user.id).all()
    for follow in followers:
        follower = User.query.get(follow.follower_id)
        if follower and follower.notification_preference and follower.notification_preference.likes:
            create_notification(
                user_id=follower.id,
                notification_type='post',
                source_id=post.id,
                message=f'{current_user.username} created a new post.'
            )

    return jsonify({
        'success': True,
        'data': post_to_dict(post)
    }), 201


@api_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id: int):
    """
    POST /api/posts/<id>/like
    Toggle like on a post. Returns updated like status and count.
    """
    post = Post.query.get_or_404(post_id)
    if post.is_deleted:
        abort(404)

    existing_like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        liked = False
    else:
        like = Like(post_id=post_id, user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
        liked = True

        # Notify post owner
        if post.user_id != current_user.id:
            owner = User.query.get(post.user_id)
            if owner and owner.notification_preference and owner.notification_preference.likes:
                create_notification(
                    user_id=post.user_id,
                    notification_type='like',
                    source_id=post_id,
                    message=f'{current_user.username} liked your post.'
                )

    like_count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({
        'success': True,
        'liked': liked,
        'like_count': like_count
    })


@api_bp.route('/posts/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id: int):
    """
    POST /api/posts/<id>/comment
    Add a comment to a post. Expects JSON with 'content' field.
    Returns the created comment data.
    """
    post = Post.query.get_or_404(post_id)
    if post.is_deleted:
        abort(404)

    data = request.get_json()
    if not data or not data.get('content', '').strip():
        return jsonify({'success': False, 'error': 'Comment content is required.'}), 400

    content = data['content'].strip()
    if len(content) > 2000:
        return jsonify({'success': False, 'error': 'Comment must be at most 2000 characters.'}), 400

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=content
    )
    db.session.add(comment)
    db.session.commit()

    # Notify post owner
    if post.user_id != current_user.id:
        owner = User.query.get(post.user_id)
        if owner and owner.notification_preference and owner.notification_preference.comments:
            create_notification(
                user_id=post.user_id,
                notification_type='comment',
                source_id=comment.id,
                message=f'{current_user.username} commented on your post.'
            )

    comment_data = {
        'id': comment.id,
        'post_id': comment.post_id,
        'user_id': comment.user_id,
        'author': user_to_dict(current_user),
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat(),
        'is_deleted': comment.is_deleted
    }

    return jsonify({
        'success': True,
        'data': comment_data
    }), 201


@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id: int):
    """
    GET /api/users/<id>
    Returns public profile data for a user.
    """
    user = User.query.get_or_404(user_id)
    if user.is_deleted:
        abort(404)

    # Check if blocked
    if current_user.is_authenticated:
        if Block.query.filter_by(blocker_id=current_user.id, blocked_id=user_id).first():
            abort(404)
        if Block.query.filter_by(blocker_id=user_id, blocked_id=current_user.id).first():
            abort(404)

    return jsonify({
        'success': True,
        'data': user_to_dict(user)
    })


@api_bp.route('/groups', methods=['GET'])
@login_required
def get_groups():
    """
    GET /api/groups?page=1&per_page=20
    Returns paginated list of groups the user can see (public groups and groups they are member of).
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 20

    # Get groups that are public or where user is a member
    user_group_ids = [gm.group_id for gm in GroupMembership.query.filter_by(user_id=current_user.id).all()]
    query = Group.query.filter(
        Group.is_deleted == False,
        or_(Group.is_public == True, Group.id.in_(user_group_ids))
    ).order_by(Group.created_at.desc())

    total = query.count()
    items, has_next, has_prev = paginate_query(query, page, per_page)
    groups_list = [group_to_dict(g) for g in items]
    pagination = get_pagination_metadata(page, per_page, total)

    return jsonify({
        'success': True,
        'data': groups_list,
        'pagination': pagination
    })


@api_bp.route('/groups', methods=['POST'])
@login_required
def create_group():
    """
    POST /api/groups
    Create a new group. Expects JSON with name, description (optional), is_public (optional).
    Returns the created group data.
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body must be JSON.'}), 400

    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    is_public = data.get('is_public', True)

    if not name:
        return jsonify({'success': False, 'error': 'Group name is required.'}), 400
    if len(name) > 100:
        return jsonify({'success': False, 'error': 'Group name must be at most 100 characters.'}), 400

    group = Group(
        name=name,
        description=description,
        is_public=is_public,
        creator_id=current_user.id
    )
    db.session.add(group)
    db.session.flush()  # Get group id

    # Creator becomes admin
    membership = GroupMembership(
        group_id=group.id,
        user_id=current_user.id,
        role='admin'
    )
    db.session.add(membership)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': group_to_dict(group)
    }), 201


@api_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    """
    GET /api/notifications?page=1&per_page=20
    Returns paginated list of notifications for the current user.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 20

    query = Notification.query.filter_by(user_id=current_user.id)\
                              .order_by(Notification.created_at.desc())

    total = query.count()
    items, has_next, has_prev = paginate_query(query, page, per_page)
    notifs_list = [notification_to_dict(n) for n in items]
    pagination = get_pagination_metadata(page, per_page, total)

    return jsonify({
        'success': True,
        'data': notifs_list,
        'pagination': pagination
    })


@api_bp.route('/notifications/mark-read', methods=['POST'])
@login_required
def mark_notifications_read():
    """
    POST /api/notifications/mark-read
    Mark all unread notifications as read for the current user.
    """
    Notification.query.filter_by(user_id=current_user.id, is_read=False)\
                      .update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True, 'message': 'All notifications marked as read.'})


@api_bp.route('/search', methods=['GET'])
@login_required
def search():
    """
    GET /api/search?q=<query>&type=users|posts|groups&page=1&per_page=10
    Search users, posts, groups. 'type' defaults to 'all'.
    Returns paginated results for each category if applicable.
    """
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all').strip().lower()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not query:
        return jsonify({'success': False, 'error': 'Search query is required.'}), 400

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10

    results = {}
    blocked_ids = get_blocked_ids(current_user)

    if search_type in ('all', 'users'):
        users_query = User.query.filter(
            User.is_deleted == False,
            User.is_active == True,
            User.id.notin_(blocked_ids),
            or_(
                User.username.ilike(f'%{query}%'),
                User.email.ilike(f'%{query}%')
            )
        ).order_by(User.username)
        users_total = users_query.count()
        users_items, _, _ = paginate_query(users_query, page, per_page)
        results['users'] = {
            'data': [user_to_dict(u) for u in users_items],
            'pagination': get_pagination_metadata(page, per_page, users_total)
        }

    if search_type in ('all', 'posts'):
        posts_query = Post.query.filter(
            Post.is_deleted == False,
            Post.content.ilike(f'%{query}%'),
            Post.user_id.notin_(blocked_ids)
        ).order_by(Post.created_at.desc())
        posts_total = posts_query.count()
        posts_items, _, _ = paginate_query(posts_query, page, per_page)
        results