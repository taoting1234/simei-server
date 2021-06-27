from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.models.user import User


class Fund(Base):
    __tablename__ = "fund"

    fields = ["id", "money", "user_id", "user", "create_time"]

    id = Column(Integer, primary_key=True, autoincrement=True)
    money = Column(Integer, nullable=False)
    user_id = Column(String(100), ForeignKey(User.id))
    user = relationship(User, foreign_keys=[user_id])
    create_time = Column(DateTime, nullable=False)

    @staticmethod
    def get_current_money():
        from app.models.application import Application

        all_money = int(db.session.query(func.sum(Fund.money)).first()[0])
        used_money = int(
            db.session.query(func.sum(Application.money))
            .filter(Application.status == 1)
            .first()[0]
        )
        return all_money - used_money
