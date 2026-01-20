from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Post, db

settings_bp = Blueprint("settings", __name__)

@settings_bp.route('/')
@login_required
def settings():
    from .forms.settings.deleteAccountForm import DeleteAccountForm
    # DeleteAccountForm is a WTForms custom form
    deleteAccountForm = DeleteAccountForm()
    return render_template('settings/settings.html', deleteAccountForm=deleteAccountForm, current_user=current_user)

@settings_bp.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    from .forms.auth.ChangePasswordForm import ChangePasswordForm
    # changePasswordForm is a WTForms custom form
    changePasswordForm = ChangePasswordForm()

    if changePasswordForm.validate_on_submit():
        current_user.set_password(changePasswordForm.newPassword.data) # hashes the password
        db.session.commit()
        flash('Password successfully updated!', "success")

        return redirect(url_for('home.home')) # redirects to other route

    return render_template('auth/changePassword.html', form=changePasswordForm, current_user=current_user)

@settings_bp.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    from .forms.settings.deleteAccountForm import DeleteAccountForm
    # DeleteAccountForm is a WTForms custom form
    deleteAccountForm = DeleteAccountForm()

    if deleteAccountForm.validate_on_submit():
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for('auth.login')) 

    return render_template('settings/settings.html', deleteAccountForm=deleteAccountForm, current_user=current_user)