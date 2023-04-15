from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator
from pydantic.types import UUID4

from app.modules.organization.schema import OrganizationInDB


class UserBase(BaseModel):
    username: str
    last_name: Optional[str]
    first_name: Optional[str]
    patronymic: Optional[str]
    # email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    is_superuser: bool = False
    is_active: Optional[bool] = None

    @validator('username', pre=True)
    def blank_string(value, field):
        if value == "":
            return None
        return value


# Properties to receive via API on creation
class RegisterUser(BaseModel):
    username: str
    last_name: Optional[str]
    first_name: Optional[str]
    patronymic: Optional[str]
    password: str

    # @validator('username', pre=True)
    # def blank_string(value, field):
    #     if value == "":
    #         raise ValueError('does not empty')
    #     return value


class UserCreate(RegisterUser):
    avatar: Optional[str] = None
    organization_id: int


# Properties to receive via API on update
class UserUpdate(UserBase):
    organization_id: int
    password: Optional[str]


# Additional properties stored in DB but not returned by API
class UserInDB(UserBase):
    id: UUID4
    organization: Optional[OrganizationInDB] = None
    access_tors: Optional[List[OrganizationInDB]] = None
    created_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDB):
    access_token: str


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserCreateDB(BaseModel):
    user: UserCreate


class UserProfile(BaseModel):
    id: UUID4
    username: str
    last_name: str
    first_name: str
    patronymic: str
    is_superuser: bool
    is_active: Optional[bool] = True
    avatar: Optional[str] = None
    organization: Optional[OrganizationInDB] = None
    access_tors: Optional[List[OrganizationInDB]] = None
    created_at: datetime

    class Config:
        orm_mode = True
