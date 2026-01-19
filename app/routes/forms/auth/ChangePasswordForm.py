from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('Old password', validators=[DataRequired(), Length(min=8)])
    newPassword = PasswordField('New Password', validators=[DataRequired(), Length(min=8), EqualTo('new_password_confirm', message='Passwords must match')])
    new_password_confirm = PasswordField('Confirm new password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Change password')