from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Generator

from app.core.security import SQLPolicy
from app.db.mysql_client import MySQLClient
from app.db.readonly_executor import ReadonlyExecutor
from app.graph.types import WorkflowDeps
from app.graph.workflow import ReflexionWorkflow
from app.observability.langsmith_client import LangSmithTracer
from app.rag.retriever import SchemaRetriever
from app.rag.schema_indexer import SchemaIndexer
from app.schemas.api_requests import QueryRequest
from app.schemas.api_responses import QueryResponse, RagasEvaluationResponse, SchemaRefreshResponse
from app.schemas.domain_models import AgentState
from app.services.ragas_evaluator import RagasEvaluator
from app.services.run_store import RunStore


class QueryOrchestrator:
    def __init__(
        self,
        mysql_client: MySQLClient,
        executor: ReadonlyExecutor,
        retriever: SchemaRetriever,
        indexer: SchemaIndexer,
        sql_policy: SQLPolicy,
        run_store: RunStore,
        tracer: LangSmithTracer,
        ragas_evaluator: RagasEvaluator,
    ) -> None:
        self.mysql_client = mysql_client
        self.executor = executor
        self.retriever = retriever
        self.indexer = indexer
        self.sql_policy = sql_policy
        self.run_store = run_store
        self.tracer = tracer
        self.ragas_evaluator = ragas_evaluator
        self.workflow = ReflexionWorkflow(
            deps=WorkflowDeps(
                mysql_client=mysql_client,
                executor=executor,
                retriever=retriever,
                indexer=indexer,
                sql_policy=sql_policy,
                tracer=tracer,
            )
        )

    def _new_state(self, request: QueryRequest) -> AgentState:
        now = datetime.now(timezone.utc)
        run_id = str(uuid.uuid4())
        state = AgentState(
            run_id=run_id,
            session_id=request.session_id,
            user_id=request.user_id,
            question=request.question,
            db_connected=False,
            connection_id=request.connection_id,
            max_retries=request.max_retries,
            retrieval_strategy=request.retrieval_strategy,
            retrieval_fetch_k=request.retrieval_fetch_k,
            mmr_lambda=request.mmr_lambda,
            started_at=now,
            updated_at=now,
        )
        state.langsmith_trace_id = self.tracer.start_trace(
            state_id=state.run_id,
            payload={"session_id": state.session_id, "question": state.question},
        )
        return state

    def run_query(self, request: QueryRequest) -> QueryResponse:
        state = self._new_state(request)
        final_state, events = self.workflow.run(state)
        ragas_result = {"mode": "disabled", "scores": {}}
        if request.run_ragas:
            ragas_result = self.ragas_evaluator.evaluate(
                question=final_state.question,
                answer=final_state.safe_sql or "",
                contexts=[ctx.ddl for ctx in final_state.rag_context],
                reference_answer=request.reference_answer,
                trace_id=final_state.langsmith_trace_id,
            )
            final_state.ragas_scores = ragas_result["scores"]
        payload = {
            "state": final_state.model_dump(mode="json"),
            "events": events,
            "ragas": ragas_result,
        }
        self.run_store.save(final_state.run_id, payload)
        self.tracer.end_trace(
            trace_id=final_state.langsmith_trace_id,
            payload={"status": "done", "error": final_state.error.model_dump() if final_state.error else None},
        )
        return QueryResponse(
            run_id=final_state.run_id,
            session_id=final_state.session_id,
            status="success" if final_state.error is None else "error",
            question=final_state.question,
            safe_sql=final_state.safe_sql,
            result=final_state.execution_result.model_dump() if final_state.execution_result else None,
            error=final_state.error.model_dump() if final_state.error else None,
            retries_used=final_state.retry_count,
            reflection_notes=final_state.reflection_notes,
            events=events,
            retrieval_diagnostics=final_state.retrieval_diagnostics,
            ragas_scores=final_state.ragas_scores,
        )

    def stream_query(self, request: QueryRequest) -> Generator[str, None, None]:
        state = self._new_state(request)
        last_state = state
        events: list[dict[str, Any]] = []
        for _, event, current_state in self.workflow.stream(state):
            events.append(event)
            last_state = current_state
            yield f"data: {json.dumps({'type': 'event', 'payload': event})}\n\n"

        payload = {
            "state": last_state.model_dump(mode="json"),
            "events": events,
        }
        ragas_result = {"mode": "disabled", "scores": {}}
        if request.run_ragas:
            ragas_result = self.ragas_evaluator.evaluate(
                question=last_state.question,
                answer=last_state.safe_sql or "",
                contexts=[ctx.ddl for ctx in last_state.rag_context],
                reference_answer=request.reference_answer,
                trace_id=last_state.langsmith_trace_id,
            )
            last_state.ragas_scores = ragas_result["scores"]
            payload["ragas"] = ragas_result
        self.run_store.save(last_state.run_id, payload)
        self.tracer.end_trace(
            trace_id=last_state.langsmith_trace_id,
            payload={"status": "done", "error": last_state.error.model_dump() if last_state.error else None},
        )
        final_payload = {
            "type": "final",
            "payload": {
                "run_id": last_state.run_id,
                "status": "success" if last_state.error is None else "error",
                "safe_sql": last_state.safe_sql,
                "error": last_state.error.model_dump() if last_state.error else None,
                "result": last_state.execution_result.model_dump()
                if last_state.execution_result
                else None,
                "retrieval_diagnostics": last_state.retrieval_diagnostics,
                "ragas_scores": last_state.ragas_scores,
            },
        }
        yield f"data: {json.dumps(final_payload)}\n\n"

    def refresh_schema_index(self, table_names: list[str] | None = None) -> SchemaRefreshResponse:
        updated = self.indexer.refresh(table_names=table_names)
        return SchemaRefreshResponse(
            refreshed=True,
            tables_updated=updated,
            updated_at=datetime.now(timezone.utc),
        )

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        return self.run_store.get(run_id)

    def generate_sql(self, question: str, session_id: str = "mcp-session") -> dict[str, Any]:
        request = QueryRequest(question=question, session_id=session_id, max_retries=0)
        response = self.run_query(request)
        return {
            "run_id": response.run_id,
            "safe_sql": response.safe_sql,
            "status": response.status,
            "error": response.error,
        }

    def execute_sql(self, sql: str) -> dict[str, Any]:
        return self.executor.run(sql=sql)

    def get_schema_catalog(self) -> list[dict[str, Any]]:
        return self.retriever.catalog()

    def evaluate_ragas(
        self,
        question: str,
        answer: str,
        contexts: list[str],
        reference_answer: str | None = None,
        trace_id: str | None = None,
    ) -> RagasEvaluationResponse:
        result = self.ragas_evaluator.evaluate(
            question=question,
            answer=answer,
            contexts=contexts,
            reference_answer=reference_answer,
            trace_id=trace_id,
        )
        return RagasEvaluationResponse(scores=result["scores"], mode=result["mode"])
