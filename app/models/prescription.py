from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    prescription_number = Column(String(50), unique=True, index=True)
    patient_name = Column(String(100))
    doctor_name = Column(String(100))
    doctor_specialty = Column(String(100))
    prescription_type = Column(String(50))
    prescription_subtype = Column(String(50), nullable=True)
    provizyon_type = Column(String(50), nullable=True)
    medications = Column(Text)  # JSON string of medications
    uploaded_file_path = Column(String(255), nullable=True)  # Optional in manual mode
    sut_evaluation = Column(Text, nullable=True)  # Store AI evaluation results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 