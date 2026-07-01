```python
"""
Main routes for the social media platform.
Handles feed, posts, likes, comments, friend requests, groups, messaging,
user profiles, search, notifications, settings, and account deletion.
"""

import json
import os
from typing import Optional, Tuple, List, Any

from flask import (
    Blueprint, render_template, redirect, url_for, flash, request,
    current_app, jsonify, abort
)
from flask_login import login_required, current_user

from extensions import db
from models import (
    User, Post, Comment, Like, FriendRequest, Follow, Group,
    GroupMembership, GroupJoinRequest, Message, Notification,
    Bookmark, Report, Block, NotificationPreference
)
from forms import (
    PostForm, CommentForm, GroupForm, ProfileEditForm,
    NotificationPreferencesForm, SearchForm, ReportForm, MessageForm
)
from utils import (
    save_image, create_notification, paginate_query, get_pagination_metadata
)

# Create the main blueprint
main_bp = Blueprint('main', __name__)

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
MAX_IMAGES_PER_POST = 5
FEED_PER_PAGE = 20
NOTIFICATIONS_PER_PAGE = 20
MESSAGES_PER_PAGE = 50


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def get_blocked_ids(user: User) -> set:
    """Return set of user IDs that block or are blocked by the given user."""
    blocked_by_me = {b.blocked_id for b in Block.query.filter_by(blocker_id=user.id).all()}
    blocked_me = {b.blocker_id for b in Block.query.filter_by(blocked_id=user.id).all()}
    return blocked_by_me | blocked_me


def is_blocked(user_a: User, user_b: User) -> bool:
    """Check if either user has blocked the other."""
    return (Block.query.filter_by(blocker_id=user_a.id, blocked_id=user_b.id).first() is not None or
            Block.query.filter_by(blocker_id=user_b.id, blocked_id=user_a.id).first() is not None)


def redirect_back(default: str = 'main.feed', **kwargs) -> str:
    """Redirect to the previous page or a default route."""
    return redirect(request.referrer or url_for(default, **kwargs))


# ----------------------------------------------------------------------
# Index
# ----------------------------------------------------------------------
@main_bp.route('/')
def index():
    """Landing page. Redirects to feed if logged in, else shows welcome."""
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    return render_template('main/index.html', title='Welcome')


# ----------------------------------------------------------------------
# Feed
# ----------------------------------------------------------------------
@main_bp.route('/feed')
@login_required
def feed():
    """
    Display paginated feed of posts from followed users and own posts.
    Excludes posts from blocked users and posts by users who blocked the current user.
    Also excludes group posts (they appear in group pages).
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', FEED_PER_PAGE, type=int)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = FEED_PER_PAGE

    blocked_ids = get_blocked_ids(current_user)
    followed_ids = [f.followed_id for f in
                    Follow.query.filter_by(follower_id=current_user.id).all()]
    # Include own posts
    feed_user_ids = set(followed_ids + [current_user.id]) - blocked_ids

    if feed_user_ids:
        query = Post.query.filter(
            Post.user_id.in_(feed_user_ids),
            Post.is_deleted == False,
            Post.group_id.is_(None)  # Exclude group posts
        ).order_by(Post.created_at.desc())
    else:
        # Fallback to most recent public posts if no follows
        query = Post.query.filter(
            Post.is_deleted == False,
            Post.group_id.is_(None)
        ).order_by(Post.created_at.desc())

    posts, has_next, has_prev = paginate_query(query, page, per_page)
    return render_template(
        'main/feed.html',
        title='Feed',
        posts=posts,
        page=page,
        per_page=per_page,
        has_next=has_next,
        has_prev=has_prev
    )


# ----------------------------------------------------------------------
# Post Creation
# ----------------------------------------------------------------------
@main_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Create a new post.
    GET: Display post creation form.
    POST: Validate form, save images (max 5), create post, notify followers.
    """
    form = PostForm()
    if form.validate_on_submit():
        # Process uploaded images
        uploaded_files = request.files.getlist('images')
        # Filter out empty files and enforce maximum count
        valid_files = [f for f in uploaded_files if f and f.filename]
        if len(valid_files) > MAX_IMAGES_PER_POST:
            flash(f'You can upload a maximum of {MAX_IMAGES_PER_POST} images.', 'danger')
            return render_template('main/create_post.html', title='New Post', form=form)

        image_paths = []
        for file in valid_files:
            # Validate file size per file (16MB max)
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            if file_size > current_app.config['MAX_CONTENT_LENGTH']:
                flash('One or more images exceed the maximum size of 16MB.', 'danger')
                return render_template('main/create_post.html', title='New Post', form=form)
            saved_path = save_image(file, subfolder='posts')
            if saved_path:
                image_paths.append(saved_path)

        post = Post(
            user_id=current_user.id,
            content=form.content.data,
            images=json.dumps(image_paths)
        )
        db.session.add(post)
        db.session.commit()

        # Notify followers about the new post (using 'likes' preference as a proxy)
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

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'post_id': post.id,
                'content': post.content,
                'images': image_paths,
                'created_at': post.created_at.isoformat()
            })
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.feed'))

    return render_template('main/create_post.html', title='New Post', form=form)


# ----------------------------------------------------------------------
# Like Toggle
# ----------------------------------------------------------------------
@main_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id: int):
    """Toggle like on a post. Returns JSON with new like count."""
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
    return jsonify({'liked': liked, 'like_count': like_count})


# ----------------------------------------------------------------------
# Add Comment
# ----------------------------------------------------------------------
@main_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id: int):
    """Add a comment to a post."""
    post = Post.query.get_or_404(post_id)
    if post.is_deleted:
        abort(404)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            post_id=post_id,
            user_id=current_user.id,
            content=form.content.data
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

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'comment_id': comment.id,
                'content': comment.content,
                'username': current_user.username,
                'created_at': comment.created_at.isoformat()
            })
        flash('Comment added!', 'success')
        return redirect(url_for('main.view_post', post_id=post_id))

    flash('Invalid comment.', 'danger')
    return redirect(url_for('main.view_post', post_id=post_id))


# ----------------------------------------------------------------------
# View Single Post
# ----------------------------------------------------------------------
@main_bp.route('/post/<int:post_id>')
@login_required
def view_post(post_id: int):
    """View a single post with its comments."""
    post = Post.query.get_or_404(post_id)
    if post.is_deleted:
        abort(404)
    if is_blocked(current_user, post.author):
        abort(404)
    comments = Comment.query.filter_by(post_id=post_id, is_deleted=False)\
                            .order_by(Comment.created_at.asc()).all()
    return render_template(
        'main/view_post.html',
        title='Post',
        post=post,
        comments=comments,
        comment_form=CommentForm()
    )


# ----------------------------------------------------------------------
# Delete Post (soft delete)
# ----------------------------------------------------------------------
@main_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id: int):
    """Soft delete a post (only the author can delete)."""
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    if post.is_deleted:
        flash('Post already deleted.', 'info')
    else:
        post.soft_delete()
        flash('Post has been deleted.', 'success')
    return redirect_back('main.feed')


# ----------------------------------------------------------------------
# Friend Request Management
# ----------------------------------------------------------------------
@main_bp.route('/friend-request/send/<int:user_id>', methods=['POST'])
@login_required
def send_friend_request(user_id: int):
    """Send a friend request to another user."""
    if user_id == current_user.id:
        flash('You cannot send a friend request to yourself.', 'danger')
        return redirect(url_for('main.user_profile', user_id=user_id))

    target = User.query.get_or_404(user_id)
    if target.is_deleted or not target.is_active:
        abort(404)

    existing_follow = Follow.query.filter_by(
        follower_id=current_user.id, followed_id=user_id
    ).first()
    if existing_follow:
        flash('You are already friends with this user.', 'info')
        return redirect(url_for('main.user_profile', user_id=user_id))

    existing_request = FriendRequest.query.filter_by(
        sender_id=current_user.id, receiver_id=user_id, status='pending'
    ).first()
    if existing_request:
        flash('You have already sent a friend request to this user.', 'info')
        return redirect(url_for('main.user_profile', user_id=user_id))

    if is_blocked(current_user, target):
        flash('You cannot send a friend request to this user.', 'danger')
        return redirect(url_for('main.user_profile', user_id=user_id))

    friend_request = FriendRequest(sender_id=current_user.id, receiver_id=user_id)
    db.session.add(friend_request)
    db.session.commit()

    if target.notification_preference and target.notification_preference.friend_requests:
        create_notification(
            user_id=user_id,
            notification_type='friend_request',
            source_id=friend_request.id,
            message=f'{current_user.username} sent you a friend request.'
        )

    flash('Friend request sent!', 'success')
    return redirect(url_for('main.user_profile', user_id=user_id))


@main_bp.route('/friend-request/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_friend_request(request_id: int):
    """Accept a friend request, creating mutual follow."""
    fr = FriendRequest.query.get_or_404(request_id)
    if fr.receiver_id != current_user.id:
        abort(403)
    if fr.status != 'pending':
        flash('This request is no longer pending.', 'warning')
        return redirect(url_for('main.friends'))

    fr.status = 'accepted'
    follow1 = Follow(follower_id=current_user.id, followed_id=fr.sender_id)
    follow2 = Follow(follower_id=fr.sender_id, followed_id=current_user.id)
    db.session.add(follow1)
    db.session.add(follow2)
    db.session.commit()

    flash('Friend request accepted!', 'success')
    return redirect(url_for('main.friends'))


@main_bp.route('/friend-request/<int:request_id>/reject', methods=['POST'])
@login_required
def reject_friend_request(request_id: int):
    """Reject a friend request."""
    fr = FriendRequest.query.get_or_404(request_id)
    if fr.receiver_id != current_user.id:
        abort(403)
    if fr.status != 'pending':
        flash('This request is no longer pending.', 'warning')
        return redirect(url_for('main.friends'))

    fr.status = 'rejected'
    db.session.commit()
    flash('Friend request rejected.', 'info')
    return redirect(url_for('main.friends'))


@main_bp.route('/friends')
@login_required
def friends():
    """Display friends list and pending friend requests."""
    following_ids = {f.followed_id for f in Follow.query.filter_by(follower_id=current_user.id).all()}
    follower_ids = {f.follower_id for f in Follow.query.filter_by(followed_id=current_user.id).all()}
    friend_ids = following_ids & follower_ids
    friends = User.query.filter(User.id.in_(friend_ids)).all()

    pending_requests = FriendRequest.query.filter_by(
        receiver_id=current_user.id, status='pending'
    ).all()

    return render_template(
        'main/friends.html',
        title='Friends',
        friends=friends,
        pending_requests=pending_requests
    )


# ----------------------------------------------------------------------
# Unfriend / Unfollow
# ----------------------------------------------------------------------
@main_bp.route('/user/<int:user_id>/unfriend', methods=['POST'])
@login_required
def unfriend(user_id: int):
    """Remove mutual follow relationship (unfriend)."""
    if user_id == current_user.id:
        flash('You cannot unfriend yourself.', 'danger')
        return redirect_back('main.friends')

    target = User.query.get_or_404(user_id)
    Follow.query.filter(
        ((Follow.follower_id == current_user.id) & (Follow.followed_id == user_id)) |
        ((Follow.follower_id == user_id) & (Follow.followed_id == current_user.id))
    ).delete()
    db.session.commit()
    flash(f'You have unfriended {target.username}.', 'info')
    return redirect_back('main.friends')


# ----------------------------------------------------------------------
# Block User
# ----------------------------------------------------------------------
@main_bp.route('/user/<int:user_id>/block', methods=['POST'])
@login_required
def block_user(user_id: int):
    """Block a user. Removes any existing follow/friend relationships."""
    if user_id == current_user.id:
        flash('You cannot block yourself.', 'danger')
        return redirect(url_for('main.user_profile', user_id=user_id))

    target = User.query.get_or_404(user_id)

    existing_block = Block.query.filter_by(blocker_id=current_user.id, blocked_id=user_id).first()
    if existing_block:
        flash('User is already blocked.', 'info')
        return redirect(url_for('main.user_profile', user_id=user_id))

    block = Block(blocker_id=current_user.id, blocked_id=user_id)
    db.session.add(block)

    # Remove mutual follows (unfriend)
    Follow.query.filter(
        ((Follow.follower_id == current_user.id) & (Follow.followed_id == user_id)) |
        ((Follow.follower_id == user_id) & (Follow.followed_id == current_user.id))
    ).delete()

    # Remove pending friend requests
    FriendRequest.query.filter(
        ((FriendRequest.sender_id == current_user.id) & (FriendRequest.receiver_id == user_id)) |
        ((FriendRequest.sender_id == user_id) & (FriendRequest.receiver_id == current_user.id))
    ).delete()

    db.session.commit()
    flash(f'You have blocked {target.username}.', 'success')
    return redirect(url_for('main.user_profile', user_id=user_id))


# ----------------------------------------------------------------------
# Unblock User
# ----------------------------------------------------------------------
@main_bp.route('/user/<int:user_id>/unblock', methods=['POST'])
@login_required
def unblock_user(user_id: int):
    """Remove a block."""
    if user_id == current_user.id:
        flash('You cannot unblock yourself.', 'danger')
        return redirect(url_for('main.user_profile', user_id=user_id))

    block = Block.query.filter_by(blocker_id=current_user.id, blocked_id=user_id).first()
    if not block:
        flash('User is not blocked.', 'info')
    else:
        db.session.delete(block)
