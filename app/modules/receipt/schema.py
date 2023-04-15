from datetime import datetime
from enum import IntEnum
from typing import Optional
from pydantic.types import UUID4
from pydantic import BaseModel

from app.modules.organization.schema import OrganizationInDB


class ReceiptStatus(IntEnum):
    not_paid = 0
    in_process = 1
    paid = 2


class ReceiptBase(BaseModel):
    order: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    citi: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    building: Optional[str] = None
    apartment: Optional[str] = None
    debt: float
    payment_state_duty: int = 0


class ReceiptCreate(ReceiptBase):
    tor_id: int
    last_name: str
    first_name: str
    order: str
    status: ReceiptStatus = ReceiptStatus.not_paid


class ReceiptUpdate(ReceiptBase):
    last_name: str
    first_name: str
    status: ReceiptStatus


class ReceiptDetail(ReceiptBase):
    created_at: datetime = None
    tor_id:  int = None
    id: UUID4
    personal_account: str
    order: str
    payment_state_duty: int
    status: ReceiptStatus


class ReceiptCreateInDB(ReceiptBase):
    tor_id: int = None
    personal_account: str
    order: str
    status: ReceiptStatus


# default schema to return on a response
class Receipt(ReceiptDetail):
    pass

    class Config:
        orm_mode = True  # помогает связать модель со схемой


class ReceiptInDB(BaseModel):
    id: UUID4
    created_at: datetime
    tor: OrganizationInDB
    personal_account: str
    order: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    citi: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    building: Optional[str] = None
    apartment: Optional[str] = None
    debt: float
    payment_state_duty: int
    status: ReceiptStatus

    class Config:
        orm_mode = True  # помогает связать модель со схемой

# Properties properties stored in DB
class ReceiptsInDB(BaseModel):
    receipts: list[ReceiptInDB]
    receiptsCount: int

class ReceiptUpdateStatus(BaseModel):
    status: ReceiptStatus

