from __future__ import annotations

from typing import Any

from app.db.mysql_client import MySQLClient


class MySQLIntrospector:
    def __init__(self, mysql_client: MySQLClient) -> None:
        self.mysql_client = mysql_client

    def list_tables(self) -> list[str]:
        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
        ORDER BY table_name
        """
        _, rows = self.mysql_client.query(sql)
        return [row["table_name"] for row in rows]

    def get_columns(self, table_name: str) -> list[str]:
        sql = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = %s
        ORDER BY ordinal_position
        """
        _, rows = self.mysql_client.query(sql, (table_name,))
        return [row["column_name"] for row in rows]

    def get_indexes(self, table_name: str) -> list[str]:
        sql = """
        SELECT index_name
        FROM information_schema.statistics
        WHERE table_schema = DATABASE() AND table_name = %s
        GROUP BY index_name
        ORDER BY index_name
        """
        _, rows = self.mysql_client.query(sql, (table_name,))
        return [row["index_name"] for row in rows]

    def get_row_count(self, table_name: str) -> int | None:
        sql = """
        SELECT table_rows
        FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = %s
        """
        _, rows = self.mysql_client.query(sql, (table_name,))
        if not rows:
            return None
        return int(rows[0]["table_rows"] or 0)

    def get_ddl(self, table_name: str) -> str:
        sql = f"SHOW CREATE TABLE `{table_name}`"
        _, rows = self.mysql_client.query(sql)
        if not rows:
            return f"CREATE TABLE {table_name} (...)"
        return rows[0].get("Create Table", f"CREATE TABLE {table_name} (...)")

    def snapshot_tables(self, table_names: list[str] | None = None) -> list[dict[str, Any]]:
        names = table_names or self.list_tables()
        docs: list[dict[str, Any]] = []
        for table_name in names:
            docs.append(
                {
                    "table_name": table_name,
                    "ddl": self.get_ddl(table_name),
                    "columns": self.get_columns(table_name),
                    "indexes": self.get_indexes(table_name),
                    "row_count": self.get_row_count(table_name),
                }
            )
        return docs

