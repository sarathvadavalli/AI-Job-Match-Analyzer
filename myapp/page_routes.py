from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from myapp.core.security import get_current_user

templates = Jinja2Templates(directory="myapp/templates")
router = APIRouter(tags=["Pages"])


@router.get("/")
def index():
    return RedirectResponse(url="/login")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        name="login.html",
        context={"request": request}
    )


@router.get("/dashboard")
def dashboard_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        name="dashboard.html",
        context={"request": request}
    )


@router.get("/profile")
def profile_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        name="profile.html",
        context={"request": request, "user": user}
    )


@router.get("/upload/jd")
def upload_jd_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        name="upload_jd.html",
        context={"request": request, "user": user}
    )


@router.get("/upload/resume")
def upload_resume_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        name="upload_resume.html",
        context={"request": request, "user": user}
    )
