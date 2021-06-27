from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.user import User


class Customer(Base):
    __tablename__ = 'customer'

    fields = ['id', 'name', 'phone', 'address', 'principal_user_id', 'principal_user', 'status', 'create_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(String(100))
    principal_user_id = Column(String(100), ForeignKey(User.id))
    principal_user = relationship(User, foreign_keys=[principal_user_id])
    status = Column(Integer, default=0)
    create_time = Column(DateTime, nullable=False)
