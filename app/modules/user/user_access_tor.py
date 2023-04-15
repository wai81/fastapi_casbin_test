from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import Column
from sqlalchemy.orm import relationship, backref
from app.db.base_class import Base

class User_access_tor(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    # user = relationship('User',
    #                     backref=backref("user_access_tor", cascade="all, delete, delete-orphan"),)
    #                     back_populates='organizations')

    organization_id = Column(Integer, ForeignKey('organization.id'), primary_key=True, nullable=False, index=True)
    # organization = relationship('Organization',
    #                             backref=backref("user_access_tor", cascade="all, delete, delete-orphan"),)
    #                              back_populates='users')
