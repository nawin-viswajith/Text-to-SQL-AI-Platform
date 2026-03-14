from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Enterprise Text-to-SQL API"
    app_env: str = Field(default="dev")
    api_prefix: str = Field(default="/api/v1")

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "readonly_user"
    mysql_password: str = "readonly_password"
    mysql_database: str = "analytics"
    mysql_connect_timeout: int = 5

    sql_default_limit: int = 100
    sql_max_limit: int = 1000

    chroma_path: str = ".chroma"
    chroma_collection: str = "schema_metadata"
    rag_retrieval_k: int = 4
    rag_fetch_k: int = 12
    rag_mmr_lambda: float = 0.7

    docs_token: str = "change-me"
    api_token: str = "change-me-api-token"
    swagger_title: str = "Enterprise Text-to-SQL API"
    rbac_enabled: bool = False

    langsmith_tracing: bool = False
    langsmith_project: str = "enterprise-text2sql"
    langsmith_api_key: str | None = None
    ragas_enabled: bool = True
    ragas_use_fallback: bool = True

    @property
    def is_prod(self) -> bool:
        return self.app_env.lower() in {"prod", "production"}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    env = {
        "app_name": os.getenv("APP_NAME", "Enterprise Text-to-SQL API"),
        "app_env": os.getenv("APP_ENV", "dev"),
        "api_prefix": os.getenv("API_PREFIX", "/api/v1"),
        "mysql_host": os.getenv("MYSQL_HOST", "localhost"),
        "mysql_port": int(os.getenv("MYSQL_PORT", "3306")),
        "mysql_user": os.getenv("MYSQL_USER", "readonly_user"),
        "mysql_password": os.getenv("MYSQL_PASSWORD", "readonly_password"),
        "mysql_database": os.getenv("MYSQL_DATABASE", "analytics"),
        "mysql_connect_timeout": int(os.getenv("MYSQL_CONNECT_TIMEOUT", "5")),
        "sql_default_limit": int(os.getenv("SQL_DEFAULT_LIMIT", "100")),
        "sql_max_limit": int(os.getenv("SQL_MAX_LIMIT", "1000")),
        "chroma_path": os.getenv("CHROMA_PATH", ".chroma"),
        "chroma_collection": os.getenv("CHROMA_COLLECTION", "schema_metadata"),
        "rag_retrieval_k": int(os.getenv("RAG_RETRIEVAL_K", "4")),
        "rag_fetch_k": int(os.getenv("RAG_FETCH_K", "12")),
        "rag_mmr_lambda": float(os.getenv("RAG_MMR_LAMBDA", "0.7")),
        "docs_token": os.getenv("DOCS_TOKEN", "change-me"),
        "api_token": os.getenv("API_TOKEN", "change-me-api-token"),
        "swagger_title": os.getenv("SWAGGER_TITLE", "Enterprise Text-to-SQL API"),
        "rbac_enabled": os.getenv("RBAC_ENABLED", "false").lower() == "true",
        "langsmith_tracing": os.getenv("LANGSMITH_TRACING", "false").lower() == "true",
        "langsmith_project": os.getenv("LANGSMITH_PROJECT", "enterprise-text2sql"),
        "langsmith_api_key": os.getenv("LANGSMITH_API_KEY"),
        "ragas_enabled": os.getenv("RAGAS_ENABLED", "true").lower() == "true",
        "ragas_use_fallback": os.getenv("RAGAS_USE_FALLBACK", "true").lower() == "true",
    }
    return Settings(**env)
