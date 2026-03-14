from __future__ import annotations

import logging
from typing import Any

from app.core.config import Settings

logger = logging.getLogger(__name__)


class MySQLClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _connect(self):
        try:
            import mysql.connector

            return mysql.connector.connect(
                host=self.settings.mysql_host,
                port=self.settings.mysql_port,
                user=self.settings.mysql_user,
                password=self.settings.mysql_password,
                database=self.settings.mysql_database,
                connection_timeout=self.settings.mysql_connect_timeout,
            )
        except Exception:
            raise

    def ping(self) -> bool:
        try:
            conn = self._connect()
            conn.close()
            return True
        except Exception as exc:
            logger.warning("MySQL ping failed: %s", exc)
            return False

    def query(self, sql: str, params: tuple[Any, ...] | None = None) -> tuple[list[str], list[dict[str, Any]]]:
        conn = self._connect()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description] if cursor.description else []
            cursor.close()
            return columns, rows
        finally:
            conn.close()

    def explain(self, sql: str) -> list[dict[str, Any]]:
        conn = self._connect()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"EXPLAIN {sql}")
            rows = cursor.fetchall()
            cursor.close()
            return rows
        finally:
            conn.close()

