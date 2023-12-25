from sqlalchemy import CHAR, TIMESTAMP,  Column, DateTime, Integer, String, text

from app.database import Base


class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    phone = Column(String(length=10), nullable=False, unique=True, index=True)
    # location = Column(Geography(geometry_type='POINT', srid=4326))

    blood_group = Column(String, nullable=False)
    sex = Column(CHAR, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
