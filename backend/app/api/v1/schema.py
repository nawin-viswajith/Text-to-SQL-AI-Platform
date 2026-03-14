from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.auth import require_data_admin_role
from app.core.dependencies import get_orchestrator
from app.schemas.api_requests import SchemaRefreshRequest
from app.schemas.api_responses import SchemaRefreshResponse
from app.services.query_orchestrator import QueryOrchestrator

router = APIRouter(tags=["schema"], dependencies=[Depends(require_data_admin_role)])


@router.post("/schema/refresh", response_model=SchemaRefreshResponse)
def refresh_schema(
    payload: SchemaRefreshRequest,
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> SchemaRefreshResponse:
    return orchestrator.refresh_schema_index(table_names=payload.table_names)
