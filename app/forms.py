from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchSpotifyform(FlaskForm):
    query = StringField('Input', validators=[DataRequired()])
    submit = SubmitField('Search')