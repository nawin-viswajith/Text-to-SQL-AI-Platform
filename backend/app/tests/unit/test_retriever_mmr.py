from app.rag.retriever import SchemaRetriever


class _Store:
    def __init__(self, docs):
        self.docs = docs

    def query(self, text: str, k: int = 4):
        return self.docs[:k]

    def all_docs(self):
        return self.docs


def test_retrieve_with_mmr_returns_requested_k() -> None:
    docs = [
        {"table_name": "orders", "ddl": "orders amount created_at", "columns": ["amount", "created_at"], "indexes": [], "row_count": 100},
        {"table_name": "customers", "ddl": "customers id segment", "columns": ["id", "segment"], "indexes": [], "row_count": 50},
        {"table_name": "products", "ddl": "products id category", "columns": ["id", "category"], "indexes": [], "row_count": 40},
        {"table_name": "payments", "ddl": "payments order_id method", "columns": ["order_id", "method"], "indexes": [], "row_count": 25},
    ]
    retriever = SchemaRetriever(chroma_store=_Store(docs))
    contexts, diagnostics = retriever.retrieve_with_metadata(
        question="show order amount by customer segment",
        k=2,
        strategy="mmr",
        fetch_k=4,
        mmr_lambda=0.7,
    )
    assert len(contexts) == 2
    assert diagnostics["strategy"] == "mmr"
    assert len(diagnostics["selected_tables"]) == 2


def test_similarity_strategy_uses_top_order() -> None:
    docs = [
        {"table_name": "t1", "ddl": "a", "columns": [], "indexes": [], "row_count": 1},
        {"table_name": "t2", "ddl": "b", "columns": [], "indexes": [], "row_count": 1},
    ]
    retriever = SchemaRetriever(chroma_store=_Store(docs))
    contexts, diagnostics = retriever.retrieve_with_metadata(
        question="anything",
        k=1,
        strategy="similarity",
        fetch_k=4,
        mmr_lambda=0.7,
    )
    assert contexts[0].table_name == "t1"
    assert diagnostics["strategy"] == "similarity"

