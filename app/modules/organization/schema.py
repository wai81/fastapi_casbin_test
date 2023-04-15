from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class OrganizationBase(BaseModel):
    id: int
    title: Optional[str] = None
    fullname: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    title: str


class OrganizationUpdate(OrganizationCreate):
    fullname: Optional[str] = None
    is_active: Optional[bool] = True


class OrganizationDetail(OrganizationBase):
    created_at: datetime
    is_active: bool


class Organization(OrganizationDetail):
    pass

    class Config:
        orm_mode = True  # помогает связать модель со схемой


class OrganizationInDB(BaseModel):
    id: int
    title: str
    fullname: str
    is_active: bool

    class Config:
        orm_mode = True  # помогает связать модель со схемой


# class OrganizationSubunits(OrganizationDetail):
#     subunits: Optional[List[Subunit]] = None
#
#
# from app.schema.subunit import Subunit
# OrganizationSubunits.update_forward_refs()
