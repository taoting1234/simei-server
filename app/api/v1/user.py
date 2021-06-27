from flask import jsonify
from flask_login import current_user, login_required

from app.libs.error_code import Forbidden, NotFound, ParameterException, Success
from app.libs.red_print import RedPrint
from app.models.user import User
from app.validators.forms import CreateUserForm, SearchForm, UserForm

api = RedPrint("user")


@api.route("", methods=["GET"])
@login_required
def search_user_api():
    if current_user.permission == 0:
        raise Forbidden()
    form = SearchForm().validate_for_api().data_
    res = User.search(**form)
    return jsonify({"code": 0, "data": res})


@api.route("", methods=["POST"])
@login_required
def create_user_api():
    if current_user.permission == 0:
        raise Forbidden()
    form = CreateUserForm().validate_for_api().data_
    if User.get_by_id(form["id"]):
        raise ParameterException("User already exist")
    form["password"] = form["id"]
    User.create(**form)
    return Success("Create user successful")


@api.route("/<string:id_>", methods=["PUT"])
@login_required
def modify_user_api(id_):
    user = User.get_by_id(id_)
    if user is None:
        raise NotFound("User not found")
    if current_user.id != user.id and current_user.permission == 0:
        raise Forbidden()
    form = UserForm().validate_for_api().data_
    if (
        current_user.permission == 0
        and form["password"]
        and user.check_password(form["old_password"]) is False
    ):
        raise ParameterException("Old password wrong")
    if form["permission"] and current_user.permission == 0:
        raise Forbidden()
    user.modify(**form)
    return Success("Modify user successful")
