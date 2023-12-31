from sqlalchemy import CHAR, TIMESTAMP,  Column, DateTime, Double, Integer, String, text

from app.database import Base


class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String(length=10), nullable=False, unique=True, index=True)
    image = Column(String, nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    blood_group = Column(String, nullable=False)
    sex = Column(CHAR, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
