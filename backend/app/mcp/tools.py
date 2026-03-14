from __future__ import annotations

from typing import Any

from app.services.query_orchestrator import QueryOrchestrator


class MCPTools:
    def __init__(self, orchestrator: QueryOrchestrator) -> None:
        self.orchestrator = orchestrator

    def generate_sql(self, payload: dict[str, Any]) -> dict[str, Any]:
        question = payload.get("question", "")
        session_id = payload.get("session_id", "mcp-session")
        return self.orchestrator.generate_sql(question=question, session_id=session_id)

    def execute_readonly_sql(self, payload: dict[str, Any]) -> dict[str, Any]:
        sql = payload.get("sql", "")
        return self.orchestrator.execute_sql(sql=sql)

    def refresh_schema_index(self, payload: dict[str, Any]) -> dict[str, Any]:
        table_names = payload.get("table_names")
        response = self.orchestrator.refresh_schema_index(table_names=table_names)
        return response.model_dump(mode="json")

    def get_table_catalog(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tables": self.orchestrator.get_schema_catalog()}

