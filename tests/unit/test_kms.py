"""KMS encryption adapter."""

from unittest.mock import MagicMock, patch

import ianuacare.infrastructure.encryption.kms as kms_module
from ianuacare.infrastructure.encryption.kms import KMSEncryptionService


def test_kms_encrypt_decrypt() -> None:
    mock_boto3 = MagicMock()
    kms = MagicMock()
    kms.encrypt.return_value = {"CiphertextBlob": b"cipher"}
    kms.decrypt.return_value = {"Plaintext": b"plain"}
    mock_boto3.client.return_value = kms

    with patch.object(kms_module, "boto3", mock_boto3):
        svc = KMSEncryptionService("key")
        encrypted = svc.encrypt(b"plain")
        assert isinstance(encrypted, bytes)
        assert svc.decrypt(encrypted) == b"plain"
