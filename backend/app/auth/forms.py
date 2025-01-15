from flask_security import RegisterForm, LoginForm, ChangePasswordForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, InputRequired


class ExtendedRegisterForm(RegisterForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    submit = SubmitField()
