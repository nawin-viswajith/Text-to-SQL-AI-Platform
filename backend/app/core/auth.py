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


def require_role(
    allowed_roles: set[str],
    x_user_role: str | None = Header(default=None),
) -> None:
    settings = get_settings()
    if not settings.rbac_enabled:
        return
    role = (x_user_role or "viewer").strip().lower()
    allowed = {r.lower() for r in allowed_roles}
    if role not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{role}' is not allowed for this action.",
        )


def require_data_admin_role(x_user_role: str | None = Header(default=None)) -> None:
    require_role({"admin", "data_engineer"}, x_user_role=x_user_role)


def require_mcp_role(x_user_role: str | None = Header(default=None)) -> None:
    require_role({"admin", "developer", "analyst"}, x_user_role=x_user_role)


def require_analyst_role(x_user_role: str | None = Header(default=None)) -> None:
    require_role({"admin", "analyst", "data_engineer"}, x_user_role=x_user_role)
