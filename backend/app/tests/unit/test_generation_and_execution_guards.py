from datetime import datetime, timezone

from app.core.security import SQLPolicy
from app.graph.nodes import execution as execution_node
from app.graph.nodes import sql_generation as generation_node
from app.graph.nodes import sql_safety_validate as validate_node
from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState, TableContext


class _NoOp:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class _Executor:
    def run(self, sql: str):
        return {
            "safe_sql": sql,
            "explain": [{"id": 1, "select_type": "SIMPLE"}],
            "columns": ["id"],
            "rows": [{"id": 1}],
            "row_count": 1,
            "execution_ms": 10,
        }


def _state() -> AgentState:
    now = datetime.now(timezone.utc)
    return AgentState(
        run_id="r1",
        session_id="s1",
        question="show orders",
        db_connected=True,
        started_at=now,
        updated_at=now,
    )


def test_generation_then_validation_creates_safe_sql() -> None:
    state = _state()
    state.rag_context = [
        TableContext(
            table_name="orders",
            ddl="CREATE TABLE orders (...)",
            columns=["id", "amount"],
            indexes=[],
            row_count=10,
        )
    ]
    deps = WorkflowDeps(
        mysql_client=_NoOp(),
        executor=_NoOp(),
        retriever=_NoOp(),
        indexer=_NoOp(),
        sql_policy=SQLPolicy(default_limit=100, max_limit=1000),
        tracer=_NoOp(),
    )

    state = generation_node.run(state, deps)
    state = validate_node.run(state, deps)

    assert state.safe_sql is not None
    assert state.safe_sql.lower().startswith("select")
    assert "limit" in state.safe_sql.lower()


def test_execution_returns_rows_when_executor_succeeds() -> None:
    state = _state()
    state.safe_sql = "SELECT id FROM `orders` LIMIT 10"
    deps = WorkflowDeps(
        mysql_client=_NoOp(),
        executor=_Executor(),
        retriever=_NoOp(),
        indexer=_NoOp(),
        sql_policy=SQLPolicy(default_limit=100, max_limit=1000),
        tracer=_NoOp(),
    )

    state = execution_node.run(state, deps)
    assert state.error is None
    assert state.execution_result is not None
    assert state.execution_result.row_count == 1

