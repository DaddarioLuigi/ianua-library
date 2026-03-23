"""AuditService."""

from ianuacare.audit.service import AuditService
from ianuacare.models.context import RequestContext
from ianuacare.models.user import User


def test_log_event(db) -> None:
    u = User("u1", "r", [])
    ctx = RequestContext(u, "p", {})
    a = AuditService(db)
    a.log_event("evt", ctx, {"k": "v"})
    rows = db.fetch_all("audit_events")
    assert len(rows) == 1
    assert rows[0]["event"] == "evt"
