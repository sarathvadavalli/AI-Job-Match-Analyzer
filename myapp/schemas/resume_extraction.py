from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class ResumeExtractionInput(BaseModel):
    text: str
    links: Optional[list[str]] = Field(default_factory=list)


class Education(BaseModel):
    degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None


class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: list[str] = Field(default_factory=list)


class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: list[str] = Field(default_factory=list)
    github_repo: Optional[str] = None


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

    skills: list[str] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    handles: Optional[list[Handle]] = Field(default_factory=list)
    links: Optional[list[Link]] = Field(default_factory=list)