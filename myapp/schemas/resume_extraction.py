from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import date


class ResumeExtractionInput(BaseModel):
    text: str
    links: Optional[list[str]] = Field(default_factory=list)


class Education(BaseModel):
    degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    start_year: Optional[int] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None


class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    employment_type: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current_job: Optional[bool] = None
    responsibilities: Optional[list[str]] = Field(default_factory=list)


class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[list[str]] = Field(default_factory=list)
    technologies: Optional[list[str]] = Field(default_factory=list)
    github_repo: Optional[str] = None
    live_url: Optional[str] = None


class Certification(BaseModel):
    name: Optional[str] = None
    organization: Optional[str] = None
    url: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None


class Handle(BaseModel):
    platform: str
    url: str


class Link(BaseModel):
    type: str
    title: Optional[str] = None
    url: str


class ResumeProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

    skills: Optional[list[str]] = Field(default_factory=list)
    technical_skills: Optional[list[str]] = Field(default_factory=list)
    soft_skills: Optional[list[str]] = Field(default_factory=list)
    languages: Optional[list[str]] = Field(default_factory=list)
    education: Optional[list[Education]] = Field(default_factory=list)
    experience: Optional[list[Experience]] = Field(default_factory=list)
    projects: Optional[list[Project]] = Field(default_factory=list)
    certifications: Optional[list[Certification]] = Field(default_factory=list)
    handles: Optional[list[Handle]] = Field(default_factory=list)
    links: Optional[list[Link]] = Field(default_factory=list)


class ProfileResponse(BaseModel):
    message: str
    profile: ResumeProfile