from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.api_responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", app_env=settings.app_env)

