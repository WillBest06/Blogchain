from app.models import Post, db
from flask import flash, redirect, Blueprint, render_template, url_for
from flask_login import login_required, current_user

create_bp = Blueprint("create", __name__)

@create_bp.route('/newpost', methods=['GET', 'POST'])
@login_required
def create():
    from .forms.create.PostForm import PostForm
    # PostForm is a WTForms custom form
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.body = form.body.data
        post.user_id = current_user.id
        post.parent_id = None

        db.session.add(post)
        db.session.commit()
        flash('Post created!')
        return redirect(url_for('home.home')) 

    return render_template('create/createPost.html', form=form)