import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI

from myapp.schemas.job_extraction import JobExtraction
from myapp.schemas.resume_extraction import ResumeProfile
from myapp.schemas.resume_extraction import ResumeExtractionInput
from myapp.services.llm.context import JD_SYSTEM_PROMPT, RESUME_SYSTEM_PROMPT

load_dotenv()

class LLMClient:

    def __init__(self):
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        # grok_api_key = os.getenv("GROK_API_KEY")

        if not gemini_api_key:
            raise ValueError(
                "API_KEY not found in environment variables."
            )

        # self.client = genai.Client(api_key=gemini_api_key)
        self.client = OpenAI(
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

    def extract_job_info(self, description: str) -> JobExtraction:
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=description,
                config=types.GenerateContentConfig(
                    system_instruction=JD_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=JobExtraction,
                    temperature=0.1,
                ),
            )

            res = JobExtraction.model_validate_json(response.text)
            # print("Validated Extraction:")
            # print(res)
            return res

        except Exception as e:
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
            print("Extracting resume information...")
            # response = self.client.models.generate_content(
            #     model="gemini-3.6-flash",
            #     contents=prompt,
            #     config=types.GenerateContentConfig(
            #         system_instruction=RESUME_SYSTEM_PROMPT,
            #         response_mime_type="application/json",
            #         response_schema=ResumeProfile,
            #         temperature=0.1,
            #     ),
            # )

            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": RESUME_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                response_format=ResumeProfile,
                temperature=0.1,
            )
 
            res: ResumeProfile = response.choices[0].message.parsed
            print("Raw Extraction Response:")
            print(res)
            return res

        except Exception as e:
            raise RuntimeError(
                f"Failed to extract resume information: {str(e)}"
            ) from e
