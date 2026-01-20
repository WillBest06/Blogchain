from flask import Blueprint, render_template
from ..models import User, Post, db


profile_bp = Blueprint("profile", __name__)

@profile_bp.route('/<username>')
def profile(username):
    from .forms.create.deletePostForm import DeletePostForm
    # DeletePostForm is a WTForms custom form
    deletePostForm = DeletePostForm()

    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    posts = db.session.execute(db.select(Post).where(Post.user_id == user.id).order_by(Post.created.desc())).scalars().all()
    
    for post in posts:
        author = db.session.execute(db.select(User).where(User.id == post.user_id)).scalar()
        post.author = author.username
        post.replies = db.session.execute(db.select(Post).where(Post.parent_id == post.id).order_by(Post.created.desc())).scalars().all()

        for reply in post.replies:
            author = db.session.execute(db.select(User).where(User.id == reply.user_id)).scalar()
            reply.author = author.username
    return render_template('view/profile.html', user=user, posts=posts, deletePostForm=deletePostForm)