from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ChromaSchemaStore:
    def __init__(self, persist_path: str, collection_name: str) -> None:
        self.persist_path = Path(persist_path)
        self.collection_name = collection_name
        self.persist_path.mkdir(parents=True, exist_ok=True)
        self._memory_docs: dict[str, dict[str, Any]] = {}
        self._collection = None
        try:
            import chromadb

            client = chromadb.PersistentClient(path=str(self.persist_path))
            self._collection = client.get_or_create_collection(name=collection_name)
        except Exception:
            self._collection = None

    def upsert(self, docs: list[dict[str, Any]]) -> int:
        if not docs:
            return 0

        if self._collection is not None:
            ids = [doc["table_name"] for doc in docs]
            documents = [json.dumps(doc) for doc in docs]
            metadatas = [
                {
                    "table_name": doc["table_name"],
                    "row_count": int(doc.get("row_count") or 0),
                }
                for doc in docs
            ]
            self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            return len(docs)

        for doc in docs:
            self._memory_docs[doc["table_name"]] = doc
        return len(docs)

    def query(self, text: str, k: int = 4) -> list[dict[str, Any]]:
        if self._collection is not None:
            results = self._collection.query(query_texts=[text], n_results=k)
            docs = results.get("documents", [[]])[0]
            return [json.loads(d) for d in docs]

        tokens = {token.lower() for token in text.split() if token.strip()}

        def score(doc: dict[str, Any]) -> int:
            hay = " ".join(
                [
                    doc.get("table_name", ""),
                    " ".join(doc.get("columns", [])),
                    doc.get("ddl", ""),
                ]
            ).lower()
            return sum(1 for t in tokens if t in hay)

        ranked = sorted(self._memory_docs.values(), key=score, reverse=True)
        return ranked[:k]

    def all_docs(self) -> list[dict[str, Any]]:
        if self._collection is not None:
            raw = self._collection.get()
            return [json.loads(item) for item in raw.get("documents", [])]
        return list(self._memory_docs.values())

