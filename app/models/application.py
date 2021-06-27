from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.user import User


class Application(Base):
    __tablename__ = "application"

    fields = [
        "id",
        "name",
        "money",
        "remark",
        "apply_user_id",
        "apply_user",
        "apply_time",
        "approval_user_id",
        "approval_user",
        "approval_time",
        "status",
    ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    money = Column(Integer, nullable=False)
    remark = Column(String(100), nullable=False)
    apply_user_id = Column(String(100), ForeignKey(User.id))
    apply_user = relationship(User, foreign_keys=[apply_user_id])
    apply_time = Column(DateTime, nullable=False)
    approval_user_id = Column(String(100), ForeignKey(User.id))
    approval_user = relationship(User, foreign_keys=[approval_user_id])
    approval_time = Column(DateTime)
    status = Column(Integer, default=0)
