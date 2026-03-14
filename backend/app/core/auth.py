from __future__ import annotations

from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def require_docs_access(x_docs_token: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if settings.is_prod and x_docs_token != settings.docs_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized for docs access.",
        )


def require_api_access(x_api_token: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if settings.is_prod and x_api_token != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized API access.",
        )

