# This file contains the Pydantic models,
# which are used to define the schema for validation.

from pydantic import BaseModel


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
    created_at: str

    class Config:
        from_attributes = True
