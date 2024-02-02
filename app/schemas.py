# This file contains the Pydantic models,
# which are used to define the schema for validation.

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


# class UserBase(BaseModel):
#     name: str
#     email: EmailStr
#     phone: str
#     address: str
#     blood_group: str
#     is_donor: bool
#     is_male: bool


# class UserCreate(UserBase):
#     password: str


# class UserResponse(UserBase):
#     id: int
#     created_at: datetime

#     class Config:
#         from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserChangePassword(BaseModel):
    email: EmailStr
    password: str
    new_password: str


class UserForgotPassword(BaseModel):
    email: EmailStr


class UserResetPassword(BaseModel):
    email: EmailStr
    password: str


class UserOtpVerify(BaseModel):
    email: EmailStr
    otp: str


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class DonorBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    sex: str
    date_of_birth: datetime
    blood_group: str
    latitude: float
    longitude: float
    city: str

    @validator("date_of_birth", pre=True)
    def parse_date_of_birth(cls, value):
        if isinstance(value, datetime):
            return value  # Return the datetime object as is
        try:
            # Parse the input string into a datetime object
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Invalid date format. Please provide the date in YYYY-MM-DD format.")


class DonorCreate(DonorBase):
    email: EmailStr
    password: str
    image: str


class DonorResponse(DonorBase):
    id: int
    email: EmailStr
    created_at: datetime
    image: str
    last_donation_date: datetime | None
    points: int


# class DonorResponseVague(BaseModel):
#     id: int
#     first_name: str
#     last_name: str
#     blood_group: str
#     latitude: float
#     longitude: float
#     image: str

#     class Config:
#         from_attributes = True


class DonorUpdate(DonorBase):
    pass


class HospitalBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    latitude: float
    longitude: float
    image: str
    is_verified: bool | None = False
    city: str


class HospitalCreate(HospitalBase):
    password: str


class HospitalResponse(HospitalBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class HospitalResponseVague(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class HospitalUpdate(BaseModel):
    name: str
    phone: str
    latitude: float
    longitude: float


class UserAdd(BaseModel):
    email: EmailStr
    password: str
    is_donor: bool

# ! Emergency Requests


class EmergencyRequestBase(BaseModel):
    patient_name: str
    blood_group: str
    medical_condition: str
    report: str
    requested_time: datetime
    expiry_time: datetime


class EmergencyRequestCreate(EmergencyRequestBase):
    pass


class EmergencyRequestResponse(EmergencyRequestBase):
    id: int
    donor: DonorResponse | None
    hospital: HospitalResponse

    class Config:
        from_attributes = True
