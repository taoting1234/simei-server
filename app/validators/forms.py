from wtforms import StringField
from wtforms.validators import DataRequired

from app.validators.base import BaseForm as Form


class LoginForm(Form):
    user_id = StringField(validators=[DataRequired(message='User id cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])
