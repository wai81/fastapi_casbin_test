from enum import IntEnum
from typing import Dict, Any
from uuid import uuid4
from sqlalchemy import Column, String, Float, Integer, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

#
# class ReceiptStatus(IntEnum):
#     not_paid = 0
#     in_process = 1
#     paid = 2
#
#     @classmethod
#     def __modify_schema__(cls, schema: Dict[str, Any]):
#         schema["enum"] = [f"{choice.name} ({choice.value})" for choice in cls]
#         return schema


class Receipt(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    personal_account = Column(String(16), nullable=True)  # номер квитанции
    order = Column(String(21))                  # номер заказа
    last_name = Column(String(30))              # фамилия
    first_name = Column(String(30))             # имя
    patronymic = Column(String(30), nullable=True)  # отчество
    citi = Column(String(30), nullable=True)
    street = Column(String(30), nullable=True)
    house = Column(String(18), nullable=True)       # № дома
    building = Column(String(10), nullable=True)    # корпус
    apartment = Column(String(10), nullable=True)   # квартира
    debt = Column(Float)                            # сумма
    payment_state_duty = Column(Integer, default=0) # признак для оплаты госпошлины
    status = Column(Integer, default=0) # статус квитанции 0-Не оплачена 1-В процесе оплаты 2-Оплачена
    tor_id = Column(Integer, ForeignKey('organization.id'))
    tor = relationship('Organization', back_populates='receipts', lazy="immediate")

