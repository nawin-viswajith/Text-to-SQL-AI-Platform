from __future__ import annotations

from typing import Any

from app.rag.chroma_client import ChromaSchemaStore
from app.schemas.domain_models import TableContext


class SchemaRetriever:
    def __init__(self, chroma_store: ChromaSchemaStore) -> None:
        self.chroma_store = chroma_store

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {token.lower() for token in text.split() if token.strip()}

    @staticmethod
    def _doc_text(doc: dict[str, Any]) -> str:
        return " ".join(
            [
                str(doc.get("table_name", "")),
                " ".join(doc.get("columns", [])),
                " ".join(doc.get("indexes", [])),
                str(doc.get("ddl", "")),
            ]
        )

    def _similarity(self, text_a: str, text_b: str) -> float:
        tokens_a = self._tokenize(text_a)
        tokens_b = self._tokenize(text_b)
        if not tokens_a or not tokens_b:
            return 0.0
        overlap = len(tokens_a.intersection(tokens_b))
        denom = len(tokens_a.union(tokens_b))
        return overlap / denom if denom else 0.0

    def _mmr_select(
        self,
        question: str,
        candidates: list[dict[str, Any]],
        k: int,
        lambda_mult: float,
    ) -> list[dict[str, Any]]:
        selected: list[dict[str, Any]] = []
        remaining = list(candidates)
        while remaining and len(selected) < k:
            best_doc = None
            best_score = float("-inf")
            for candidate in remaining:
                relevance = self._similarity(question, self._doc_text(candidate))
                diversity_penalty = 0.0
                if selected:
                    diversity_penalty = max(
                        self._similarity(
                            self._doc_text(candidate),
                            self._doc_text(chosen),
                        )
                        for chosen in selected
                    )
                mmr_score = (lambda_mult * relevance) - ((1 - lambda_mult) * diversity_penalty)
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_doc = candidate
            if best_doc is None:
                break
            selected.append(best_doc)
            remaining = [doc for doc in remaining if doc.get("table_name") != best_doc.get("table_name")]
        return selected

    def retrieve_with_metadata(
        self,
        question: str,
        k: int = 4,
        strategy: str = "mmr",
        fetch_k: int = 12,
        mmr_lambda: float = 0.7,
    ) -> tuple[list[TableContext], dict[str, Any]]:
        candidates = self.chroma_store.query(question, k=max(fetch_k, k))
        if strategy == "similarity":
            selected = candidates[:k]
        else:
            selected = self._mmr_select(
                question=question,
                candidates=candidates,
                k=k,
                lambda_mult=mmr_lambda,
            )
        contexts = [TableContext(**doc, source="chroma") for doc in selected]
        diagnostics = {
            "strategy": strategy,
            "requested_k": k,
            "fetch_k": max(fetch_k, k),
            "mmr_lambda": mmr_lambda,
            "candidate_count": len(candidates),
            "selected_tables": [ctx.table_name for ctx in contexts],
        }
        return contexts, diagnostics

    def retrieve(
        self,
        question: str,
        k: int = 4,
        strategy: str = "mmr",
        fetch_k: int = 12,
        mmr_lambda: float = 0.7,
    ) -> list[TableContext]:
        contexts, _ = self.retrieve_with_metadata(
            question=question,
            k=k,
            strategy=strategy,
            fetch_k=fetch_k,
            mmr_lambda=mmr_lambda,
        )
        return contexts

    def catalog(self) -> list[dict]:
        return self.chroma_store.all_docs()
