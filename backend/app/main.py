from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.api.v1.health import router as health_router
from app.api.v1.mcp import router as mcp_router
from app.api.v1.query import router as query_router
from app.api.v1.schema import router as schema_router
from app.core.auth import require_docs_access
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(
    title=settings.swagger_title,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(query_router, prefix=settings.api_prefix)
app.include_router(schema_router, prefix=settings.api_prefix)
app.include_router(mcp_router, prefix=settings.api_prefix)


@app.get("/openapi.json", include_in_schema=False, dependencies=[Depends(require_docs_access)])
def openapi_spec():
    return get_openapi(
        title=app.title,
        version="0.1.0",
        routes=app.routes,
    )


@app.get("/docs", include_in_schema=False, dependencies=[Depends(require_docs_access)])
def swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title=f"{app.title} - Swagger UI")


@app.get("/redoc", include_in_schema=False, dependencies=[Depends(require_docs_access)])
def redoc_ui():
    return get_redoc_html(openapi_url="/openapi.json", title=f"{app.title} - ReDoc")

