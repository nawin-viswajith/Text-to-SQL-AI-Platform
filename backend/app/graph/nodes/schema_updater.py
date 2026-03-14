from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentError, AgentState


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    if not state.needs_schema_refresh:
        state.next_step = "finish"
        state.reflection_notes.append("Schema update skipped (flag not set).")
        state.updated_at = datetime.now(timezone.utc)
        return state

    try:
        updated = deps.indexer.refresh()
        state.needs_schema_refresh = False
        state.next_step = "rag_retrieval"
        state.reflection_notes.append(
            f"Schema index refreshed ({updated} table documents); retrying generation."
        )
    except Exception as exc:
        state.error = AgentError(
            code="SCHEMA_REFRESH_FAILED",
            message=str(exc),
            category="unknown",
            retryable=False,
        )
        state.next_step = "finish"
        state.reflection_notes.append("Schema refresh failed; stopping retries.")
    state.updated_at = datetime.now(timezone.utc)
    return state

