from sqlalchemy import Column, Integer, Double, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EmergencyRequest(Base):
    __tablename__ = 'emergency_requests'

    id = Column(Integer, primary_key=True, nullable=False)
    patient_name = Column(String, nullable=False)
    blood_group = Column(String, nullable=False)
    # required for what medical condition
    medical_condition = Column(String, nullable=False)
    # medical report image, or pdf
    report = Column(String, nullable=False)
    requested_time = Column(DateTime, nullable=False)
    expiry_time = Column(DateTime, nullable=False)

    donor_id = Column(Integer, ForeignKey('donors.id'), nullable=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)

    donor = relationship("Donor", back_populates="emergency_requests")
    hospital = relationship("Hospital", back_populates="emergency_requests")
