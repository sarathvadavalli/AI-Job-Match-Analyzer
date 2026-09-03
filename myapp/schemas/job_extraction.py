from pydantic import BaseModel
from typing import Optional

class ExtractedField(BaseModel):
    value: Optional[str] = None
    confidence: float
    source: Optional[str] = None


class ExtractedList(BaseModel):
    value: list[str]
    confidence: float
    source: Optional[str] = None


class Experience(BaseModel):
    min: ExtractedField
    max: ExtractedField
    confidence: float
    source: Optional[str] = None


class JobExtraction(BaseModel):
    job_title: ExtractedField
    experience_years: Experience
    required_skills: ExtractedList
    preferred_skills: ExtractedList
    soft_skills: ExtractedList
    location: ExtractedField
