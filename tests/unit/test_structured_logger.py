"""Structured logger."""

from __future__ import annotations

import json
import logging

from ianuacare.core.logging.service import StructuredLogger
from ianuacare.core.models.context import RequestContext
from ianuacare.core.models.user import User


def test_structured_logger_emits_json(caplog) -> None:
    logger = logging.getLogger("test-structured")
    structured = StructuredLogger(logger=logger)
    context = RequestContext(User("u1", "r", []), "prod", {"request_id": "r1"})

    with caplog.at_level(logging.INFO, logger="test-structured"):
        structured.info("hello", context=context, extra={"k": "v"})

    payload = json.loads(caplog.records[0].message)
    assert payload["message"] == "hello"
    assert payload["user_id"] == "u1"
    assert payload["product"] == "prod"
    assert payload["request_id"] == "r1"
    assert payload["k"] == "v"
