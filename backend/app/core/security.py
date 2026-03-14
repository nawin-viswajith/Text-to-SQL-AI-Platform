from __future__ import annotations

import re


class SQLPolicyError(ValueError):
    """Raised when SQL violates platform policy."""


class SQLPolicy:
    DENYLIST = re.compile(
        r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|replace)\b",
        re.IGNORECASE,
    )
    SELECT_ONLY = re.compile(r"^\s*select\b", re.IGNORECASE)
    LIMIT_CAPTURE = re.compile(r"\blimit\s+(\d+)\b", re.IGNORECASE)

    def __init__(self, default_limit: int = 100, max_limit: int = 1000) -> None:
        self.default_limit = default_limit
        self.max_limit = max_limit

    def ensure_read_only(self, sql: str) -> str:
        normalized = sql.strip().rstrip(";")
        if not normalized:
            raise SQLPolicyError("SQL cannot be empty.")
        if self.DENYLIST.search(normalized):
            raise SQLPolicyError("Unsafe SQL operation detected by denylist policy.")
        if not self.SELECT_ONLY.match(normalized):
            raise SQLPolicyError("Only SELECT queries are allowed.")
        return normalized

    def ensure_limit(self, sql: str) -> str:
        match = self.LIMIT_CAPTURE.search(sql)
        if not match:
            return f"{sql} LIMIT {self.default_limit}"
        current_limit = int(match.group(1))
        if current_limit > self.max_limit:
            capped_sql = self.LIMIT_CAPTURE.sub(f"LIMIT {self.max_limit}", sql, count=1)
            return capped_sql
        return sql

    def validate_and_harden(self, sql: str) -> str:
        readonly_sql = self.ensure_read_only(sql)
        return self.ensure_limit(readonly_sql)

