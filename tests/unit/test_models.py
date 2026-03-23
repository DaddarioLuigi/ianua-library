"""Tests for domain models."""

from ianuacare.models.context import RequestContext
from ianuacare.models.packet import DataPacket
from ianuacare.models.user import User


def test_user_slots_and_fields() -> None:
    u = User("1", "admin", ["a:1"])
    assert u.user_id == "1"
    assert u.role == "admin"
    assert u.permissions == ["a:1"]


def test_request_context() -> None:
    u = User("1", "r", [])
    ctx = RequestContext(u, "p", metadata={"k": 1})
    assert ctx.user is u
    assert ctx.product == "p"
    assert ctx.metadata["k"] == 1


def test_data_packet() -> None:
    p = DataPacket(raw_data={"x": 1}, metadata={"m": 2})
    assert p.raw_data == {"x": 1}
    assert p.metadata["m"] == 2
