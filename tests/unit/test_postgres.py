"""PostgreSQL adapter."""

from unittest.mock import MagicMock, patch

import ianuacare.infrastructure.storage.postgres as postgres_module
from ianuacare.infrastructure.storage.postgres import PostgresDatabaseClient


def test_postgres_write_fetch() -> None:
    mock_psycopg = MagicMock()
    conn = MagicMock()
    cur = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cur
    mock_psycopg.connect.return_value.__enter__.return_value = conn
    cur.fetchall.return_value = [('{"a": 1}',)]

    with patch.object(postgres_module, "psycopg", mock_psycopg):
        db = PostgresDatabaseClient("postgresql://example")
        out = db.write("records", {"a": 1})
        assert out["ok"] is True
        rows = db.fetch_all("records")
        assert rows == [{"a": 1}]
