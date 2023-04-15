from datetime import datetime
from typing import Sequence, Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from app.modules.organization.schema import OrganizationInDB
from app.modules.user.schema import UserProfile


class OrderBase(BaseModel):
    citi: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    building: Optional[str] = None
    apartment: Optional[str] = None


class OrderCreate(OrderBase):
    organization_id: int
    order_creator_id: UUID4


class OrderUpdate(OrderBase):
    pass


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: UUID4
    created_at: datetime
    order_no: str
    organization_id: int
    order_creator_id: UUID4

    class Config:
        orm_mode = True


class OrderInDB(BaseModel):
    id: UUID4
    created_at: datetime
    order_no: str
    citi: str
    street: str
    house: str
    building: str
    apartment: str
    organization: OrganizationInDB
    order_creator: UserProfile

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDB):
    pass


# Properties properties stored in DB
class OrdersInDB(BaseModel):
    items: list[OrderInDB]
    total: int


class OrderSearchResults(BaseModel):
    results: Sequence[Order]

