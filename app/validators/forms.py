from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.validators.base import BaseForm as Form


class SearchForm(Form):
    page = IntegerField()
    page_size = IntegerField()

    def validate_page(self, value):
        if self.page.data:
            self.page.data = int(self.page.data)
            if self.page.data <= 0:
                raise ValidationError("Page must >= 1")

    def validate_page_size(self, value):
        if self.page_size.data:
            self.page_size.data = int(self.page_size.data)
            if self.page_size.data > 100:
                raise ValidationError("Page size must <= 100")


class LoginForm(Form):
    id = StringField(validators=[DataRequired(message="User id cannot be empty")])
    password = StringField(
        validators=[DataRequired(message="Password cannot be empty")]
    )


class MoneyForm(Form):
    money = IntegerField(validators=[DataRequired(message="Money cannot be empty")])

    def validate_money(self, value):
        if self.money.data <= 0:
            raise ValidationError("Money must be > 0")


class CreateApplicationForm(MoneyForm):
    name = StringField(validators=[DataRequired(message="Name cannot be empty")])
    remark = StringField(validators=[DataRequired(message="Remark cannot be empty")])


class ApplicationForm(Form):
    status = IntegerField()

    def validate_status(self, value):
        if self.status.data != 0 and self.status.data != 1:
            raise ValidationError("Status must be 0 or 1")


class SearchApplicationForm(SearchForm):
    apply_user_id = StringField()


class CreateUserForm(Form):
    id = StringField(validators=[DataRequired(message="User id cannot be empty")])
    nickname = StringField(
        validators=[DataRequired(message="Nickname cannot be empty")]
    )


class UserForm(Form):
    nickname = StringField()
    old_password = StringField()
    password = StringField()
    permission = IntegerField()


class SearchCustomerForm(SearchForm):
    name = StringField()
    phone = StringField()
    address = StringField()
    principal_user_id = StringField()
    status = IntegerField()


class CreateCustomerForm(Form):
    name = StringField(
        validators=[DataRequired(message="Customer name cannot be empty")]
    )
    phone = StringField()
    address = StringField()
    principal_user_id = StringField()


class ModifyCustomerForm(Form):
    name = StringField()
    phone = StringField()
    address = StringField()
    principal_user_id = StringField()
    status = IntegerField()
