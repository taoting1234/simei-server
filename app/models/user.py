from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    fields = ['id', 'nickname', 'permission']

    id = Column(String(100), primary_key=True)
    password = Column(String(100), nullable=False)
    nickname = Column(String(100), nullable=False)
    permission = Column(Integer, default=0)

    def check_password(self, password):
        return self.password == password

    @staticmethod
    @login_manager.user_loader
    def load_user(id_):
        return User.get_by_id(id_)

    @staticmethod
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return AuthFailed()
