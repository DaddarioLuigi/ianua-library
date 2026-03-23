"""Audit trail (no PHI in stored details)."""

from __future__ import annotations

from typing import Any

from ianuacare.models.context import RequestContext
from ianuacare.storage.database import DatabaseClient


class AuditService:
    """Persists audit events with user/product scope only."""

    COL_AUDIT = "audit_events"

    def __init__(self, db_client: DatabaseClient) -> None:
        self._db = db_client

    def log_event(
        self,
        event_name: str,
        context: RequestContext,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Record an audit event; ``details`` must not contain PHI/PII."""
        safe_details = dict(details or {})
        record = {
            "event": event_name,
            "user_id": context.user.user_id,
            "product": context.product,
            "details": safe_details,
        }
        self._db.write(self.COL_AUDIT, record)
