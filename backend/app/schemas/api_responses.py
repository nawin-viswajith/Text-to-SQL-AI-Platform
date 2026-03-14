from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    run_id: str
    session_id: str
    status: str
    question: str
    safe_sql: str | None = None
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    retries_used: int = 0
    reflection_notes: list[str] = Field(default_factory=list)
    events: list[dict[str, Any]] = Field(default_factory=list)
    retrieval_diagnostics: dict[str, Any] = Field(default_factory=dict)
    ragas_scores: dict[str, float] | None = None


class RunResponse(BaseModel):
    run_id: str
    payload: dict[str, Any]


class SchemaRefreshResponse(BaseModel):
    refreshed: bool
    tables_updated: int
    updated_at: datetime


class HealthResponse(BaseModel):
    status: str
    app_env: str


class RagasEvaluationResponse(BaseModel):
    scores: dict[str, float]
    mode: str
