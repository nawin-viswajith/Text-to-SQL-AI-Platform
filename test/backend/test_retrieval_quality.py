from app.rag.retriever import SchemaRetriever


class _Store:
    def query(self, text: str, k: int = 4):
        return [
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
        ][:k]

    def all_docs(self):
        return []


def test_mmr_quality_metrics_are_present() -> None:
    retriever = SchemaRetriever(_Store())
    _, diagnostics = retriever.retrieve_with_metadata(
        question="order amount by customer segment",
        k=2,
        strategy="mmr",
        fetch_k=3,
        mmr_lambda=0.7,
    )
    quality = diagnostics.get("quality", {})
    assert "avg_relevance" in quality
    assert "diversity" in quality
    assert "coverage" in quality

