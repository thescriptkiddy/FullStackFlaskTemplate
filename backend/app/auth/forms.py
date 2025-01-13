from flask_security import RegisterForm, LoginForm, ChangePasswordForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, InputRequired


class ExtendedRegisterForm(RegisterForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    submit = SubmitField()

# class ResetPasswordForm(ChangePasswordForm):
#    password = PasswordField("New Password", validators=[DataRequired()])
#    password2 = PasswordField(
#        "Repeat Password", validators=[DataRequired(), EqualTo("password")])
#    submit = SubmitField("Confirm Password Reset")
