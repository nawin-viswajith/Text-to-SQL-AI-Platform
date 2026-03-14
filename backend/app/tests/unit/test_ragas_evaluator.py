from app.core.config import Settings
from app.services.ragas_evaluator import RagasEvaluator


class _Tracer:
    def __init__(self):
        self.calls = []

    def log_metrics(self, trace_id, metrics, source):
        self.calls.append((trace_id, metrics, source))


def test_ragas_fallback_scores() -> None:
    tracer = _Tracer()
    settings = Settings(
        ragas_enabled=True,
        ragas_use_fallback=True,
    )
    evaluator = RagasEvaluator(settings=settings, tracer=tracer)  # type: ignore[arg-type]
    result = evaluator.evaluate(
        question="show total revenue by month",
        answer="select month, sum(amount) from orders group by month",
        contexts=["orders table has month and amount columns"],
        reference_answer="select month, sum(amount) as total from orders group by month",
        trace_id="trace-1",
    )
    assert result["mode"] in {"ragas", "fallback"}
    assert isinstance(result["scores"], dict)
    assert len(result["scores"]) >= 1
    assert len(tracer.calls) == 1

