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
            logger.info("LangSmith trace started: %s for state=%s", trace_id, state_id)
        return trace_id

    def log_event(self, trace_id: str | None, node: str, payload: dict[str, Any]) -> None:
        if self.enabled and trace_id:
            logger.info("LangSmith event %s node=%s", trace_id, node)

    def end_trace(self, trace_id: str | None, payload: dict[str, Any]) -> None:
        if self.enabled and trace_id:
            logger.info("LangSmith trace ended: %s", trace_id)

