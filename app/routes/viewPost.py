from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import current_user
from ..models import User, Post, db

viewPost_bp = Blueprint("viewPost", __name__)

@viewPost_bp.route('/<username>/<int:post_id>')
def viewPost(username, post_id):
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalar()
    post.replies = db.session.execute(db.select(Post).where(Post.parent_id == post.id).order_by(Post.created.desc())).scalars().all()
    parent_post = None

    if post:
        author = db.session.execute(db.select(User).where(User.id == post.user_id)).scalar()
        post.author = author.username

        parent_id = post.parent_id
        
        if parent_id:
            parent_post = db.session.execute(db.select(Post).where(Post.id == parent_id)).scalar()
            author = db.session.execute(db.select(User).where(User.id == parent_post.user_id)).scalar()
            parent_post.author = author.username
    else:
        abort(404)

    return render_template('viewPost.html', post=post, parent=parent_post)