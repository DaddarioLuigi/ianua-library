"""AuditService."""

from ianuacare.core.audit.service import AuditService
from ianuacare.core.models.context import RequestContext
from ianuacare.core.models.user import User


def test_log_event(db) -> None:
    u = User("u1", "r", [])
    ctx = RequestContext(u, "p", {})
    a = AuditService(db)
    a.log_event("evt", ctx, {"k": "v"})
    rows = db.fetch_all("audit_events")
    assert len(rows) == 1
    assert rows[0]["event"] == "evt"
