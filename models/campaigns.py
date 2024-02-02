from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    banner = Column(String, nullable=False)
    interested_donors = Column(Integer, nullable=False, default=0)
    donated_donors = Column(Integer, nullable=False, default=0)
    total_bags = Column(Integer, nullable=False, default=0)

    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)

    hospital = relationship("Hospital")
