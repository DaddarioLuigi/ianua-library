"""PostgreSQL storage adapter."""

from __future__ import annotations

import json
from typing import Any

try:  # Optional dependency
    import psycopg
except Exception:  # pragma: no cover - import-time optional dependency handling
    psycopg = None  # type: ignore[assignment]


class PostgresDatabaseClient:
    """Persist records in per-collection PostgreSQL tables."""

    def __init__(self, connection_string: str) -> None:
        if psycopg is None:
            raise ImportError("PostgresDatabaseClient requires psycopg")
        self._connection_string = connection_string

    def write(self, collection: str, record: dict[str, Any]) -> dict[str, Any]:
        with psycopg.connect(self._connection_string) as conn, conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {collection} (payload) VALUES (%s)",
                (json.dumps(record),),
            )
            conn.commit()
        return {"ok": True, "collection": collection}

    def fetch_all(self, collection: str) -> list[dict[str, Any]]:
        with psycopg.connect(self._connection_string) as conn, conn.cursor() as cur:
            cur.execute(f"SELECT payload FROM {collection}")
            rows = cur.fetchall()
        return [json.loads(row[0]) for row in rows]
