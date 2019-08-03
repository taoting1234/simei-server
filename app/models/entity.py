from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(String(100), primary_key=True)
    password = Column(String(100), nullable=False)
    nickname = Column(String(100), nullable=False)
    permission = Column(Integer, nullable=False)


class Fund(Base):
    __tablename__ = 'fund'

    id = Column(Integer, primary_key=True)
    money = Column(Integer, nullable=False)
    user_id = Column(String(100), ForeignKey('user.id'))
    user = relationship("app.models.entity.User")
    create_time = Column(DateTime, nullable=False)


class Application(Base):
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    money = Column(Integer, nullable=False)
    remark = Column(String(100), nullable=False)
    apply_user_id = Column(String(100), ForeignKey('user.id'))
    apply_user = relationship("app.models.entity.User", foreign_keys=[apply_user_id])
    apply_time = Column(DateTime, nullable=False)
    approval_user_id = Column(String(100), ForeignKey('user.id'))
    approval_user = relationship("app.models.entity.User", foreign_keys=[approval_user_id])
    approval_time = Column(DateTime)
    status = Column(Integer, nullable=False)
