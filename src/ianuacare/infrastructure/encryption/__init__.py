"""Encryption abstractions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EncryptionService(Protocol):
    """Contract for reversible encryption services."""

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt clear bytes."""
        ...

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt encrypted bytes."""
        ...


class NoOpEncryption:
    """Test-friendly encryption that leaves data unchanged."""

    def encrypt(self, data: bytes) -> bytes:
        return data

    def decrypt(self, data: bytes) -> bytes:
        return data


__all__ = ["EncryptionService", "NoOpEncryption"]
