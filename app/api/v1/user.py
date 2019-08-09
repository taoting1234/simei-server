from flask import jsonify
from flask_login import current_user, login_required, login_user, logout_user
from app.libs.error_code import AuthFailed, Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.user import check_password, get_user_by_user_id, add_user, modify_password, get_user_list, modify_user
from app.validators.forms import LoginForm, AddUserForm, ModifyPasswordForm, UserInfoForm

api = RedPrint('user')


@api.route("/login", methods=['POST'])
def login_api():
    form = LoginForm().validate_for_api()
    user_id = form.user_id.data
    password = form.password.data
    user = get_user_by_user_id(user_id)
    if not user:
        raise AuthFailed('User id does not exist')
    if not check_password(password, user.password):
        raise AuthFailed('Wrong username or password')
    login_user(user, remember=True)
    return Success('Login successful')


@api.route("/logout", methods=['POST'])
def logout_api():
    logout_user()
    return Success('Logout successful')


@api.route("/get_login_user_info", methods=['POST'])
@login_required
def get_login_user_info_api():
    return jsonify({
        'code': 0,
        'data': {
            'user_id': current_user.id,
            'nickname': current_user.nickname,
            'permission': current_user.permission
        }
    })


@api.route("/add_user", methods=['POST'])
def add_user_api():
    form = AddUserForm().validate_for_api()
    add_user(form.user_id.data, form.nickname.data)
    return Success('Add user successful')


@api.route("/modify_password", methods=['POST'])
@login_required
def modify_password_api():
    form = ModifyPasswordForm().validate_for_api()
    modify_password(form.user_id.data, form.new_password.data)
    return Success('Modify successful')


@api.route("/get_user_list", methods=['POST'])
@login_required
def get_user_list_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    res = get_user_list()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/modify_user_info", methods=['POST'])
@login_required
def modify_user_info_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    form = UserInfoForm().validate_for_api()
    modify_user(form.user_id.data, form.nickname.data, form.permission.data)
    return Success('Modify successful')
