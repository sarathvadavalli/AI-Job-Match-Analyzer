from myapp.schemas.resume_extraction import ResumeProfile
from myapp.schemas.resume_extraction import ResumeExtractionInput
from myapp.services.llm.client import LLMClient


class ResumeService:

    def extract_resume_info(self, description: ResumeExtractionInput) -> ResumeProfile:
        try:
            llm_client = LLMClient()
            extraction: ResumeProfile = (
                    llm_client.extract_resume_info(description)
            )

            return extraction

        except Exception as e:
            raise RuntimeError(
                f"Failed to process resume description: {str(e)}"
            ) from e
