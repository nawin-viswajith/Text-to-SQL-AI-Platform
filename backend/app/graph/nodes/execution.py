from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentError, AgentState, QueryResult


def _classify_error(error_text: str) -> AgentError:
    lowered = error_text.lower()
    if "unknown column" in lowered or "unknown table" in lowered:
        return AgentError(
            code="SCHEMA_MISMATCH",
            message=error_text,
            category="schema_mismatch",
            retryable=True,
        )
    if "access denied" in lowered:
        return AgentError(
            code="PERMISSION_DENIED",
            message=error_text,
            category="permission",
            retryable=False,
        )
    if "syntax" in lowered:
        return AgentError(
            code="SQL_SYNTAX",
            message=error_text,
            category="syntax",
            retryable=False,
        )
    if "timeout" in lowered:
        return AgentError(
            code="DB_TIMEOUT",
            message=error_text,
            category="timeout",
            retryable=True,
        )
    if "connect" in lowered:
        return AgentError(
            code="DB_CONNECTIVITY",
            message=error_text,
            category="connectivity",
            retryable=True,
        )
    return AgentError(
        code="DB_UNKNOWN",
        message=error_text,
        category="unknown",
        retryable=False,
    )


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    if not state.db_connected or state.mode == "generic_sql_fallback":
        state.execution_result = QueryResult(
            columns=[],
            rows=[],
            row_count=0,
            truncated=False,
            execution_ms=0,
        )
        state.next_step = "finish"
        state.reflection_notes.append(
            "Execution skipped due to missing DB connection; returning SQL-only output."
        )
        state.updated_at = datetime.now(timezone.utc)
        return state

    if not state.safe_sql:
        state.error = AgentError(
            code="MISSING_SQL",
            message="No SQL found for execution.",
            category="unknown",
            retryable=False,
        )
        state.next_step = "reflexion_analyzer"
        state.updated_at = datetime.now(timezone.utc)
        return state

    try:
        payload = deps.executor.run(state.safe_sql)
        state.explain_plan = str(payload["explain"])
        state.execution_result = QueryResult(
            columns=payload["columns"],
            rows=payload["rows"],
            row_count=payload["row_count"],
            truncated=False,
            execution_ms=payload["execution_ms"],
        )
        state.error = None
        state.reflection_notes.append("SQL executed successfully against MySQL.")
    except Exception as exc:
        state.error = _classify_error(str(exc))
        state.reflection_notes.append("SQL execution failed; entering reflexion analyzer.")

    state.next_step = "reflexion_analyzer"
    state.updated_at = datetime.now(timezone.utc)
    return state

