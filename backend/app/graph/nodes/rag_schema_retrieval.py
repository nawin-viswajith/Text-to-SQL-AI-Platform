from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    if state.db_connected:
        rag_context, diagnostics = deps.retriever.retrieve_with_metadata(
            question=state.question,
            k=4,
            strategy=state.retrieval_strategy,
            fetch_k=state.retrieval_fetch_k,
            mmr_lambda=state.mmr_lambda,
        )
        state.rag_context = rag_context
        state.retrieval_diagnostics = diagnostics
        deps.tracer.log_retrieval(
            trace_id=state.langsmith_trace_id,
            payload=diagnostics,
        )
        quality = diagnostics.get("quality", {})
        if quality:
            deps.tracer.log_metrics(
                trace_id=state.langsmith_trace_id,
                metrics={key: float(value) for key, value in quality.items()},
                source="retrieval",
            )
        state.reflection_notes.append(f"Retrieved {len(state.rag_context)} schema context docs.")
    else:
        state.rag_context = []
        state.retrieval_diagnostics = {
            "strategy": state.retrieval_strategy,
            "candidate_count": 0,
            "selected_tables": [],
            "reason": "db_disconnected",
        }
    state.next_step = "sql_generation"
    state.updated_at = datetime.now(timezone.utc)
    return state
