from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import current_user
from ..models import User, Post, db

viewPost_bp = Blueprint("viewPost", __name__)

@viewPost_bp.route('/<username>/<int:post_id>')
def viewPost(username, post_id):
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalar()  
    parent_post = None

    # 404 error if db query returns null e.g. wrong url
    if post:
        post.replies = db.session.execute(db.select(Post).where(Post.parent_id == post.id).order_by(Post.created.desc())).scalars().all()
        author = db.session.execute(db.select(User).where(User.id == post.user_id)).scalar()
        post.author = author.username

        parent_id = post.parent_id
        
        if parent_id:
            parent_post = db.session.execute(db.select(Post).where(Post.id == parent_id)).scalar()
            author = db.session.execute(db.select(User).where(User.id == parent_post.user_id)).scalar()
            parent_post.author = author.username
    else:
        abort(404)

    from .forms.create.deletePostForm import DeletePostForm
    # DeletePostForm is a WTForms custom form
    deletePostForm = DeletePostForm()
    return render_template('view/viewPost.html', post=post, parent=parent_post, deletePostForm=deletePostForm)