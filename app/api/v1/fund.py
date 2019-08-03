from flask import jsonify
from flask_login import current_user, login_required
from app.libs.error_code import Forbidden, Success
from app.libs.red_print import RedPrint
from app.models.fund import add_fund, apply, get_application_list_by_user_id, approval, get_fund
from app.validators.forms import MoneyForm, ApplyForm, UserIdForm, ApprovalForm

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
