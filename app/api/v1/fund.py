from flask import jsonify
from flask_login import current_user, login_required

from app.libs.error_code import Forbidden, NotFound, Success
from app.libs.red_print import RedPrint
from app.models.fund import Fund
from app.validators.forms import MoneyForm, SearchForm

api = RedPrint("fund")


@api.route("", methods=["GET"])
@login_required
def search_fund_api():
    if current_user.permission == 0:
        raise Forbidden()
    form = SearchForm().validate_for_api().data_
    res = Fund.search(**form)
    return jsonify({"code": 0, "data": res})


@api.route("/current", methods=["GET"])
@login_required
def get_fund_current_api():
    if current_user.permission == 0:
        raise Forbidden()
    return jsonify({"code": 0, "data": Fund.get_current_money()})


@api.route("", methods=["POST"])
@login_required
def create_fund_api():
    if current_user.permission == 0:
        raise Forbidden()
    form = MoneyForm().validate_for_api().data_
    form["user_id"] = current_user.id
    Fund.create(**form)
    return Success("Create fund success")


@api.route("/<int:id_>", methods=["DELETE"])
@login_required
def delete_fund_api(id_):
    if current_user.permission == 0:
        raise Forbidden()
    fund = Fund.get_by_id(id_)
    if fund is None:
        raise NotFound("Fund not found")
    fund.delete()
    return Success("Delete fund success")
