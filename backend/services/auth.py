from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.core.settings import settings
from backend.core.database import get_db
from backend.services.users import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        payload = data.copy()
        payload["exp"] = datetime.now(timezone.utc) + (expires_delta or timedelta(
            minutes=settings.access_token_expire_minutes))
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    def validate_token_and_get_user(self, credentials: HTTPAuthorizationCredentials):
        try:
            payload = jwt.decode(
                credentials.credentials,
                settings.secret_key,
                algorithms=[settings.algorithm],
            )
            username = payload.get("sub")

            if not username:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

            user_repo = UserRepository(self.db)
            user = user_repo.get_by_username(username)

            if not user:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")

            return user

        except jwt.PyJWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.validate_token_and_get_user(credentials)
