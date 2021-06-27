from flask import Blueprint

from app.api.v1 import (
    application,
    collection_money,
    customer,
    file,
    fund,
    session,
    user,
)


def create_blueprint_v1():
    bp_v1 = Blueprint("v1", __name__)

    session.api.register(bp_v1)
    user.api.register(bp_v1)
    fund.api.register(bp_v1)
    application.api.register(bp_v1)
    customer.api.register(bp_v1)
    file.api.register(bp_v1)
    collection_money.api.register(bp_v1)
    return bp_v1
