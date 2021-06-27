from flask import jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.libs.error_code import AuthFailed, Success
from app.libs.red_print import RedPrint
from app.models.user import User
from app.validators.forms import LoginForm

api = RedPrint('session')


@api.route("", methods=['GET'])
@login_required
def get_session_api():
    return jsonify({
        'code': 0,
        'data': current_user
    })


@api.route("", methods=['POST'])
def create_session_api():
    form = LoginForm().validate_for_api()
    user_id = form.id.data
    password = form.password.data
    user = User.get_by_id(user_id)
    if not user:
        raise AuthFailed('User id does not exist')
    if not user.check_password(password):
        raise AuthFailed('Wrong username or password')
    login_user(user, remember=True)
    return Success('Login successful')


@api.route("", methods=['DELETE'])
@login_required
def delete_session_api():
    logout_user()
    return Success('Logout successful')
