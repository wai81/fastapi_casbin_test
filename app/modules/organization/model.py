from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organization(Base):
    id = Column(Integer, primary_key=True, index=True)
    # tor_id = Column(Integer, unique=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    fullname = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True)

    receipts = relationship('Receipt',
                            back_populates='tor', uselist=True, )
    orders = relationship('Order',  # cascade='all,delete-orphan',
                          back_populates='organization', uselist=True, )
    users = relationship('User',
                         # cascade='all,delete-orphan',
                         back_populates='organization', uselist=True, )
    access_users = relationship('User',
                                secondary="user_access_tor",
                                back_populates="access_tors", uselist=True)

    subunits = relationship('Subunit',
                            # cascade='all,delete-orphan',
                            back_populates='organization', uselist=True, )

    booking_transport = relationship('BookingTransport',
                                     # cascade='all,delete-orphan',
                                     back_populates='organization', uselist=True, )
