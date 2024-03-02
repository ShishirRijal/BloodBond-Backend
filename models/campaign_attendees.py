from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class CampaignAttendee(Base):
    __tablename__ = 'campaign_attendees'

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey('donors.id'))
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    donated = Column(Boolean, default=False)
    __table_args__ = (UniqueConstraint(
        'donor_id', 'campaign_id', name='_donor_campaign_uc'),)

    donor = relationship("Donor")
    campaign = relationship("Campaign")
