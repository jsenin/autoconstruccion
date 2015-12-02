from flask_wtf import Form
from wtforms import StringField, PasswordField


class LoginForm(Form):
    user_mail = StringField('Email')
    password = PasswordField('Password')
