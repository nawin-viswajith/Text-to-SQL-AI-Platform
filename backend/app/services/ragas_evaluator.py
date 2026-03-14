from __future__ import annotations

from typing import Any

from app.core.config import Settings
from app.observability.langsmith_client import LangSmithTracer


class RagasEvaluator:
    def __init__(self, settings: Settings, tracer: LangSmithTracer) -> None:
        self.settings = settings
        self.tracer = tracer
        self.enabled = settings.ragas_enabled
        self.use_fallback = settings.ragas_use_fallback

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {token.lower() for token in text.split() if token.strip()}

    def _fallback_scores(
        self,
        question: str,
        answer: str,
        contexts: list[str],
        reference_answer: str | None,
    ) -> dict[str, float]:
        context_blob = " ".join(contexts)
        q_tokens = self._tokenize(question)
        a_tokens = self._tokenize(answer)
        c_tokens = self._tokenize(context_blob)
        r_tokens = self._tokenize(reference_answer or "")

        def overlap_ratio(a: set[str], b: set[str]) -> float:
            if not a:
                return 0.0
            return len(a.intersection(b)) / len(a)

        scores = {
            "context_relevance": round(overlap_ratio(q_tokens, c_tokens), 4),
            "answer_groundedness": round(overlap_ratio(a_tokens, c_tokens), 4),
            "answer_relevance": round(overlap_ratio(q_tokens, a_tokens), 4),
        }
        if reference_answer:
            scores["reference_alignment"] = round(overlap_ratio(a_tokens, r_tokens), 4)
        return scores

    def evaluate(
        self,
        question: str,
        answer: str,
        contexts: list[str],
        reference_answer: str | None = None,
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        if not self.enabled:
            return {"mode": "disabled", "scores": {}}

        try:
            from datasets import Dataset
            from ragas import evaluate
            from ragas.metrics import answer_relevancy, faithfulness

            data = {
                "question": [question],
                "answer": [answer],
                "contexts": [contexts],
            }
            metrics = [answer_relevancy, faithfulness]
            if reference_answer:
                from ragas.metrics import answer_correctness

                data["ground_truth"] = [reference_answer]
                metrics.append(answer_correctness)

            dataset = Dataset.from_dict(data)
            ragas_result = evaluate(dataset=dataset, metrics=metrics)
            scores = {key: round(float(value), 4) for key, value in ragas_result.items()}
            self.tracer.log_metrics(trace_id=trace_id, metrics=scores, source="ragas")
            return {"mode": "ragas", "scores": scores}
        except Exception:
            if not self.use_fallback:
                return {"mode": "ragas_failed", "scores": {}}
            scores = self._fallback_scores(
                question=question,
                answer=answer,
                contexts=contexts,
                reference_answer=reference_answer,
            )
            self.tracer.log_metrics(trace_id=trace_id, metrics=scores, source="ragas_fallback")
            return {"mode": "fallback", "scores": scores}

