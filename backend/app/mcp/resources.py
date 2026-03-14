from __future__ import annotations

from typing import Any

from app.services.query_orchestrator import QueryOrchestrator


class MCPResources:
    def __init__(self, orchestrator: QueryOrchestrator) -> None:
        self.orchestrator = orchestrator

    def schema_catalog(self) -> dict[str, Any]:
        return {"uri": "schema://catalog", "data": self.orchestrator.get_schema_catalog()}

    def schema_table(self, table_name: str) -> dict[str, Any]:
        catalog = self.orchestrator.get_schema_catalog()
        table = next((doc for doc in catalog if doc.get("table_name") == table_name), None)
        return {"uri": f"schema://table/{table_name}", "data": table}

    def run_trace(self, run_id: str) -> dict[str, Any]:
        payload = self.orchestrator.get_run(run_id)
        return {"uri": f"run://{run_id}/trace", "data": payload}

