from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, URL


class CreateItemForm(FlaskForm):
    title = StringField("Create new Item", validators=[DataRequired()])
    submit = SubmitField("Submit Item")
