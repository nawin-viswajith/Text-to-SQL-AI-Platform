from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from app.graph.nodes import (
    context_check,
    execution,
    finalize,
    rag_schema_retrieval,
    reflexion_analyzer,
    schema_updater,
    sql_generation,
    sql_safety_validate,
)
from app.graph.types import WorkflowDeps
from app.schemas.domain_models import AgentState

NodeFunc = Callable[[AgentState, WorkflowDeps], AgentState]


class ReflexionWorkflow:
    """LangGraph-style finite state workflow with deterministic routing."""

    MAX_NODE_STEPS = 30

    def __init__(self, deps: WorkflowDeps) -> None:
        self.deps = deps
        self.nodes: dict[str, NodeFunc] = {
            "context_check": context_check.run,
            "rag_retrieval": rag_schema_retrieval.run,
            "sql_generation": sql_generation.run,
            "sql_safety_validate": sql_safety_validate.run,
            "execution": execution.run,
            "reflexion_analyzer": reflexion_analyzer.run,
            "schema_updater": schema_updater.run,
        }
        self.compiled_graph = self._build_langgraph()

    def _build_langgraph(self):
        try:
            from langgraph.graph import END, StateGraph
        except Exception:
            return None

        graph = StateGraph(AgentState)
        for name, fn in self.nodes.items():
            graph.add_node(name, lambda state, fn=fn: fn(state, self.deps))
        graph.set_entry_point("context_check")

        route_map = {
            "context_check": "context_check",
            "rag_retrieval": "rag_retrieval",
            "sql_generation": "sql_generation",
            "sql_safety_validate": "sql_safety_validate",
            "execution": "execution",
            "reflexion_analyzer": "reflexion_analyzer",
            "schema_updater": "schema_updater",
            "finish": END,
        }
        for name in self.nodes:
            graph.add_conditional_edges(
                name,
                lambda state: state.next_step or "finish",
                route_map,
            )
        return graph.compile()

    def _event(self, node: str, state: AgentState) -> dict:
        return {
            "node": node,
            "at": datetime.now(timezone.utc).isoformat(),
            "retry_count": state.retry_count,
            "has_error": state.error is not None,
            "error_category": state.error.category if state.error else None,
            "next_step": state.next_step,
        }

    def run(self, initial_state: AgentState) -> tuple[AgentState, list[dict]]:
        state = initial_state
        state.next_step = state.next_step or "context_check"
        events: list[dict] = []
        for _ in range(self.MAX_NODE_STEPS):
            if state.next_step in (None, "finish"):
                break
            node_name = state.next_step
            node = self.nodes[node_name]
            state = node(state, self.deps)
            events.append(self._event(node_name, state))
            self.deps.tracer.log_event(
                trace_id=state.langsmith_trace_id,
                node=node_name,
                payload=events[-1],
            )

        state = finalize.run(state, self.deps)
        events.append(self._event("finalize", state))
        return state, events

    def stream(self, initial_state: AgentState):
        state = initial_state
        state.next_step = state.next_step or "context_check"
        for _ in range(self.MAX_NODE_STEPS):
            if state.next_step in (None, "finish"):
                break
            node_name = state.next_step
            state = self.nodes[node_name](state, self.deps)
            event = self._event(node_name, state)
            self.deps.tracer.log_event(
                trace_id=state.langsmith_trace_id,
                node=node_name,
                payload=event,
            )
            yield ("event", event, state)

        state = finalize.run(state, self.deps)
        yield ("event", self._event("finalize", state), state)
