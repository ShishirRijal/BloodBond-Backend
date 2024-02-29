from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from app.database import Base


class Reward(Base):
    __tablename__ = 'rewards'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('hospitals.id'))  # hospital
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    redeemed_quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))

    hospital = relationship("Hospital")
