from uuid import uuid4

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Subunit(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(60), index=True, nullable=False)
    title = Column(String(160), index=True, nullable=False)
    color_subunit = Column(String(180), nullable=True)
    is_active = Column(Boolean, default=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', back_populates='subunits', lazy="immediate")
    booking_transport = relationship('BookingTransport', back_populates='subunit', uselist=True,)
