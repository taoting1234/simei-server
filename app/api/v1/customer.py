from flask import jsonify
from flask_login import current_user, login_required

from app.libs.error_code import (Forbidden, NotFound, ParameterException,
                                 Success)
from app.libs.red_print import RedPrint
from app.models.customer import Customer
from app.models.user import User
from app.validators.forms import (CreateCustomerForm, ModifyCustomerForm,
                                  SearchCustomerForm)

api = RedPrint('customer')


@api.route("", methods=['GET'])
@login_required
def search_customer_api():
    form = SearchCustomerForm().validate_for_api().data_
    res = Customer.search(**form)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("", methods=['POST'])
@login_required
def create_customer_api():
    form = CreateCustomerForm().validate_for_api().data_
    if User.get_by_id(form['principal_user_id']) is None:
        raise ParameterException('Principal user does not exist')
    Customer.create(**form)
    return Success('Create customer success')


@api.route("/<int:id_>", methods=['PUT'])
@login_required
def modify_customer_api(id_):
    customer = Customer.get_by_id(id_)
    if customer is None:
        raise NotFound('Customer not found')
    form = ModifyCustomerForm().validate_for_api().data_
    if form['principal_user_id']:
        if User.get_by_id(form['principal_user_id']) is None:
            raise ParameterException('Principal user does not exist')
    if form['name'] and current_user.permission == 0:
        raise Forbidden()
    customer.modify(**form)
    return Success('Modify customer success')


@api.route("/<int:id_>", methods=['DELETE'])
@login_required
def delete_customer_api(id_):
    if current_user.permission == 0:
        raise Forbidden()
    customer = Customer.get_by_id(id_)
    if customer is None:
        raise NotFound('Customer not found')
    customer.delete()
    return Success('Delete customer success')
