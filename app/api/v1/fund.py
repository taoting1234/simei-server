from flask import jsonify
from flask_login import current_user, login_required
from app.libs.error_code import Forbidden, Success
from app.libs.red_print import RedPrint
from app.models.fund import add_fund, apply, get_application_list_by_user_id, approval, get_fund, \
    get_application_by_application_id, delete_application
from app.validators.forms import MoneyForm, ApplyForm, UserIdForm, ApprovalForm, ApplicationIdForm

api = RedPrint('fund')


@api.route("/add_fund", methods=['POST'])
@login_required
def add_fund_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    form = MoneyForm().validate_for_api()
    add_fund(current_user.id, form.money.data)
    return Success('Add fund successful')


@api.route("/apply", methods=['POST'])
@login_required
def apply_api():
    form = ApplyForm().validate_for_api()
    apply(current_user.id, form.name.data, form.money.data, form.remark.data)
    return Success('Apply successful')


@api.route("/delete_application", methods=['POST'])
@login_required
def delete_application_api():
    form = ApplicationIdForm().validate_for_api()
    application = get_application_by_application_id(form.application_id.data)
    if application.status == 1:
        raise Forbidden('Can\'t delete successful application')
    if not current_user.permission:
        if application.apply_user != current_user:
            raise Forbidden()
    delete_application(form.application_id.data)
    return Success('Delete application successful')


@api.route("/get_application_list", methods=['POST'])
@login_required
def get_apply_list_api():
    form = UserIdForm().validate_for_api()
    res = get_application_list_by_user_id(form.user_id.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/admin_get_application_list", methods=['POST'])
@login_required
def admin_get_apply_list_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    res = get_application_list_by_user_id()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route('/approval', methods=['POST'])
@login_required
def approval_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    form = ApprovalForm().validate_for_api()
    approval(form.application_id.data, current_user.id, form.status.data)
    return Success('Approval successful')


@api.route('/get_fund', methods=['POST'])
@login_required
def get_fund_api():
    res = get_fund()
    return jsonify({
        'code': 0,
        'data': res
    })
