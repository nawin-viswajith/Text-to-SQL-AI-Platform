from __future__ import annotations

from app.rag.chroma_client import ChromaSchemaStore
from app.schemas.domain_models import TableContext


class SchemaRetriever:
    def __init__(self, chroma_store: ChromaSchemaStore) -> None:
        self.chroma_store = chroma_store

    def retrieve(self, question: str, k: int = 4) -> list[TableContext]:
        docs = self.chroma_store.query(question, k=k)
        return [TableContext(**doc, source="chroma") for doc in docs]

    def catalog(self) -> list[dict]:
        return self.chroma_store.all_docs()

