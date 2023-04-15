from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, String, TIMESTAMP, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class BookingTransport(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    startDate = Column(DateTime(timezone=True), default=datetime.utcnow,
                       nullable=True)  # Column(type_=TIMESTAMP(timezone=False), nullable=True)
    endDate = Column(DateTime(timezone=True), default=datetime.utcnow,
                     nullable=True)  # Column(type_=TIMESTAMP(timezone=False), nullable=True)
    allDay = Column(Boolean(), default=False)
    duration = Column(Integer, nullable=True, default=1)  # продолжительность в пути
    count_man = Column(Integer, nullable=True, default=1)  # количество человек
    description = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True)

    transport_id = Column(UUID(as_uuid=True),
                          ForeignKey('transport.id'),
                          nullable=True)
    transport = relationship('Transport',
                             back_populates='booking_transport',
                             lazy="immediate")

    subunit_id = Column(UUID(as_uuid=True),
                        ForeignKey('subunit.id'),
                        nullable=True)
    subunit = relationship('Subunit',
                           back_populates='booking_transport',
                           lazy="immediate")

    organization_id = Column(Integer,
                             ForeignKey('organization.id'),
                             nullable=True)
    organization = relationship('Organization',
                                back_populates='booking_transport',
                                lazy="immediate")
    creator_id = Column(UUID(as_uuid=True),
                        ForeignKey('user.id'),
                        nullable=True)
    creator = relationship('User',
                           back_populates='booking_transport',
                           lazy="immediate")


class Transport(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    image_url = Column(String, nullable=True)
    image_url_type = Column(String)
    title = Column(String(180), nullable=False)
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    booking_transport = relationship('BookingTransport',
                                     back_populates='transport',
                                     uselist=True, )
