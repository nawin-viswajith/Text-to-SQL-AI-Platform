from __future__ import annotations

from datetime import datetime, timezone

from app.core.security import SQLPolicyError
from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentError, AgentState


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    try:
        safe_sql = deps.sql_policy.validate_and_harden(state.candidate_sql or "")
        state.safe_sql = safe_sql
        state.error = None
        state.next_step = "execution"
        state.reflection_notes.append("SQL policy validation passed.")
    except SQLPolicyError as exc:
        state.error = AgentError(
            code="SQL_POLICY_BLOCK",
            message=str(exc),
            category="permission",
            retryable=False,
        )
        state.next_step = "reflexion_analyzer"
        state.reflection_notes.append("SQL policy validation blocked query.")
    state.updated_at = datetime.now(timezone.utc)
    return state

