from __future__ import annotations

import logging
import os
import uuid
from typing import Any

from app.core.config import Settings

logger = logging.getLogger(__name__)


class LangSmithTracer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.enabled = settings.langsmith_tracing
        self._client = None
        if self.enabled:
            try:
                from langsmith import Client

                if settings.langsmith_api_key:
                    os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
                os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
                self._client = Client()
            except Exception as exc:  # pragma: no cover
                logger.warning("LangSmith disabled due to initialization error: %s", exc)
                self.enabled = False

    def start_trace(self, state_id: str, payload: dict[str, Any]) -> str:
        trace_id = str(uuid.uuid4())
        if self.enabled and self._client:
            try:
                self._client.create_run(
                    id=trace_id,
                    name="text2sql-query",
                    run_type="chain",
                    inputs=payload,
                    metadata={"state_id": state_id},
                    project_name=self.settings.langsmith_project,
                )
            except Exception as exc:  # pragma: no cover
                logger.warning("LangSmith create_run failed: %s", exc)
            logger.info("LangSmith trace started: %s for state=%s", trace_id, state_id)
        return trace_id

    def log_event(self, trace_id: str | None, node: str, payload: dict[str, Any]) -> None:
        if not trace_id:
            return
        if self.enabled and self._client:
            try:
                self._client.create_example(
                    inputs={"node": node},
                    outputs=payload,
                    metadata={"trace_id": trace_id, "kind": "node_event"},
                )
            except Exception:  # pragma: no cover
                pass
        logger.info("LangSmith event %s node=%s", trace_id, node)

    def log_retrieval(self, trace_id: str | None, payload: dict[str, Any]) -> None:
        if not trace_id:
            return
        if self.enabled and self._client:
            try:
                self._client.create_example(
                    inputs={"kind": "retrieval"},
                    outputs=payload,
                    metadata={"trace_id": trace_id, "kind": "retrieval"},
                )
            except Exception:  # pragma: no cover
                pass
        logger.info("LangSmith retrieval %s strategy=%s", trace_id, payload.get("strategy"))

    def log_metrics(self, trace_id: str | None, metrics: dict[str, float], source: str) -> None:
        if not trace_id:
            return
        if self.enabled and self._client:
            for metric_name, score in metrics.items():
                try:
                    self._client.create_feedback(
                        run_id=trace_id,
                        key=f"{source}.{metric_name}",
                        score=float(score),
                    )
                except Exception:  # pragma: no cover
                    pass
        logger.info("LangSmith metrics %s source=%s metrics=%s", trace_id, source, metrics)

    def end_trace(self, trace_id: str | None, payload: dict[str, Any]) -> None:
        if not trace_id:
            return
        if self.enabled and self._client:
            try:
                self._client.update_run(
                    run_id=trace_id,
                    outputs=payload,
                    end_time=None,
                )
            except Exception:  # pragma: no cover
                pass
        logger.info("LangSmith trace ended: %s", trace_id)
