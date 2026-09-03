from pydantic import BaseModel
from typing import Optional

from myapp.schemas.job_extraction import JobExtraction

class JobRequest(BaseModel):
    description: str


class Experience(BaseModel):
    min: Optional[float]
    max: Optional[float]


class JobResponse(BaseModel):
    job_title: str
    experience_years: Experience
    required_skills: list[str]
    preferred_skills: list[str]
    soft_skills: list[str]
    location: Optional[str]

    @classmethod
    def from_extraction(cls, extraction: JobExtraction):
        return cls(
            job_title=extraction.job_title.value,
            experience_years=Experience(
                min=extraction.experience_years.min.value,
                max=extraction.experience_years.max.value,
            ),
            required_skills=extraction.required_skills.value,
            preferred_skills=extraction.preferred_skills.value,
            soft_skills=extraction.soft_skills.value,
            location=extraction.location.value,
        )
