import datetime

from flask import jsonify
from flask_login import current_user, login_required

from app.libs.error_code import Forbidden, NotFound, Success
from app.libs.red_print import RedPrint
from app.models.application import Application
from app.validators.forms import (
    ApplicationForm,
    CreateApplicationForm,
    SearchApplicationForm,
)

api = RedPrint("application")


@api.route("", methods=["GET"])
@login_required
def search_application_api():
    form = SearchApplicationForm().validate_for_api().data_
    if form["apply_user_id"] is None and current_user.permission == 0:
        raise Forbidden()
    res = Application.search(**form)
    return jsonify({"code": 0, "data": res})


@api.route("", methods=["POST"])
@login_required
def create_application_api():
    form = CreateApplicationForm().validate_for_api().data_
    form["apply_user_id"] = current_user.id
    form["apply_time"] = datetime.datetime.now()
    Application.create(**form)
    return Success("Create application success")


@api.route("/<int:id_>", methods=["PUT"])
@login_required
def modify_application_api(id_):
    if current_user.permission == 0:
        raise Forbidden()
    application = Application.get_by_id(id_)
    if application is None:
        raise NotFound("Application not found")
    form = ApplicationForm().validate_for_api().data_
    if form["status"] == 1:
        form["approval_user_id"] = current_user.id
        form["approval_time"] = datetime.datetime.now()
    application.modify(**form)
    return Success("Modify application success")


@api.route("/<int:id_>", methods=["DELETE"])
@login_required
def delete_application_api(id_):
    application = Application.get_by_id(id_)
    if application is None:
        raise NotFound("Application not found")
    if application.apply_user_id != current_user.id and current_user.permission == 0:
        raise Forbidden()
    application.delete()
    return Success("Delete application success")
