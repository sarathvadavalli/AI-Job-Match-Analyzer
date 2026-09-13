from typing import Literal
from pydantic import BaseModel, Field

class SkillAnalysis(BaseModel):
    skill: str = Field(
        description="The job skill being evaluated"
    )
    level: Literal["basic", "hands_on", "strong"] = Field(
        description="Candidate's demonstrated proficiency: basic, hands_on, or strong."
    )
    evidence: str = Field(
        description="Explicit evidence from the candidate's skills, experience, or projects supporting this assessment"
    )


class Missing(BaseModel):
    skill: str = Field(
        description="The job skill being evaluated"
    )
    label: Literal["required", "optional"] = Field(
        description="Label that describes if the missing skill is a required/optional one."
    )


class Feedback(BaseModel):
    label: Literal["skills", "education", "experience", "projects"] = Field(
        description="Category of the suggested improvement"
    )
    description: str = Field(
        description="Specific and actionable improvement suggestion"
    )


class MatchResult(BaseModel):
    match_score: int = Field(
        ge=0,
        le=100,
        description="Overall candidate-job match score from 0 to 100, based on skills, proficiency, experience, education, and project evidence"
    )

    skill_analysis: list[SkillAnalysis] = Field(
        default_factory=list,
        description="Analysis of each relevant job skill based on explicit evidence from the candidate experience, projects or certifications"
    )

    missing_skills: list[Missing] = Field(
        default_factory=list,
        description="The job skills that donot exist in candidate profile"
    )

    feedback: list[Feedback] = Field(
        default_factory=list,
        description="Actionable suggestions for improving job fit"
    )
