from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.main import app  # noqa: E402


def run() -> int:
    client = TestClient(app)

    checks = [
        ("health", client.get("/api/v1/health")),
        (
            "query",
            client.post(
                "/api/v1/query",
                json={
                    "question": "show order totals",
                    "session_id": "smoke-session",
                    "run_ragas": True,
                },
            ),
        ),
        (
            "mcp_catalog",
            client.post("/api/v1/mcp/tools/get_table_catalog", json={"tool_input": {}}),
        ),
    ]

    failed = []
    for name, response in checks:
        if response.status_code != 200:
            failed.append((name, response.status_code))

    if failed:
        print("Smoke failed:", failed)
        return 1
    print("Smoke passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

