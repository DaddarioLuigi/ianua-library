"""Database and bucket clients."""

from ianuacare.infrastructure.storage.bucket import InMemoryBucketClient
from ianuacare.infrastructure.storage.database import InMemoryDatabaseClient


def test_database_write_fetch() -> None:
    db = InMemoryDatabaseClient()
    db.write("c", {"a": 1})
    assert db.fetch_all("c") == [{"a": 1}]


def test_bucket_upload_download() -> None:
    b = InMemoryBucketClient()
    b.upload("k", b"data")
    assert b.download("k") == b"data"
