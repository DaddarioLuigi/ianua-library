"""Redis adapter."""

from unittest.mock import MagicMock, patch

import ianuacare.infrastructure.cache.redis as redis_module
from ianuacare.infrastructure.cache.redis import RedisCacheClient


def test_redis_set_get_invalidate() -> None:
    mock_redis_cls = MagicMock()
    redis = MagicMock()
    redis.get.return_value = '{"x": 1}'
    mock_redis_cls.from_url.return_value = redis

    with patch.object(redis_module, "Redis", mock_redis_cls):
        cache = RedisCacheClient()
        cache.set("k", {"x": 1}, ttl_seconds=30)
        assert cache.get("k") == {"x": 1}
        cache.invalidate("k")
        redis.delete.assert_called_once_with("k")
