# This file contains the Pydantic models,
# which are used to define the schema for validation.

from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    blood_group: str
    is_donor: bool
    is_male: bool


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
