"""Cognito adapter."""

from unittest.mock import MagicMock, patch

import ianuacare.infrastructure.auth.cognito as cognito_module
from ianuacare.infrastructure.auth.cognito import CognitoUserRepository


def test_cognito_get_user_by_token() -> None:
    mock_boto3 = MagicMock()
    mock_jwt = MagicMock()
    mock_jwt.get_unverified_claims.return_value = {
        "custom:role": "clinician",
        "custom:permissions": "pipeline:run",
    }
    cognito = MagicMock()
    cognito.get_user.return_value = {"Username": "u1"}
    mock_boto3.client.return_value = cognito

    with patch.object(cognito_module, "boto3", mock_boto3), patch.object(
        cognito_module,
        "jwt",
        mock_jwt,
    ):
        repo = CognitoUserRepository("eu-west-1", "pool", "app")
        user = repo.get_user_by_token("token")

    assert user["user_id"] == "u1"
    assert user["role"] == "clinician"
    assert user["permissions"] == ["pipeline:run"]
