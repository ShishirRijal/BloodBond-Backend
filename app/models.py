from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text

from .database import Base

# Create a SQLAlchemy model for the User table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    phone = Column(String(10), nullable=False, unique=True, index=True)
    address = Column(String, nullable=False)
    blood_group = Column(String, nullable=False)
    is_donor = Column(Boolean, nullable=False)
    is_male = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
