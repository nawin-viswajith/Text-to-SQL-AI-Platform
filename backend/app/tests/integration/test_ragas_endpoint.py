from fastapi.testclient import TestClient

from app.main import app


def test_ragas_evaluate_endpoint() -> None:
    client = TestClient(app)
    payload = {
        "question": "show top customers by revenue",
        "answer": "select customer_id, sum(amount) from orders group by customer_id",
        "contexts": ["orders table has customer_id and amount columns"],
    }
    response = client.post("/api/v1/evaluate/ragas", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "scores" in body
    assert "mode" in body

