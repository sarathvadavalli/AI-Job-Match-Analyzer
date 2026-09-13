from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from myapp.core.security import get_current_user
from myapp.core.db import profiles_collection

from myapp.services.job_service import JobService
from myapp.services.resume_service import ResumeService
from myapp.services.doc_service import DocumentService
from myapp.services.match_service import MatchService

from myapp.schemas.job_response import JobRequest, JobResponse
from myapp.schemas.resume_extraction import ResumeProfile
from myapp.schemas.job_match_result import MatchResult
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/jd/extract", response_model=dict)
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

        # return JSONResponse(content=result.dict())
        return result.dict()

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
async def extract_resume_info(file: UploadFile = File(...), user = Depends(get_current_user)):
    profile = profiles_collection.find_one({
        "user_id":user['_id']
    })

    try:
        file_name = file.filename
        content = await file.read()
        doc_service = DocumentService(file_type="job")
        jd = doc_service.extract_text(file_name, content)

        match_service = MatchService()
        result = match_service.match(
            profile=profile,
            job_description=jd
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
