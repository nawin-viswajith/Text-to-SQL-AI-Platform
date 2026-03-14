from fastapi.testclient import TestClient

from app.main import app


def test_mcp_tool_contract_get_table_catalog() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/mcp/tools/get_table_catalog", json={"tool_input": {}})
    assert response.status_code == 200
    body = response.json()
    assert body["tool"] == "get_table_catalog"
    assert "result" in body
    assert "tables" in body["result"]


def test_mcp_tool_contract_evaluate_ragas() -> None:
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
    assert body["tool"] == "evaluate_ragas"
    assert "scores" in body["result"]
    assert "mode" in body["result"]

