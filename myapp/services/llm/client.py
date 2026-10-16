import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from myapp.schemas.job_extraction import JobExtraction
from myapp.schemas.resume_extraction import ResumeProfile
from myapp.schemas.resume_extraction import ResumeExtractionInput
from myapp.schemas.job_match_result import MatchResult
from myapp.services.llm.context import (
    JD_SYSTEM_PROMPT,
    MATCH_SYSTEM_PROMPT,
    RESUME_SYSTEM_PROMPT,
)

load_dotenv()

logger = logging.getLogger()


class LLMClient:

    def __init__(self):
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")

        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

        self.client = OpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def extract_job_info(self, description: str) -> JobExtraction:
        try:
            logger.info("Sending job extraction request to OpenRouter.")
            response = self.client.beta.chat.completions.parse(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": JD_SYSTEM_PROMPT},
                    {"role": "user", "content": description},
                ],
                response_format=JobExtraction,
                temperature=0.1,
            )
            res = response.choices[0].message.parsed
            if res is None:
                raise ValueError("OpenRouter returned no parsed job extraction.")

            logger.info("Received parsed job extraction from OpenRouter.")
            return res

        except Exception as e:
            logger.exception("Job extraction request failed.")
            raise RuntimeError(
                f"Failed to extract job information: {str(e)}"
            ) from e

    def extract_resume_info(self, description: ResumeExtractionInput) -> ResumeProfile:
        prompt = f"""
RESUME TEXT:
{description.text}
HYPERLINKS FOUND IN RESUME:
{description.links}
Use both the resume text and hyperlinks to construct the candidate profile.
Classify the hyperlinks appropriately.
"""

        try:
            logger.info("Sending resume extraction request to OpenRouter.")
            response = self.client.beta.chat.completions.parse(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": RESUME_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                response_format=ResumeProfile,
                temperature=0.1,
            )

            res = response.choices[0].message.parsed
            if res is None:
                raise ValueError("OpenRouter returned no parsed resume profile.")

            logger.info("Received parsed resume profile from OpenRouter.")
            return res

        except Exception as e:
            logger.exception("Resume extraction request failed.")
            raise RuntimeError(
                f"Failed to extract resume information: {str(e)}"
            ) from e

    def generate_match_feedback(self, profile: dict, jd: str) -> MatchResult:
        prompt = f"""
CANDIDATE'S PROFILE: 
{profile}
JOB DESCRIPTION:
{jd}
"""
        try:
            logger.info("Sending resume match request to OpenRouter.")
            response = self.client.beta.chat.completions.parse(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": MATCH_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                response_format=MatchResult,
                temperature=0.2,
            )

            res = response.choices[0].message.parsed
            if res is None:
                raise ValueError("OpenRouter returned no parsed match result.")
            logger.info("Received parsed resume match result from OpenRouter.")

            with open("output.json", "w", encoding="utf-8") as f:
                f.write(res.model_dump_json(indent=4))

            return res
        except Exception as e:
            logger.exception("Resume match request failed.")
            raise RuntimeError(
                f"Failed to generate match feedback: {str(e)}"
            ) from e
