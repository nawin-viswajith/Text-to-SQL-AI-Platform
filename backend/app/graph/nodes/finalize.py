from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    state.updated_at = datetime.now(timezone.utc)
    return state

