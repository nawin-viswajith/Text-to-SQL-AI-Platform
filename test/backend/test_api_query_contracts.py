from fastapi.testclient import TestClient

from app.main import app


def test_query_contract_includes_diagnostics_and_events() -> None:
    client = TestClient(app)
    payload = {
        "question": "show order totals",
        "session_id": "contract-test",
        "retrieval_strategy": "mmr",
        "run_ragas": True,
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "events" in body
    assert "retrieval_diagnostics" in body
    assert "ragas_scores" in body

