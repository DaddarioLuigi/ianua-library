"""ConfigService."""

from ianuacare.config.service import ConfigService


def test_get_default() -> None:
    c = ConfigService()
    assert c.get("missing", 42) == 42


def test_set_get() -> None:
    c = ConfigService({"a": 1})
    assert c.get("a") == 1
    c.set("b", 2)
    assert c.get("b") == 2
