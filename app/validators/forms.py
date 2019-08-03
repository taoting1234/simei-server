from flask_login import current_user
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError

from app.libs.error_code import Forbidden
from app.models.user import get_user_by_user_id
from app.validators.base import BaseForm as Form


class LoginForm(Form):
    user_id = StringField(validators=[DataRequired(message='User id cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class MoneyForm(Form):
    money = IntegerField(validators=[DataRequired(message='money cannot be empty')])

    def validate_money(self, value):
        if self.money.data <= 0:
            raise ValidationError('Money must be > 0')


class ApplyForm(MoneyForm):
    name = StringField(validators=[DataRequired(message='Name cannot be empty')])
    remark = StringField(validators=[DataRequired(message='Remark cannot be empty')])


class UserIdForm(Form):
    user_id = StringField(validators=[DataRequired(message='User id cannot be empty')])

    def validate_username(self, value):
        if not current_user.permission and current_user.id != self.user_id.data:
            raise Forbidden()
        if not get_user_by_user_id(self.username.data):
            raise ValidationError('User id does not exist')
