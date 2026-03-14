from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    if not state.error:
        state.next_step = "finish"
        state.reflection_notes.append("No errors detected; workflow completed.")
        state.updated_at = datetime.now(timezone.utc)
        return state

    if (
        state.error.category == "schema_mismatch"
        and state.error.retryable
        and state.retry_count < state.max_retries
    ):
        state.retry_count += 1
        state.needs_schema_refresh = True
        state.next_step = "schema_updater"
        state.reflection_notes.append(
            f"Schema mismatch detected. Retry {state.retry_count}/{state.max_retries} scheduled."
        )
    else:
        state.next_step = "finish"
        state.reflection_notes.append(
            "Error is non-retryable or retry budget exhausted; finishing run."
        )
    state.updated_at = datetime.now(timezone.utc)
    return state

