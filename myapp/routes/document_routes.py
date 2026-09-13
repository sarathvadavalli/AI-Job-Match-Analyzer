from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from myapp.core.security import get_current_user
from myapp.core.db import profiles_collection

from myapp.services.job_service import JobService
from myapp.services.resume_service import ResumeService
from myapp.services.doc_service import DocumentService
from myapp.services.match_service import MatchService

from myapp.schemas.job_response import JobRequest, JobResponse
from myapp.schemas.resume_extraction import ResumeProfile
from myapp.schemas.job_match_result import MatchResult

router = APIRouter()

@router.post("/jd/extract", response_model=JobResponse)
async def extract_job_info(file: UploadFile = File(...)):
    file_name = file.filename
    extension = file_name.lower().split(".")[-1]

    if extension not in ["pdf", "docx", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, DOCX, or TXT file.",
        )

    try:
        content = await file.read()
        doc_service = DocumentService(file_type="job")
        description = doc_service.extract_text(file_name, content)

        job_service = JobService()
        result = job_service.extract_job_info(description.text)
        if isinstance(result, str) and result.startswith("Error:"):
            raise HTTPException(status_code=502, detail=result)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resume/extract", response_model=ResumeProfile)
async def extract_resume_info(file: UploadFile = File(...)):
    file_name = file.filename
    extension = file_name.lower().split(".")[-1]

    if extension not in ["pdf", "docx", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, DOCX, or TXT file.",
        )

    try:
        content = await file.read()        
        doc_service = DocumentService(file_type="resume")
        description = doc_service.extract_text(file_name, content)

        resume_service = ResumeService()
        result = resume_service.extract_resume_info(description)

        if isinstance(result, str) and result.startswith("Error:"):
            raise HTTPException(status_code=502, detail=result)

        profile = result.model_dump(mode="json")
        return profile

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resume/match", response_model=MatchResult)
async def match_resume(
    file: UploadFile | None = File(None),
    jd_text: str | None = Form(None),
    user = Depends(get_current_user),
):
    profile = profiles_collection.find_one({
        "user_id":user['_id']
    })

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found. Please create your profile first",
        )

    try:
        if file and file.filename:
            extension = file.filename.lower().split(".")[-1]
            if extension not in ["pdf", "docx", "txt"]:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file type. Please upload a PDF, DOCX, or TXT file.",
                )
            content = await file.read()
            doc_service = DocumentService(file_type="job")
            jd = doc_service.extract_text(file.filename, content).text
        elif jd_text and jd_text.strip():
            jd = jd_text.strip()
        else:
            raise HTTPException(
                status_code=400,
                detail="Provide a job description file or enter job description text.",
            )

        match_service = MatchService()
        result = match_service.match(
            profile=profile,
            job_description=jd
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
