from __future__ import annotations

import time
from typing import Any

from app.core.security import SQLPolicy
from app.db.mysql_client import MySQLClient


class ReadonlyExecutor:
    def __init__(self, mysql_client: MySQLClient, sql_policy: SQLPolicy) -> None:
        self.mysql_client = mysql_client
        self.sql_policy = sql_policy

    def run(self, sql: str) -> dict[str, Any]:
        safe_sql = self.sql_policy.validate_and_harden(sql)
        explain_rows = self.mysql_client.explain(safe_sql)
        start = time.perf_counter()
        columns, rows = self.mysql_client.query(safe_sql)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "safe_sql": safe_sql,
            "explain": explain_rows,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "execution_ms": elapsed_ms,
        }

