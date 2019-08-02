from flask import jsonify
from flask_login import current_user, login_required, login_user, logout_user
from app.libs.error_code import AuthFailed, Success
from app.libs.red_print import RedPrint
from app.models.user import check_password, get_user_by_user_id
from app.validators.forms import LoginForm

api = RedPrint('user')


@api.route("/login", methods=['POST'])
def login_api():
    form = LoginForm().validate_for_api()
    user_id = form.user_id.data
    password = form.password.data
    user = get_user_by_user_id(user_id)
    if not user:
        raise AuthFailed('User id does not exist')
    if not check_password(user, password):
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
