"""Cognito account operations (reset, logout, change password, profile)."""

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import ianuacare.infrastructure.auth.cognito as cognito_module
from ianuacare.core.auth.cognito_account import CognitoAccountService
from ianuacare.core.exceptions.errors import AuthenticationError, ValidationError


def test_request_password_reset_returns_delivery() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.forgot_password.return_value = {
        "CodeDeliveryDetails": {
            "Destination": "u***@e***",
            "DeliveryMedium": "EMAIL",
        }
    }
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")
        delivery = svc.request_password_reset("user@example.com")

    assert delivery.destination == "u***@e***"
    assert delivery.delivery_medium == "EMAIL"
    cognito.forgot_password.assert_called_once()


def test_confirm_password_reset_calls_boto() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")
        svc.confirm_password_reset("u", "123456", "NewP@ssw0rd1")

    cognito.confirm_forgot_password.assert_called_once()
    kw = cognito.confirm_forgot_password.call_args[1]
    assert kw["Username"] == "u"
    assert kw["ConfirmationCode"] == "123456"
    assert kw["Password"] == "NewP@ssw0rd1"


def test_logout_global_sign_out() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")
        svc.logout("access-token")

    cognito.global_sign_out.assert_called_once_with(AccessToken="access-token")


def test_logout_invalid_token() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.global_sign_out.side_effect = ClientError(
        {"Error": {"Code": "NotAuthorizedException", "Message": "x"}},
        "GlobalSignOut",
    )
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")

    with pytest.raises(AuthenticationError) as ei:
        svc.logout("bad")
    assert ei.value.code == "invalid_token"


def test_change_password() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")
        svc.change_password("at", "OldP@ss1", "NewP@ssw0rd1")

    cognito.change_password.assert_called_once_with(
        AccessToken="at",
        PreviousPassword="OldP@ss1",
        ProposedPassword="NewP@ssw0rd1",
    )


def test_change_password_wrong_old_password() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.change_password.side_effect = ClientError(
        {"Error": {"Code": "NotAuthorizedException", "Message": "x"}},
        "ChangePassword",
    )
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")

    with pytest.raises(AuthenticationError) as ei:
        svc.change_password("at", "wrong", "NewP@ssw0rd1")
    assert ei.value.code == "invalid_credentials"


def test_update_profile_attributes() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")
        svc.update_profile_attributes("at", {"email": "n@example.com"})

    cognito.update_user_attributes.assert_called_once()
    kw = cognito.update_user_attributes.call_args[1]
    assert kw["AccessToken"] == "at"
    assert {"Name": "email", "Value": "n@example.com"} in kw["UserAttributes"]


def test_update_profile_alias_exists() -> None:
    mock_boto3 = MagicMock()
    cognito = MagicMock()
    cognito.update_user_attributes.side_effect = ClientError(
        {"Error": {"Code": "AliasExistsException", "Message": "x"}},
        "UpdateUserAttributes",
    )
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3):
        svc = CognitoAccountService("eu-west-1", "client-id")

    with pytest.raises(ValidationError) as ei:
        svc.update_profile_attributes("at", {"email": "taken@example.com"})
    assert ei.value.code == "alias_exists"
