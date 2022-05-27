from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    description = StringField(label='description', validators=[DataRequired()])
    img_url = URLField(label='img_url', validators=[DataRequired()])
    git_url = URLField(label='git_url', validators=[DataRequired()])
    identifiers = StringField(label='identifiers', validators=[DataRequired()])
    submit = SubmitField(label='Submit')