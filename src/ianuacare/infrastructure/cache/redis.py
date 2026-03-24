"""Redis cache adapter."""

from __future__ import annotations

import json
from typing import Any

try:  # Optional dependency
    from redis import Redis
except Exception:  # pragma: no cover - import-time optional dependency handling
    Redis = None  # type: ignore[assignment]


class RedisCacheClient:
    """Cache adapter backed by Redis."""

    def __init__(self, url: str = "redis://localhost:6379") -> None:
        if Redis is None:
            raise ImportError("RedisCacheClient requires redis")
        self._redis = Redis.from_url(url)

    def get(self, key: str) -> Any | None:
        value = self._redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        serialized = json.dumps(value)
        self._redis.set(name=key, value=serialized, ex=ttl_seconds)

    def invalidate(self, key: str) -> None:
        self._redis.delete(key)
