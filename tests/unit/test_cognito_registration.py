"""Cognito self-registration (SignUp / ConfirmSignUp)."""

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import ianuacare.infrastructure.auth.cognito as cognito_module
from ianuacare.core.auth.cognito_registration import CognitoRegistrationService
from ianuacare.core.exceptions.errors import AuthenticationError, ValidationError


def test_cognito_register_success_pending_confirmation() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.sign_up.return_value = {
        "UserSub": "sub-123",
        "UserConfirmed": False,
    }
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoRegistrationService("eu-west-1", "client-id")
        result = svc.register(
            "user@example.com",
            "ValidP@ssw0rd1",
            attributes={"email": "user@example.com"},
        )

    assert result.user_sub == "sub-123"
    assert result.user_confirmed is False
    cognito.sign_up.assert_called_once()
    call_kw = cognito.sign_up.call_args[1]
    assert call_kw["ClientId"] == "client-id"
    assert call_kw["Username"] == "user@example.com"
    assert call_kw["Password"] == "ValidP@ssw0rd1"
    assert {"Name": "email", "Value": "user@example.com"} in call_kw["UserAttributes"]
    assert "SECRET_HASH" not in call_kw


def test_cognito_register_success_auto_confirmed() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.sign_up.return_value = {"UserSub": "sub-abc", "UserConfirmed": True}
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoRegistrationService("eu-west-1", "client-id")
        result = svc.register("alice", "ValidP@ssw0rd1")

    assert result.user_sub == "sub-abc"
    assert result.user_confirmed is True


def test_cognito_register_includes_secret_hash() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.sign_up.return_value = {"UserSub": "s", "UserConfirmed": False}
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoRegistrationService("eu-west-1", "client-id", client_secret="sec")
        svc.register("bob", "ValidP@ssw0rd1")

    sh = cognito.sign_up.call_args[1]["SecretHash"]
    assert isinstance(sh, str) and len(sh) > 0


def test_cognito_register_username_exists() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.sign_up.side_effect = ClientError(
        {"Error": {"Code": "UsernameExistsException", "Message": "x"}},
        "SignUp",
    )
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoRegistrationService("eu-west-1", "client-id")

    with pytest.raises(ValidationError) as ei:
        svc.register("u", "ValidP@ssw0rd1")
    assert ei.value.code == "username_exists"


def test_cognito_confirm_success() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoRegistrationService("eu-west-1", "client-id")
        svc.confirm("user@example.com", "123456")

    cognito.confirm_sign_up.assert_called_once()
    kw = cognito.confirm_sign_up.call_args[1]
    assert kw["Username"] == "user@example.com"
    assert kw["ConfirmationCode"] == "123456"


def test_cognito_confirm_code_mismatch() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.confirm_sign_up.side_effect = ClientError(
        {"Error": {"Code": "CodeMismatchException", "Message": "x"}},
        "ConfirmSignUp",
    )
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoRegistrationService("eu-west-1", "client-id")

    with pytest.raises(ValidationError) as ei:
        svc.confirm("u", "wrong")
    assert ei.value.code == "invalid_confirmation_code"


def test_cognito_register_rate_limited() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.sign_up.side_effect = ClientError(
        {"Error": {"Code": "TooManyRequestsException", "Message": "x"}},
        "SignUp",
    )
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoRegistrationService("eu-west-1", "client-id")

    with pytest.raises(AuthenticationError) as ei:
        svc.register("u", "ValidP@ssw0rd1")
    assert ei.value.code == "rate_limited"
