from flask import Blueprint, render_template
from flask_login import current_user
from ..models import User, Post, db

home_bp = Blueprint("home", __name__)

@home_bp.route('/')
def home():
    from .forms.create.deletePostForm import DeletePostForm
    # DeletePostForm is a WTForms custom form
    deletePostForm = DeletePostForm()

    # query only gets posts without a parent
    posts = db.session.execute(db.select(Post).where(Post.parent_id == None).order_by(Post.created.desc())).scalars().all()
    
    for post in posts:
        author = db.session.execute(db.select(User).where(User.id == post.user_id)).scalar()
        post.author = author.username
        post.replies = db.session.execute(db.select(Post).where(Post.parent_id == post.id).order_by(Post.created.desc())).scalars().all()

        for reply in post.replies:
            author = db.session.execute(db.select(User).where(User.id == reply.user_id)).scalar()
            reply.author = author.username
    return render_template('home.html', current_user=current_user, posts=posts, deletePostForm=deletePostForm)