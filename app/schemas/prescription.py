from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class MedicationBase(BaseModel):
    name: str
    barcode: Optional[str] = None
    dose: Optional[str] = None
    quantity: Optional[int] = None
    instructions: Optional[str] = None
    report_required: Optional[bool] = None
    report_valid: Optional[bool] = None

class PrescriptionBase(BaseModel):
    prescription_number: str
    patient_name: str
    doctor_name: str
    doctor_specialty: str
    prescription_type: str
    prescription_subtype: Optional[str] = None
    provizyon_type: Optional[str] = None
    medications: List[MedicationBase]

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionResponse(PrescriptionBase):
    id: int
    uploaded_file_path: Optional[str] = None
    sut_evaluation: Optional[Dict] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PrescriptionQuery(BaseModel):
    prescription_number: Optional[str] = None
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None

class SUTEvaluationRequest(BaseModel):
    prescription_id: int

class SUTEvaluationResponse(BaseModel):
    prescription_id: int
    evaluation: Dict
    medications: List[Dict]

class PrescriptionFileUpload(BaseModel):
    input_mode: str = "upload"

class PrescriptionManualEntry(PrescriptionBase):
    input_mode: str = "manual" 