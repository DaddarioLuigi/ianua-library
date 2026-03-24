"""Database abstraction (protocol + in-memory implementation)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DatabaseClient(Protocol):
    """Contract for database-backed persistence."""

    def write(self, collection: str, record: dict[str, Any]) -> dict[str, Any]:
        """Insert or update a record in ``collection``."""
        ...

    def fetch_all(self, collection: str) -> list[dict[str, Any]]:
        """Return all records in ``collection``."""
        ...


class InMemoryDatabaseClient:
    """In-memory ``DatabaseClient`` for development and tests."""

    def __init__(self, storage: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self._storage: dict[str, list[dict[str, Any]]] = storage if storage is not None else {}

    def write(self, collection: str, record: dict[str, Any]) -> dict[str, Any]:
        if collection not in self._storage:
            self._storage[collection] = []
        self._storage[collection].append(dict(record))
        return {"ok": True, "collection": collection, "count": len(self._storage[collection])}

    def fetch_all(self, collection: str) -> list[dict[str, Any]]:
        return [dict(r) for r in self._storage.get(collection, [])]

