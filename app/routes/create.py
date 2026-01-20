from app.models import User, Post, db
from flask import flash, redirect, Blueprint, render_template, url_for, request
from flask_login import login_required, current_user

create_bp = Blueprint("create", __name__)

@create_bp.route('/post', methods=['GET', 'POST'])
@login_required
def create():
    parent_id = request.args.get("reply_to")
    parent_post = None
    if parent_id:
        parent_post = db.session.execute(db.select(Post).where(Post.id == parent_id)).scalar()
        author = db.session.execute(db.select(User).where(User.id == parent_post.user_id)).scalar()
        parent_post.author = author.username

    from .forms.create.PostForm import PostForm
    # PostForm is a WTForms custom form
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.body = form.body.data
        post.user_id = current_user.id
        post.parent_id = parent_id

        db.session.add(post)
        db.session.commit()
            
        if parent_id:
            flash("Reply sent!", "success")
        else:
            flash('Post created!', "success")

        author = db.session.execute(db.select(User).where(User.id == post.user_id)).scalar()
        post.author = author.username
        return redirect(url_for('viewPost.viewPost', username=post.author, post_id=post.id)) 

    return render_template('create/post.html', form=form, parent=parent_post)