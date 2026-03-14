from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.auth import require_analyst_role
from app.core.dependencies import get_orchestrator
from app.schemas.api_requests import RagasEvaluationRequest
from app.schemas.api_responses import RagasEvaluationResponse
from app.services.query_orchestrator import QueryOrchestrator

router = APIRouter(tags=["evaluation"], dependencies=[Depends(require_analyst_role)])


@router.post("/evaluate/ragas", response_model=RagasEvaluationResponse)
def evaluate_ragas(
    payload: RagasEvaluationRequest,
    orchestrator: QueryOrchestrator = Depends(get_orchestrator),
) -> RagasEvaluationResponse:
    return orchestrator.evaluate_ragas(
        question=payload.question,
        answer=payload.answer,
        contexts=payload.contexts,
        reference_answer=payload.reference_answer,
        trace_id=payload.trace_id,
    )
