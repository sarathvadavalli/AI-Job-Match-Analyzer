from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from pymongo.errors import DuplicateKeyError

from myapp.core.db import users_collection
from myapp.core.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from myapp.schemas.auth import TokenResponse, MessageResponse, UserCreate, UserLogin, UserProfile

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    now = datetime.now(timezone.utc)

    user = {
        "name": payload.name.strip(),
        "username": payload.username.lower(),
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "created_at": now,
        "last_login_at": None,
    }

    try:
        users_collection.insert_one(user)
    except DuplicateKeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
             detail="This username or email already exists.",
        ) from exc

    return {"message": "Account created successfully."}


@router.post("/login", response_model=MessageResponse)
def login_user(payload: UserLogin, response: Response):
    identifier = payload.identifier.strip().lower()

    if "@" in identifier:
        # Treat as email
        user = users_collection.find_one({"email": identifier})
    else:
        # Treat as username
        user = users_collection.find_one({"username": identifier})

    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or username or password.",
        )

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login_at": datetime.now(timezone.utc)}},
    )
    
    token = create_access_token(user["username"])
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age= 60*60
    )

    return {"message": "Authentication successful"}


@router.post("/logout", response_model=MessageResponse)
def logout(response: Response):
    response.delete_cookie(
        key="access_token"
    )

    return {"message": "Logged out successfully"}
