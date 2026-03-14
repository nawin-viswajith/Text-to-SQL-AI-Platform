from __future__ import annotations

from dataclasses import dataclass

from app.core.security import SQLPolicy
from app.db.mysql_client import MySQLClient
from app.db.readonly_executor import ReadonlyExecutor
from app.observability.langsmith_client import LangSmithTracer
from app.rag.retriever import SchemaRetriever
from app.rag.schema_indexer import SchemaIndexer


@dataclass(slots=True)
class WorkflowDeps:
    mysql_client: MySQLClient
    executor: ReadonlyExecutor
    retriever: SchemaRetriever
    indexer: SchemaIndexer
    sql_policy: SQLPolicy
    tracer: LangSmithTracer

