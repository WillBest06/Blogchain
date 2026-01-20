from app.models import User, db
from flask import flash, redirect, Blueprint, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))

    from .forms.auth.LoginForm import LoginForm
    # LoginForm is a WTForms custom form
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar() # scalar returns actual user object

        if user and user.check_password(form.password.data):
            login_user(user)

            flash('Logged in successfully.', "success")

            next = request.args.get('next')
            print(next)

            return redirect(next or url_for('home.home'))
        else:
            flash('Invalid username or password.', "danger")
    return render_template('auth/login.html', form=form)

@auth_bp.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()

    return redirect(url_for("home.home"))

@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def signup():

    from .forms.auth.SignupForm import SignupForm
    # SignupForm is a WTForms custom form
    form = SignupForm()
    if form.validate_on_submit():
        userAlreadyExists = db.session.execute(db.select(User).filter_by(username=form.username.data)).first()

        if userAlreadyExists:
            flash('Username taken.', "danger")
        else:
            user = User()
            user.username = form.username.data
            user.set_password(form.password.data) # hashes the password

            db.session.add(user)
            db.session.commit()
            flash('Account successfully created. Please login.', "success")
            return redirect(url_for('auth.login')) # redirects to other route

    return render_template('auth/signup.html', form=form)