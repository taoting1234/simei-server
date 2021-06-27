from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.customer import Customer
from app.models.user import User


class CollectionMoney(Base):
    __tablename__ = 'collection_money'

    fields = ['id', 'user_id', 'user', 'name', 'money', 'remark', 'customer_id', 'customer', 'create_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), ForeignKey(User.id))
    user = relationship(User, foreign_keys=[user_id])
    name = Column(String(100), nullable=False)
    money = Column(Integer, nullable=False)
    remark = Column(String(100), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id))
    customer = relationship(Customer, foreign_keys=[customer_id])
    create_time = Column(DateTime, nullable=False)
