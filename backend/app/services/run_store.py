from __future__ import annotations

from threading import Lock
from typing import Any


class RunStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._runs: dict[str, dict[str, Any]] = {}

    def save(self, run_id: str, payload: dict[str, Any]) -> None:
        with self._lock:
            self._runs[run_id] = payload

    def get(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            return self._runs.get(run_id)

