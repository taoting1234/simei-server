from flask_login import current_user
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError

from app.libs.error_code import Forbidden
from app.models.fund import get_application_by_application_id
from app.models.user import get_user_by_user_id
from app.validators.base import BaseForm as Form


class LoginForm(Form):
    user_id = StringField(validators=[DataRequired(message='User id cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class MoneyForm(Form):
    money = IntegerField(validators=[DataRequired(message='Money cannot be empty')])

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
            raise ValidationError('User does not exist')


class ApprovalForm(Form):
    application_id = IntegerField(validators=[DataRequired(message='Application id cannot be empty')])
    status = IntegerField(validators=[DataRequired(message='Status cannot be empty')])

    def validate_application_id(self, value):
        if not get_application_by_application_id(self.application_id.data):
            raise ValidationError('Application does not exist')

    def validate_status(self, value):
        if self.status.data != 1 and self.status.data != 2:
            raise ValidationError('Status must be 1 or 2')
