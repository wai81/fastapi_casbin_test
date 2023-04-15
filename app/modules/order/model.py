from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Order(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_no = Column(String(16), nullable=True)    # номер заказа

    citi = Column(String(30), nullable=True)
    street = Column(String(30), nullable=True)
    house = Column(String(18), nullable=True)  # № дома
    building = Column(String(10), nullable=True)  # корпус
    apartment = Column(String(10), nullable=True)  # квартира

    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', back_populates='orders', lazy="immediate")
    order_creator_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    order_creator = relationship('User', back_populates='orders', lazy="immediate")

