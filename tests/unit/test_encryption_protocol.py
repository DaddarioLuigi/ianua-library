"""Encryption protocol implementations."""

from ianuacare.infrastructure.encryption import NoOpEncryption


def test_noop_encryption_roundtrip() -> None:
    enc = NoOpEncryption()
    value = b"abc"
    assert enc.decrypt(enc.encrypt(value)) == value
