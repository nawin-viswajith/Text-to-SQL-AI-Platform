from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    if state.db_connected:
        state.rag_context = deps.retriever.retrieve(state.question, k=4)
        state.reflection_notes.append(f"Retrieved {len(state.rag_context)} schema context docs.")
    else:
        state.rag_context = []
    state.next_step = "sql_generation"
    state.updated_at = datetime.now(timezone.utc)
    return state

