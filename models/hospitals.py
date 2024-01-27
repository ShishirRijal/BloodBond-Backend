from sqlalchemy import TIMESTAMP, Boolean, Column, Double, ForeignKey, Integer, String, text

from app.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String(length=10), nullable=False, unique=True, index=True)
    latitude = Column(Double, nullable=False)
    image = Column(String, nullable=False)
    longitude = Column(Double, nullable=False)
    city = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
