from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo


class CreateUserForm(FlaskForm):
    firstname = StringField("Enter your First name")
    lastname = StringField("Enter your Last name")
    password = PasswordField("Enter your password", validators=[DataRequired(), InputRequired(),
                                                                EqualTo('password_confirm',
                                                                        message='Password must match')])
    password_confirm = PasswordField('Repeat Password')
    submit = SubmitField("Create a new Account")


class UpdateUserForm(FlaskForm):
    firstname = StringField("Enter your First name")
    lastname = StringField("Enter your Last name")
    submit = SubmitField("Update User")


class UpdateUserProfileForm(FlaskForm):
    firstname = StringField("Enter your First name")
    lastname = StringField("Enter your Last name")
    email = EmailField("Enter your new email address")
    submit = SubmitField("Update User")
