from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Create account')