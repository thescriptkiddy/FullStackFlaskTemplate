from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, URL
from wtforms.widgets import ListWidget, CheckboxInput


class CreateMenuForm(FlaskForm):
    name = StringField()
    links = SelectMultipleField("All links", validators=[DataRequired()], choices=[])
    submit = SubmitField("Save menu")

    def __init__(self, all_links=None, *args, **kwargs):
        super(CreateMenuForm, self).__init__(*args, **kwargs)
        if all_links:
            self.links.choices = [(link, link) for link in all_links]


class UpdateMenuForm(FlaskForm):
    name = StringField('Menu Name', validators=[DataRequired()])
    links = SelectMultipleField('Links', coerce=str)
    submit = SubmitField('Update Menu')

    def __init__(self, *args, **kwargs):
        super(UpdateMenuForm, self).__init__(*args, **kwargs)
        self.all_links = kwargs.pop('all_links', [])
        self.links.choices = [(link.id, link.url) for link in self.all_links]


class UpdateLinkForm(FlaskForm):
    name = StringField("Link Name", validators=[DataRequired()])
    submit = SubmitField("Update Link")
