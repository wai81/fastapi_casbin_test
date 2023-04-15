from datetime import datetime
from typing import Optional
from app.modules.user.schema import UserInDB
from pydantic import BaseModel
from pydantic.types import UUID4

from app.modules.organization.schema import OrganizationInDB
from app.modules.subunit.schema import SubunitInDB

# ---Transport---
class TransportBase(BaseModel):
    id: UUID4
    title: Optional[str] = None
    details: Optional[str] = None
    is_active: Optional[bool] = True
    image_url: Optional[str] = None
    image_url_type: Optional[str] = None


class TransportCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    image_url: Optional[str] = None
    image_url_type: Optional[str] = None


class TransportUpdate(TransportCreate):
    pass


class TransportDetail(TransportBase):
    id: UUID4
    created_at: datetime


class Transport(TransportDetail):
    pass

    class Config:
        orm_mode = True  # помогает связать модель со схемой


class TransportInDB(BaseModel):
    id: UUID4
    title: str
    image_url: Optional[str] = None
    image_url_type: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: datetime

    class Config:
        orm_mode = True  # помогает связать модель со схемой


# ---BookingTransportBase---
class BookingTransportBase(BaseModel):
    title: Optional[str] = None
    startDate: Optional[datetime] = None
    duration: Optional[int]
    endDate: Optional[datetime] = None
    allDay: bool = False
    description: Optional[str] = None
    count_man: Optional[int]
    creator_id: Optional[UUID4] = None



class BookingTransportCreate(BookingTransportBase):
    startDate: datetime
    duration: Optional[int]
    endDate: datetime
    is_active: Optional[bool] = True
    subunit_id: UUID4
    organization_id: int
    transport_id: Optional[UUID4] = None
    count_man: Optional[int]
    

class BookingTransportUpdate(BookingTransportCreate):
    transport_id: Optional[UUID4] = None


class BookingTransportDetail(BookingTransportBase):
    id: UUID4
    subunit: SubunitInDB
    created_at: datetime
    is_active: Optional[bool] = True
   


class BookingTransport(BookingTransportDetail):
    pass

    class Config:
        orm_mode = True  # помогает связать модель со схемой


class BookingTransportInDB(BaseModel):
    id: UUID4
    title: str
    startDate: datetime
    duration: int
    endDate: datetime
    allDay: bool
    count_man: int
    description: Optional[str] = None
    subunit: Optional[SubunitInDB] = None
    transport: Optional[TransportInDB] = None
    organization: Optional[OrganizationInDB] = None
    creator: Optional[UserInDB] = None
    created_at: datetime
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True  # помогает связать модель со схемой
