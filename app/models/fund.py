import datetime

from sqlalchemy import desc, func

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


def get_application_list_by_user_id(user_id=None):
    if user_id:
        r = Application.query.filter_by(apply_user_id=user_id).order_by(desc(Application.id)).all()
    else:
        r = Application.query.order_by(desc(Application.id)).all()

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
    } for i in r]


def get_application_by_application_id(application_id):
    return Application.query.get(application_id)


def approval(application_id, user_id, status):
    r = get_application_by_application_id(application_id)
    with db.auto_commit():
        r.approval_user_id = user_id
        r.approval_time = datetime.datetime.now()
        r.status = status


def get_fund():
    r1 = db.session.query(func.sum(Fund.money)).first()
    if r1:
        r1 = int(r1[0])
    else:
        r1 = 0
    r2 = db.session.query(func.sum(Application.money)).filter(
        Application.status == 1
    ).first()
    if r2:
        r2 = int(r2[0])
    else:
        r2 = 0

    return r1 - r2


def delete_application(application_id):
    Application.query.filter_by(id=application_id).delete()
