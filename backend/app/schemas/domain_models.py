from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class TableContext(BaseModel):
    table_name: str
    ddl: str
    columns: list[str] = Field(default_factory=list)
    indexes: list[str] = Field(default_factory=list)
    row_count: int | None = None
    source: Literal["chroma", "mysql_live"] = "chroma"


class QueryResult(BaseModel):
    columns: list[str] = Field(default_factory=list)
    rows: list[dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    truncated: bool = False
    execution_ms: int | None = None


class AgentError(BaseModel):
    code: str | None = None
    message: str
    category: Literal[
        "schema_mismatch",
        "syntax",
        "permission",
        "connectivity",
        "timeout",
        "unknown",
    ] = "unknown"
    retryable: bool = False


class AgentState(BaseModel):
    run_id: str
    session_id: str
    user_id: str | None = None
    question: str

    db_connected: bool = False
    connection_id: str | None = None
    mode: Literal["connected", "generic_sql_fallback"] = "connected"

    rag_context: list[TableContext] = Field(default_factory=list)
    retrieval_strategy: Literal["mmr", "similarity"] = "mmr"
    retrieval_fetch_k: int = 12
    mmr_lambda: float = 0.7
    retrieval_diagnostics: dict[str, Any] = Field(default_factory=dict)
    candidate_sql: str | None = None
    safe_sql: str | None = None
    explain_plan: str | None = None

    execution_result: QueryResult | None = None
    error: AgentError | None = None
    reflection_notes: list[str] = Field(default_factory=list)

    needs_schema_refresh: bool = False
    retry_count: int = 0
    max_retries: int = 2
    next_step: Literal[
        "context_check",
        "rag_retrieval",
        "sql_generation",
        "sql_safety_validate",
        "execution",
        "reflexion_analyzer",
        "schema_updater",
        "finish",
        "ask_user",
    ] | None = None

    langsmith_trace_id: str | None = None
    ragas_scores: dict[str, float] | None = None
    started_at: datetime
    updated_at: datetime
