from uuid import uuid4

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    last_name = Column(String(30), nullable=True)  # фамилия
    first_name = Column(String(30), nullable=True)  # имя
    patronymic = Column(String(30), nullable=True)  # отчество
    username = Column(String, index=True, nullable=False)
    avatar = Column(String, nullable=True)
    # email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization',
                                back_populates='users',
                                lazy="immediate")
    access_tors = relationship('Organization',
                               secondary="user_access_tor",
                               back_populates='access_users',
                               lazy="immediate")
    orders = relationship("Order",
                          # cascade="all,delete-orphan",
                          # back_populates="order_creator",
                          uselist=True,
                          lazy="immediate")
    booking_transport = relationship('BookingTransport',
                                     back_populates='creator',
                                     uselist=True, )
