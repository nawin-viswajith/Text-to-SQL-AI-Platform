from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.core.auth import require_api_access, require_mcp_role
from app.core.dependencies import get_orchestrator
from app.mcp.resources import MCPResources
from app.mcp.server import SlidingWindowRateLimiter
from app.mcp.tools import MCPTools
from app.schemas.api_requests import MCPToolRequest
from app.services.query_orchestrator import QueryOrchestrator

router = APIRouter(tags=["mcp"], dependencies=[Depends(require_api_access), Depends(require_mcp_role)])
rate_limiter = SlidingWindowRateLimiter(max_requests=60, window_seconds=60)


def _enforce_rate_limit(client_id: str) -> None:
    if not rate_limiter.allow(client_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded.",
        )


@router.post("/mcp/tools/{tool_name}")
def call_tool(
    tool_name: str,
    payload: MCPToolRequest,
    x_client_id: str | None = Header(default="anonymous-client"),
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> dict:
    _enforce_rate_limit(x_client_id or "anonymous-client")
    tools = MCPTools(orchestrator)
    dispatch = {
        "generate_sql": tools.generate_sql,
        "execute_readonly_sql": tools.execute_readonly_sql,
        "refresh_schema_index": tools.refresh_schema_index,
        "get_table_catalog": tools.get_table_catalog,
        "evaluate_ragas": tools.evaluate_ragas,
    }
    if tool_name not in dispatch:
        raise HTTPException(status_code=404, detail=f"Unknown MCP tool: {tool_name}")
    return {
        "tool": tool_name,
        "result": dispatch[tool_name](payload.tool_input),
    }


@router.get("/mcp/resources/schema/catalog")
def get_schema_catalog(
    x_client_id: str | None = Header(default="anonymous-client"),
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> dict:
    _enforce_rate_limit(x_client_id or "anonymous-client")
    resources = MCPResources(orchestrator)
    return resources.schema_catalog()


@router.get("/mcp/resources/schema/table/{table_name}")
def get_schema_table(
    table_name: str,
    x_client_id: str | None = Header(default="anonymous-client"),
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> dict:
    _enforce_rate_limit(x_client_id or "anonymous-client")
    resources = MCPResources(orchestrator)
    return resources.schema_table(table_name=table_name)


@router.get("/mcp/resources/run/{run_id}/trace")
def get_run_trace(
    run_id: str,
    x_client_id: str | None = Header(default="anonymous-client"),
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> dict:
    _enforce_rate_limit(x_client_id or "anonymous-client")
    resources = MCPResources(orchestrator)
    return resources.run_trace(run_id=run_id)
