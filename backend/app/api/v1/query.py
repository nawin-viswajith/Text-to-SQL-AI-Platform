from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.dependencies import get_orchestrator
from app.schemas.api_requests import QueryRequest
from app.schemas.api_responses import QueryResponse, RunResponse
from app.services.query_orchestrator import QueryOrchestrator

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def run_query(
    payload: QueryRequest,
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> QueryResponse:
    return orchestrator.run_query(payload)


@router.post("/query/stream")
def stream_query(
    payload: QueryRequest,
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> StreamingResponse:
    stream = orchestrator.stream_query(payload)
    return StreamingResponse(stream, media_type="text/event-stream")


@router.get("/runs/{run_id}", response_model=RunResponse)
def get_run(
    run_id: str,
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> RunResponse:
    run_payload = orchestrator.get_run(run_id)
    if run_payload is None:
        raise HTTPException(status_code=404, detail="Run not found.")
    return RunResponse(run_id=run_id, payload=run_payload)

