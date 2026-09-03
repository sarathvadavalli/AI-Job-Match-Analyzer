from myapp.schemas.job_extraction import JobExtraction
from myapp.schemas.job_response import JobResponse
from myapp.services.llm.client import LLMClient


class JobService:

    def extract_job_info(self, description: str) -> JobResponse:
        try:
            llm_client = LLMClient()
            extraction: JobExtraction = (
                llm_client.extract_job_info(description)
            )

            res = JobResponse.from_extraction(extraction)
            # print("Validated Response:")
            # print(res)
            return res

        except Exception as e:
            raise RuntimeError(
                f"Failed to process job description: {str(e)}"
            ) from e
