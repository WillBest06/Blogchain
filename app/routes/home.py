from flask import Blueprint, render_template
from flask_login import current_user
from ..models import User, Post, db

home_bp = Blueprint("home", __name__)

@home_bp.route('/')
def home():
    # query only gets posts without a parent
    stories = db.session.execute(db.select(Post).where(Post.parent_id == None).order_by(Post.created.desc())).scalars().all()
    
    for story in stories:
        author = db.session.execute(db.select(User).where(User.id == story.user_id)).scalar()
        story.author = author.username
    return render_template('home.html', current_user=current_user, stories=stories)