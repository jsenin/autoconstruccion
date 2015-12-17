from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=32)])
    remember_me = BooleanField('Remember me')


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=32)])
    username = StringField('Name', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo(password)])
