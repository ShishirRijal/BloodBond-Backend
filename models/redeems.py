from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from app.database import Base


class Redeem(Base):
    __tablename__ = 'redeems'

    id = Column(Integer, primary_key=True, index=True)
    reward_id = Column(Integer, ForeignKey('rewards.id'))
    donor_id = Column(Integer, ForeignKey('donors.id'))

    redeemed_at = Column(TIMESTAMP(timezone=True),
                         nullable=False, server_default=text('NOW()'))

    reward = relationship("Reward")
