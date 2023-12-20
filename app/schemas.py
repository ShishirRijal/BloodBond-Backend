# This file contains the Pydantic models,
# which are used to define the schema for validation.

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
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
    email: EmailStr
    password: str


class UserChangePassword(BaseModel):
    email: EmailStr
    password: str
    new_password: str


class UserForgotPassword(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None
