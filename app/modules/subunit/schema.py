from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from app.modules.organization.schema import OrganizationInDB


class SubunitBase(BaseModel):
    id: UUID4
    name: Optional[str] = None
    title: Optional[str] = None
    color_subunit: Optional[str] = None


class SubunitCreate(BaseModel):
    name: str
    title: Optional[str] = None
    organization_id: int
    color_subunit: Optional[str] = None
    is_active: Optional[bool] = True


class SubunitUpdate(SubunitCreate):
    pass


class SubunitDetail(SubunitBase):
    title: str
    is_active: bool
    created_at: datetime


class Subunit(SubunitDetail):
    pass

    class Config:
        orm_mode = True  # помогает связать модель со схемой


class SubunitInDB(BaseModel):
    id: UUID4
    name: str
    title: str
    is_active: bool
    color_subunit: Optional[str] = None
    organization: OrganizationInDB
    created_at: datetime

    class Config:
        orm_mode = True  # помогает связать модель со схемой
