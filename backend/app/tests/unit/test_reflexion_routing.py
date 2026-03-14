from datetime import datetime, timezone

from app.graph.nodes.reflexion_analyzer import run
from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentError, AgentState


class _NoOp:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None


def _deps() -> WorkflowDeps:
    return WorkflowDeps(
        mysql_client=_NoOp(),
        executor=_NoOp(),
        retriever=_NoOp(),
        indexer=_NoOp(),
        sql_policy=_NoOp(),
        tracer=_NoOp(),
    )


def _base_state() -> AgentState:
    now = datetime.now(timezone.utc)
    return AgentState(
        run_id="r1",
        session_id="s1",
        question="test",
        started_at=now,
        updated_at=now,
    )


def test_schema_mismatch_retries() -> None:
    state = _base_state()
    state.max_retries = 2
    state.retry_count = 0
    state.error = AgentError(
        code="SCHEMA_MISMATCH",
        message="Unknown column x",
        category="schema_mismatch",
        retryable=True,
    )
    state = run(state, _deps())
    assert state.next_step == "schema_updater"
    assert state.retry_count == 1
    assert state.needs_schema_refresh is True


def test_non_retryable_finishes() -> None:
    state = _base_state()
    state.error = AgentError(
        code="PERM",
        message="Access denied",
        category="permission",
        retryable=False,
    )
    state = run(state, _deps())
    assert state.next_step == "finish"

