from sqlalchemy import Boolean, Column, Integer, String,  ForeignKey

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_donor = Column(Boolean, nullable=False)
