"""Cache abstractions and in-memory implementation."""

from __future__ import annotations

import time
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CacheClient(Protocol):
    """Contract for key/value caches used by orchestration."""

    def get(self, key: str) -> Any | None:
        """Return cached value or ``None`` when missing/expired."""
        ...

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        """Store ``value`` under ``key`` with optional TTL."""
        ...

    def invalidate(self, key: str) -> None:
        """Delete ``key`` if present."""
        ...


class InMemoryCacheClient:
    """Simple in-memory cache with optional TTL support."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float | None]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if expires_at is not None and expires_at <= time.time():
            self.invalidate(key)
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        expires_at = time.time() + ttl_seconds if ttl_seconds is not None else None
        self._store[key] = (value, expires_at)

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)


__all__ = ["CacheClient", "InMemoryCacheClient"]
