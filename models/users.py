from typing import Optional
from sqlalchemy import Boolean, Column, Integer, String,  ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from models.donors import Donor
# from . import hospitals, donors


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_donor = Column(Boolean, nullable=False)
    # Either donor_id or hospital_id will be null, depending on the value of is_donor
    donor_id = Column(Integer, ForeignKey(
        "donors.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    hospital_id = Column(Integer, ForeignKey(
        "hospitals.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    donor = relationship("Donor")
    hospital = relationship("Hospital")
