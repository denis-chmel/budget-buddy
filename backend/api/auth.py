from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from backend.core.database import get_db
from backend.core.settings import settings
from backend.services.users import get_user_by_username, create_user
from backend.services.auth import verify_password, create_access_token
from backend.schema.auth import LoginRequest, LoginResponse

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = get_user_by_username(db, login_request.username)
    is_new_user = False
    message = ""

    if user is None:
        user = create_user(db, login_request.username, login_request.password)
        is_new_user = True
        message = f"You've successfully registered, {user.username}!"
    else:
        if not verify_password(login_request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        message = f"Welcome back, {user.username}!"

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        is_new_user=is_new_user,
        message=message
    )
