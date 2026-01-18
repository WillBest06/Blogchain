from app.models import User, Post, db
from flask import flash, redirect, Blueprint, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

delete_bp = Blueprint("delete", __name__)

@delete_bp.route("/delete/post/<int:post_id>", methods=['GET', 'POST'])
def deletePost(post_id):
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalar()

    db.session.delete(post)
    db.session.commit()

    print("deleted")

    return redirect(url_for("home.home"))