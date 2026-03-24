"""JSON structured logger."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from ianuacare.core.models.context import RequestContext


class StructuredLogger:
    """Emit JSON logs with optional request context fields."""

    def __init__(self, name: str = "ianuacare", *, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(name)

    def info(
        self,
        message: str,
        *,
        context: RequestContext | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._emit(logging.INFO, message, context=context, extra=extra)

    def warning(
        self,
        message: str,
        *,
        context: RequestContext | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._emit(logging.WARNING, message, context=context, extra=extra)

    def error(
        self,
        message: str,
        *,
        context: RequestContext | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._emit(logging.ERROR, message, context=context, extra=extra)

    def _emit(
        self,
        level: int,
        message: str,
        *,
        context: RequestContext | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": logging.getLevelName(level),
            "message": message,
        }
        if context is not None:
            payload["user_id"] = context.user.user_id
            payload["product"] = context.product
            request_id = context.metadata.get("request_id")
            if request_id is not None:
                payload["request_id"] = request_id
        if extra:
            payload.update(extra)
        self._logger.log(level, json.dumps(payload, sort_keys=True))
