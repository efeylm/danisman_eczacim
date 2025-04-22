from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
import json
import os
from typing import List, Optional
import shutil
import re
import uuid
import datetime
from app.db.database import get_db
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse, SUTEvaluationResponse
from app.services.sut_service import SUTService

router = APIRouter(tags=["Prescriptions"])

# Define uploads directory
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/prescriptions/", response_model=PrescriptionResponse)
async def create_prescription(
    input_mode: str = Form(...),
    prescription_data: Optional[str] = Form(None),
    prescription_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Upload a prescription and save it to the database.
    Can work in two modes:
    - upload: Upload a prescription file (PDF or image)
    - manual: Manually enter prescription data
    """
    try:
        # Validate input mode
        if input_mode not in ["upload", "manual"]:
            raise HTTPException(status_code=400, detail="Invalid input mode. Must be 'upload' or 'manual'")
        
        # Validate that we have the right data for the selected mode
        if input_mode == "upload" and not prescription_file:
            raise HTTPException(status_code=400, detail="Prescription file is required in upload mode")
        
        if input_mode == "manual" and not prescription_data:
            raise HTTPException(status_code=400, detail="Prescription data is required in manual mode")
        
        # Create Prescription object
        db_prescription = Prescription()
        
        # Handle upload mode
        if input_mode == "upload":
            # Generate a unique filename
            file_ext = os.path.splitext(prescription_file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_location = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Save the uploaded file
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(prescription_file.file, file_object)
            
            # For now, just create a minimal prescription record
            # In a real implementation, OCR would extract data from the file
            db_prescription.prescription_number = f"AUTO-{uuid.uuid4().hex[:8].upper()}"
            db_prescription.patient_name = "Dosyadan Otomatik"
            db_prescription.doctor_name = "Dosyadan Otomatik"
            db_prescription.doctor_specialty = "Belirtilmemiş"
            db_prescription.prescription_type = "Normal"
            db_prescription.uploaded_file_path = file_location
            
            # Set default dummy medication data
            # In a real implementation, this would be extracted from the file
            medications = [
                {
                    "name": "Otomatik Tespit Edilmiş İlaç",
                    "barcode": "",
                    "dose": "",
                    "quantity": 1,
                    "report_required": False,
                    "report_valid": False
                }
            ]
            
            db_prescription.medications = json.dumps(medications)
            
        # Handle manual mode
        elif input_mode == "manual":
            # Parse prescription data from form
            prescription_dict = json.loads(prescription_data)
            
            # Set prescription attributes
            db_prescription.prescription_number = prescription_dict.get("prescription_number", "")
            db_prescription.patient_name = prescription_dict.get("patient_name", "")
            db_prescription.doctor_name = prescription_dict.get("doctor_name", "")
            db_prescription.doctor_specialty = prescription_dict.get("doctor_specialty", "")
            db_prescription.prescription_type = prescription_dict.get("prescription_type", "")
            db_prescription.prescription_subtype = prescription_dict.get("prescription_subtype", "")
            db_prescription.provizyon_type = prescription_dict.get("provizyon_type", "")
            db_prescription.medications = json.dumps(prescription_dict.get("medications", []))
            db_prescription.uploaded_file_path = ""  # No file in manual mode
        
        # Save the prescription to the database
        db.add(db_prescription)
        db.commit()
        db.refresh(db_prescription)
        
        # Return the saved prescription
        return {
            "id": db_prescription.id,
            "prescription_number": db_prescription.prescription_number,
            "patient_name": db_prescription.patient_name,
            "doctor_name": db_prescription.doctor_name,
            "doctor_specialty": db_prescription.doctor_specialty,
            "prescription_type": db_prescription.prescription_type,
            "prescription_subtype": db_prescription.prescription_subtype,
            "provizyon_type": db_prescription.provizyon_type,
            "medications": json.loads(db_prescription.medications),
            "uploaded_file_path": db_prescription.uploaded_file_path,
            "sut_evaluation": json.loads(db_prescription.sut_evaluation) if db_prescription.sut_evaluation else None,
            "created_at": db_prescription.created_at,
            "updated_at": db_prescription.updated_at
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prescription upload failed: {str(e)}")

@router.get("/prescriptions/{prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    """
    Get a prescription by ID
    """
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    return {
        "id": prescription.id,
        "prescription_number": prescription.prescription_number,
        "patient_name": prescription.patient_name,
        "doctor_name": prescription.doctor_name,
        "doctor_specialty": prescription.doctor_specialty,
        "prescription_type": prescription.prescription_type,
        "prescription_subtype": prescription.prescription_subtype,
        "provizyon_type": prescription.provizyon_type,
        "medications": json.loads(prescription.medications),
        "uploaded_file_path": prescription.uploaded_file_path,
        "sut_evaluation": json.loads(prescription.sut_evaluation) if prescription.sut_evaluation else None,
        "created_at": prescription.created_at,
        "updated_at": prescription.updated_at
    }

@router.post("/prescriptions/{prescription_id}/evaluate", response_model=SUTEvaluationResponse)
async def evaluate_prescription(prescription_id: int, db: Session = Depends(get_db)):
    """
    Evaluate a prescription against SUT rules
    """
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    try:
        # Parse medications
        medications = json.loads(prescription.medications)
        
        # Create prescription data for evaluation
        prescription_data = {
            "prescription_number": prescription.prescription_number,
            "medications": medications
        }
        
        # Evaluate with SUT service
        sut_service = SUTService()
        evaluation_result = sut_service.evaluate_prescription(prescription_data)
        
        # Save evaluation to DB
        prescription.sut_evaluation = json.dumps(evaluation_result)
        db.commit()
        db.refresh(prescription)
        
        return {
            "prescription_id": prescription.id,
            "evaluation": evaluation_result,
            "medications": medications
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@router.get("/prescriptions/", response_model=List[PrescriptionResponse])
async def list_prescriptions(db: Session = Depends(get_db)):
    """
    List all prescriptions
    """
    prescriptions = db.query(Prescription).all()
    result = []
    
    for prescription in prescriptions:
        result.append({
            "id": prescription.id,
            "prescription_number": prescription.prescription_number,
            "patient_name": prescription.patient_name,
            "doctor_name": prescription.doctor_name,
            "doctor_specialty": prescription.doctor_specialty,
            "prescription_type": prescription.prescription_type,
            "prescription_subtype": prescription.prescription_subtype,
            "provizyon_type": prescription.provizyon_type,
            "medications": json.loads(prescription.medications),
            "uploaded_file_path": prescription.uploaded_file_path,
            "sut_evaluation": json.loads(prescription.sut_evaluation) if prescription.sut_evaluation else None,
            "created_at": prescription.created_at,
            "updated_at": prescription.updated_at
        })
    
    return result 