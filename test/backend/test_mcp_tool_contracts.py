from fastapi.testclient import TestClient

from app.main import app


def test_mcp_catalog_contract() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/mcp/tools/get_table_catalog", json={"tool_input": {}})
    assert response.status_code == 200
    body = response.json()
    assert body.get("tool") == "get_table_catalog"
    assert "tables" in body.get("result", {})


def test_mcp_ragas_contract() -> None:
    client = TestClient(app)
    payload = {
        "tool_input": {
            "question": "show top customers by revenue",
            "answer": "select customer_id, sum(amount) from orders group by customer_id",
            "contexts": ["orders table has customer_id and amount columns"],
        }
    }
    response = client.post("/api/v1/mcp/tools/evaluate_ragas", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body.get("tool") == "evaluate_ragas"
    assert "scores" in body.get("result", {})

