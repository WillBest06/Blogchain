from app.models import User, Post, db
from flask import flash, redirect, Blueprint, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

delete_bp = Blueprint("delete", __name__)

@delete_bp.route("/delete/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def deletePost(post_id):
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalar()
    replies = db.session.execute(db.select(Post).where(Post.parent_id == post.id)).scalars().all()

    db.session.delete(post)

    for reply in replies:
        db.session.delete(reply)
    
    db.session.commit()

    return redirect(url_for("home.home"))