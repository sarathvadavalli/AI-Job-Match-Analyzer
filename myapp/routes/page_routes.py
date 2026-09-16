from fastapi import APIRouter, Request, Depends, Body, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from pymongo.errors import DuplicateKeyError

from myapp.core.db import users_collection, profiles_collection
from myapp.core.security import get_current_user
from myapp.schemas.resume_extraction import ProfileResponse

templates = Jinja2Templates(directory="myapp/templates")
router = APIRouter(tags=["Pages"])


@router.get("/")
def index():
    return RedirectResponse(url="/login")


@router.get("/login")
def login_page(request: Request):
    error = request.cookies.get("flash_error", "")
    response = templates.TemplateResponse(
        request, 
        "login.html", 
        context={"error": error}
    )
    if error != "":
        response.delete_cookie("flash_error")

    return response


@router.get("/dashboard")
def dashboard_page(request: Request, user = Depends(get_current_user)):
    response = templates.TemplateResponse(
        request,
        name="dashboard.html",
        context={"request": request}
    )
    response.headers["Cache-Control"] = "no-store"

    return response


@router.get("/profile", response_model=ProfileResponse)
def profile_page(request: Request, user = Depends(get_current_user)):
    user_id = user['_id']
    profile = profiles_collection.find_one({'user_id': user_id})
    if not profile:
        profile = {}
    else:
        profile.pop('_id')
        profile.pop('user_id')

    response = templates.TemplateResponse(
        request,
        name="profile.html",
        context={
            "request": request,
            "user": user,
            "profile": profile,
        }
    )
    response.headers["Cache-Control"] = "no-store"

    return response


@router.post("/profile", response_model=ProfileResponse)
def save_profile(profile: dict = Body(...), user=Depends(get_current_user)):
    user_id = user['_id']
    record = profiles_collection.find_one({'user_id': user_id})

    try:
        if not record:
            profile['user_id'] = user_id
            profiles_collection.insert_one(profile)
            profile.pop('user_id')
        else:
            profiles_collection.update_one(
                {"user_id": user_id},
                {"$set": profile}
            )
    except DuplicateKeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
             detail="This user's profile already exists.",
        ) from exc

    return {"message": "Profile saved successfully.", "profile": profile}


@router.get("/jd/upload")
def upload_jd_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        name="upload_jd.html",
        context={"request": request, "user": user}
    )


@router.get("/resume/upload")
def upload_resume_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        name="upload_resume.html",
        context={"request": request, "user": user}
    )


@router.get("/analysis")
def analysis_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        name="analysis.html",
        context={"request": request, "user": user}
    )
