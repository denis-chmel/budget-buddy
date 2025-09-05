from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.settings import settings

router = APIRouter(tags=["health"])

class HealthResponse(BaseModel):
    status: str
    version: str

@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version=settings.app_version
    )
