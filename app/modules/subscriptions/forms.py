from flask_wtf import FlaskForm
from wtforms import SubmitField

class SubscribeForm(FlaskForm):
    submit = SubmitField('Subscribe')

class ChangePlanForm(FlaskForm):
    submit = SubmitField('Change Plan')