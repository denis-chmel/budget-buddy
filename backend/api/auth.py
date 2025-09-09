from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta
from backend.core.settings import settings
from backend.services.users import get_user_repo, UserRepository
from backend.services.auth import AuthService, get_auth_service
from backend.schema.auth import LoginRequest, LoginResponse

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(
    login_request: LoginRequest,
    auth: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repo),
) -> LoginResponse:
    user = user_repo.get_by_username(login_request.username)
    is_new_user = False
    message = ""

    if user is None:
        user = user_repo.create(
            login_request.username,
            auth.hash_password(login_request.password),
        )
        is_new_user = True
        message = f"You've successfully registered, {user.username}!"
    else:
        if not auth.verify_password(login_request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        message = f"Welcome back, {user.username}!"

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        is_new_user=is_new_user,
        message=message
    )
