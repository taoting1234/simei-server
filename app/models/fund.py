import datetime

from app.models.base import db
from app.models.entity import Fund, Application


def add_fund(user_id, money):
    with db.auto_commit():
        r = Fund()
        r.user_id = user_id
        r.money = money
        r.create_time = datetime.datetime.now()
        db.session.add(r)


def apply(user_id, name, money, remark):
    with db.auto_commit():
        r = Application()
        r.apply_user_id = user_id
        r.name = name
        r.money = money
        r.remark = remark
        r.apply_time = datetime.datetime.now()
        r.status = 0
        db.session.add(r)


def get_apply_list_by_user_id(user_id):
    return [{
        'id': i.id,
        'name': i.name,
        'money': i.money,
        'remark': i.remark,
        'apply_user_id': i.apply_user_id,
        'apply_user_nickname': i.apply_user.nickname,
        'apply_time': i.apply_time,
        'approval_user_id': i.approval_user_id,
        'approval_user_nickname': i.approval_user.nickname if i.approval_user else None,
        'approval_time': i.approval_time,
        'status': i.status
    } for i in Application.query.filter_by(apply_user_id=user_id).all()]
