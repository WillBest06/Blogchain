from flask import Blueprint, render_template
from flask_login import current_user
from ..models import User, Post, db

profile_bp = Blueprint("profile", __name__)

@profile_bp.route('/<username>')
def profile(username):
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    posts = db.session.execute(db.select(Post).where(Post.user_id == user.id).order_by(Post.created.desc())).scalars().all()
    
    for post in posts:
        post.replies = db.session.execute(db.select(Post).where(Post.parent_id == post.id).order_by(Post.created.desc())).scalars().all()
    return render_template('profile.html', current_user=current_user, posts=posts)