from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import db
from app.models.entity import User


def check_password(user, password):
    return user.password == password


def modify_password(user_id, password):
    user = get_user_by_user_id(user_id)
    with db.auto_commit():
        user.password = password


def modify_user(user_id, nickname):
    user = get_user_by_user_id(user_id)
    with db.auto_commit():
        user.nickname = nickname


@login_manager.user_loader
def get_user_by_user_id(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthFailed()


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_user_by_username('31702411')
        print(r)
        print(r.oj_username[0].oj_username)
