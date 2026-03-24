"""Writer encryption integration."""

from ianuacare.core.models.context import RequestContext
from ianuacare.core.models.packet import DataPacket
from ianuacare.core.models.user import User
from ianuacare.infrastructure.encryption import NoOpEncryption
from ianuacare.infrastructure.storage import InMemoryBucketClient, InMemoryDatabaseClient, Writer


def test_writer_accepts_encryption_service() -> None:
    writer = Writer(InMemoryDatabaseClient(), InMemoryBucketClient(), encryption=NoOpEncryption())
    ctx = RequestContext(User("u1", "r", []), "prod", {})
    packet = DataPacket(raw_data={"a": 1}, metadata={"request_id": "r1"})
    out = writer.write_raw(packet, ctx)
    assert out["ok"] is True
