from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    state.db_connected = deps.mysql_client.ping()
    if state.db_connected:
        state.mode = "connected"
        state.next_step = "rag_retrieval"
        state.reflection_notes.append("Database connection verified.")
    else:
        state.mode = "generic_sql_fallback"
        state.next_step = "sql_generation"
        state.reflection_notes.append(
            "Database connection unavailable; generated generic SQL fallback."
        )
    state.updated_at = datetime.now(timezone.utc)
    return state

