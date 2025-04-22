import os
import json
import fitz  # PyMuPDF
import re
from typing import Dict, List, Optional

class SUTService:
    def __init__(self, sut_pdf_path: str = "SUT.pdf"):
        self.sut_pdf_path = sut_pdf_path
        if not os.path.exists(sut_pdf_path):
            raise FileNotFoundError(f"SUT.pdf not found at {sut_pdf_path}")
    
    def extract_text_from_pdf(self) -> str:
        """Extract text content from SUT.pdf"""
        doc = fitz.open(self.sut_pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    
    def find_relevant_section(self, text: str, medication_name: str) -> Optional[str]:
        """Find relevant section in SUT text for given medication"""
        # Simple implementation - in a real app, this would be more sophisticated
        # using regex or text matching to locate the specific SUT section
        
        # This is a placeholder; actual implementation would search for specific sections
        medication_lower = medication_name.lower()
        
        # Example pattern matching for common drug groups
        patterns = [
            (r"atorvastatin", "LDL değeri kontrol edilmeli"),
            (r"entekavir", "Kronik Hepatit B tedavisinde kullanım şartları kontrol edilmeli"),
            (r"floben", "Rapor detaylı kontrol edilmeli"),
        ]
        
        results = []
        for pattern, note in patterns:
            if re.search(pattern, medication_lower):
                results.append({
                    "pattern": pattern,
                    "note": note,
                    "requirement": "Rapor gerekli"
                })
        
        return results if results else None
    
    def evaluate_prescription(self, prescription_data: Dict) -> Dict:
        """
        Evaluate a prescription based on SUT rules
        
        Returns a dict with evaluation results
        """
        sut_text = self.extract_text_from_pdf()
        
        evaluation_results = {
            "prescription_number": prescription_data.get("prescription_number", ""),
            "evaluation_summary": "",
            "medications": []
        }
        
        medications = prescription_data.get("medications", [])
        
        for med in medications:
            med_name = med.get("name", "")
            med_evaluation = {
                "name": med_name,
                "sut_requirements": self.find_relevant_section(sut_text, med_name),
                "status": "❓" # Default to unknown
            }
            
            # Determine medication status
            if med.get("report_required") and not med.get("report_valid"):
                med_evaluation["status"] = "✘"  # Report required but not valid
            elif self.find_relevant_section(sut_text, med_name) and med.get("report_valid"):
                med_evaluation["status"] = "✔"  # Requirements met
            elif not self.find_relevant_section(sut_text, med_name):
                med_evaluation["status"] = "✔"  # No special requirements
            
            evaluation_results["medications"].append(med_evaluation)
        
        # Overall evaluation
        if any(med["status"] == "✘" for med in evaluation_results["medications"]):
            evaluation_results["evaluation_summary"] = "✘ Reçete SUT'a uygun değil"
        elif all(med["status"] == "✔" for med in evaluation_results["medications"]):
            evaluation_results["evaluation_summary"] = "✔ Reçete SUT'a uygun"
        else:
            evaluation_results["evaluation_summary"] = "❓ Reçete değerlendirmesi tamamlanamadı"
        
        return evaluation_results 