"""Cache protocol implementations."""

from ianuacare.infrastructure.cache import InMemoryCacheClient


def test_in_memory_cache_set_get_invalidate() -> None:
    cache = InMemoryCacheClient()
    cache.set("k", {"a": 1})
    assert cache.get("k") == {"a": 1}
    cache.invalidate("k")
    assert cache.get("k") is None
