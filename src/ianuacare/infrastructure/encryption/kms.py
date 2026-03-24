"""AWS KMS encryption adapter."""

from __future__ import annotations

import base64

try:  # Optional dependency
    import boto3
except Exception:  # pragma: no cover - import-time optional dependency handling
    boto3 = None  # type: ignore[assignment]


class KMSEncryptionService:
    """Encrypt/decrypt bytes using AWS KMS."""

    def __init__(self, key_id: str, region: str | None = None) -> None:
        if boto3 is None:
            raise ImportError("KMSEncryptionService requires boto3")
        self._key_id = key_id
        self._kms = boto3.client("kms", region_name=region)

    def encrypt(self, data: bytes) -> bytes:
        response = self._kms.encrypt(KeyId=self._key_id, Plaintext=data)
        return base64.b64encode(response["CiphertextBlob"])

    def decrypt(self, data: bytes) -> bytes:
        ciphertext = base64.b64decode(data)
        response = self._kms.decrypt(CiphertextBlob=ciphertext)
        return bytes(response["Plaintext"])
