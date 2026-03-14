from __future__ import annotations

from functools import lru_cache

from app.core.config import get_settings
from app.core.security import SQLPolicy
from app.db.mysql_client import MySQLClient
from app.db.readonly_executor import ReadonlyExecutor
from app.observability.langsmith_client import LangSmithTracer
from app.rag.chroma_client import ChromaSchemaStore
from app.rag.retriever import SchemaRetriever
from app.rag.schema_indexer import SchemaIndexer
from app.services.query_orchestrator import QueryOrchestrator
from app.services.ragas_evaluator import RagasEvaluator
from app.services.run_store import RunStore


@lru_cache(maxsize=1)
def get_orchestrator() -> QueryOrchestrator:
    settings = get_settings()
    policy = SQLPolicy(
        default_limit=settings.sql_default_limit,
        max_limit=settings.sql_max_limit,
    )
    mysql_client = MySQLClient(settings=settings)
    executor = ReadonlyExecutor(mysql_client=mysql_client, sql_policy=policy)
    chroma_store = ChromaSchemaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.chroma_collection,
    )
    retriever = SchemaRetriever(chroma_store=chroma_store)
    indexer = SchemaIndexer(mysql_client=mysql_client, chroma_store=chroma_store)
    tracer = LangSmithTracer(settings=settings)
    ragas_evaluator = RagasEvaluator(settings=settings, tracer=tracer)
    run_store = RunStore()
    return QueryOrchestrator(
        mysql_client=mysql_client,
        executor=executor,
        retriever=retriever,
        indexer=indexer,
        sql_policy=policy,
        run_store=run_store,
        tracer=tracer,
        ragas_evaluator=ragas_evaluator,
    )
