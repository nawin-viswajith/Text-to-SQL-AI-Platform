from __future__ import annotations

from datetime import datetime, timezone

from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState


def _heuristic_sql(question: str, table_name: str, columns: list[str]) -> str:
    q = question.lower()
    if "count" in q or "how many" in q:
        return f"SELECT COUNT(*) AS total_count FROM `{table_name}`"
    select_cols = columns[:5] if columns else ["*"]
    select_clause = ", ".join(f"`{col}`" for col in select_cols) if select_cols != ["*"] else "*"
    return f"SELECT {select_clause} FROM `{table_name}`"


def run(state: AgentState, deps: WorkflowDeps) -> AgentState:
    if state.mode == "generic_sql_fallback":
        state.candidate_sql = "SELECT * FROM `your_table`"
        state.reflection_notes.append(
            "Generic SQL generated because DB context is unavailable."
        )
    elif state.rag_context:
        top = state.rag_context[0]
        state.candidate_sql = _heuristic_sql(
            question=state.question,
            table_name=top.table_name,
            columns=top.columns,
        )
        state.reflection_notes.append(
            f"SQL generated using schema context from table `{top.table_name}`."
        )
    else:
        state.candidate_sql = "SELECT 1 AS health_check"
        state.reflection_notes.append("Fallback SQL generated due to empty schema retrieval.")
    state.next_step = "sql_safety_validate"
    state.updated_at = datetime.now(timezone.utc)
    return state

