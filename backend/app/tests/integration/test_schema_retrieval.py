from app.rag.retriever import SchemaRetriever


class _Store:
    def __init__(self):
        self.docs = [
            {
                "table_name": "orders",
                "ddl": "orders order_id customer_id amount created_at",
                "columns": ["order_id", "customer_id", "amount", "created_at"],
                "indexes": ["idx_orders_customer_id"],
                "row_count": 1000,
            },
            {
                "table_name": "customers",
                "ddl": "customers customer_id segment city",
                "columns": ["customer_id", "segment", "city"],
                "indexes": ["idx_customers_segment"],
                "row_count": 100,
            },
            {
                "table_name": "payments",
                "ddl": "payments payment_id order_id method",
                "columns": ["payment_id", "order_id", "method"],
                "indexes": ["idx_payments_order_id"],
                "row_count": 1000,
            },
        ]

    def query(self, text: str, k: int = 4):
        return self.docs[:k]

    def all_docs(self):
        return self.docs


def test_schema_retrieval_returns_expected_topk() -> None:
    retriever = SchemaRetriever(_Store())
    contexts, diagnostics = retriever.retrieve_with_metadata(
        question="show customer segment revenue from orders",
        k=2,
        strategy="mmr",
        fetch_k=3,
        mmr_lambda=0.7,
    )
    assert len(contexts) == 2
    assert diagnostics["candidate_count"] == 3
    assert diagnostics["strategy"] == "mmr"
    assert "quality" in diagnostics


def test_retrieval_quality_signal_is_nonzero_for_relevant_query() -> None:
    retriever = SchemaRetriever(_Store())
    _, diagnostics = retriever.retrieve_with_metadata(
        question="order amount by customer segment",
        k=2,
        strategy="mmr",
        fetch_k=3,
        mmr_lambda=0.7,
    )
    assert diagnostics["quality"]["coverage"] > 0.0

