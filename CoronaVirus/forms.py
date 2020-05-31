from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired


class DateForm(FlaskForm):
    date = DateField('date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Search')
