from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    session_id: str = Field(min_length=1, max_length=128)
    user_id: str | None = Field(default=None, max_length=128)
    connection_id: str | None = Field(default=None, max_length=128)
    max_retries: int = Field(default=2, ge=0, le=5)
    retrieval_strategy: Literal["mmr", "similarity"] = "mmr"
    retrieval_fetch_k: int = Field(default=12, ge=4, le=50)
    mmr_lambda: float = Field(default=0.7, ge=0.0, le=1.0)
    run_ragas: bool = False
    reference_answer: str | None = Field(default=None, max_length=6000)


class SchemaRefreshRequest(BaseModel):
    table_names: list[str] | None = None


class MCPToolRequest(BaseModel):
    tool_input: dict = Field(default_factory=dict)


class RagasEvaluationRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    answer: str = Field(min_length=1, max_length=12000)
    contexts: list[str] = Field(default_factory=list)
    reference_answer: str | None = Field(default=None, max_length=12000)
    trace_id: str | None = Field(default=None, max_length=128)
