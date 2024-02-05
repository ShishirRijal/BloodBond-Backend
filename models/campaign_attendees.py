from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class CampaignAttendee(Base):
    __tablename__ = 'campaign_attendees'

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey('donors.id'))
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    donated = Column(Boolean, default=False)
