from myapp.schemas.job_match_result import MatchResult
from myapp.services.llm.client import LLMClient


class MatchService:

    def match(self, profile: dict, job_description: str) -> MatchResult:
        try:
            llm_client = LLMClient()
            extraction: ResumeProfile = (
                llm_client.generate_match_feedback(profile, job_description)
            )

            return extraction

        except Exception as e:
            raise RuntimeError(
                f"Failed to process resume description: {str(e)}"
            ) from e