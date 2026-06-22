from pydantic import BaseModel
from typing import List


class ClinicalNote(BaseModel):
    note_text: str


class SOAPNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str


class ICD10Code(BaseModel):
    code: str
    description: str
    confidence: float


class RiskFlag(BaseModel):
    risk_type: str
    severity: str
    description: str


class NoteAnalysis(BaseModel):
    soap: SOAPNote
    icd10_codes: List[ICD10Code]
    risk_flags: List[RiskFlag]
    follow_up_recommendations: List[str]
    note_id: str
    processed_at: str
