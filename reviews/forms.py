from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField

class ReviewSearchForm(FlaskForm):
	keywords = StringField('Review Keywords', validators=[validators.DataRequired()])
	scoreDirection = SelectField('Score direction', choices=[('>=', '>='),('<=', '<=')])
	scoreThreshold = SelectField('Score threshold', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
	submit = SubmitField('Submit')
