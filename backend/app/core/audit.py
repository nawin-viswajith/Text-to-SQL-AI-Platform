from __future__ import annotations

import logging
import time
import uuid

from fastapi import Request, Response

logger = logging.getLogger("audit")


async def audit_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    response: Response = await call_next(request)
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    logger.info(
        "request_id=%s method=%s path=%s status=%s duration_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    response.headers["X-Request-Id"] = request_id
    return response

