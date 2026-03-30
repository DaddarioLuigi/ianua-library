"""Cognito-backed user repository and password login."""

from __future__ import annotations

import base64
import hashlib
import hmac
from typing import Any, NoReturn

from ianuacare.core.exceptions.errors import AuthenticationError, ValidationError

try:  # Optional dependencies
    import boto3
    from jose import jwt
except Exception:  # pragma: no cover - import-time optional dependency handling
    boto3 = None  # type: ignore[assignment]
    jwt = None  # type: ignore[assignment]


def _cognito_secret_hash(username: str, client_id: str, client_secret: str) -> str:
    """Compute SECRET_HASH for confidential app clients (USER_PASSWORD_AUTH)."""
    msg = bytes(username + client_id, "utf-8")
    key = bytes(client_secret, "utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def _raise_cognito_initiate_auth_error(exc: Any) -> NoReturn:
    """Map Cognito ``InitiateAuth`` failures to :class:`AuthenticationError`."""
    from botocore.exceptions import ClientError

    if not isinstance(exc, ClientError):
        raise exc
    code = exc.response.get("Error", {}).get("Code", "")
    if code in ("NotAuthorizedException", "UserNotFoundException"):
        raise AuthenticationError(
            "Invalid username or password",
            code="invalid_credentials",
        ) from exc
    if code == "TooManyRequestsException":
        raise AuthenticationError("Too many attempts", code="rate_limited") from exc
    raise AuthenticationError("Authentication failed", code="cognito_error") from exc


def _raise_cognito_sign_up_error(exc: Any) -> NoReturn:
    """Map Cognito ``SignUp`` failures."""
    from botocore.exceptions import ClientError

    if not isinstance(exc, ClientError):
        raise exc
    code = exc.response.get("Error", {}).get("Code", "")
    if code == "UsernameExistsException":
        raise ValidationError("Username already registered", code="username_exists") from exc
    if code == "InvalidPasswordException":
        raise ValidationError("Password does not meet policy", code="invalid_password") from exc
    if code == "InvalidParameterException":
        raise ValidationError("Invalid sign-up parameters", code="invalid_parameter") from exc
    if code == "TooManyRequestsException":
        raise AuthenticationError("Too many attempts", code="rate_limited") from exc
    if code == "UserLambdaValidationException":
        msg = exc.response.get("Error", {}).get("Message", "Registration validation failed")
        raise ValidationError(msg, code="user_lambda_validation") from exc
    raise ValidationError("Registration failed", code="cognito_error") from exc


def _raise_cognito_confirm_sign_up_error(exc: Any) -> NoReturn:
    """Map Cognito ``ConfirmSignUp`` failures."""
    from botocore.exceptions import ClientError

    if not isinstance(exc, ClientError):
        raise exc
    code = exc.response.get("Error", {}).get("Code", "")
    if code == "CodeMismatchException":
        raise ValidationError(
            "Invalid confirmation code",
            code="invalid_confirmation_code",
        ) from exc
    if code == "ExpiredCodeException":
        raise ValidationError(
            "Confirmation code expired",
            code="expired_confirmation_code",
        ) from exc
    if code == "NotAuthorizedException":
        raise ValidationError(
            "User cannot be confirmed or is already confirmed",
            code="confirm_not_allowed",
        ) from exc
    if code == "UserNotFoundException":
        raise ValidationError("Unknown user", code="user_not_found") from exc
    if code == "AliasExistsException":
        raise ValidationError("Alias already in use", code="alias_exists") from exc
    if code == "TooManyRequestsException":
        raise AuthenticationError("Too many attempts", code="rate_limited") from exc
    raise ValidationError("Confirmation failed", code="cognito_error") from exc


class CognitoUserRepository:
    """Resolve users by validating Cognito-issued JWT access tokens."""

    def __init__(self, region: str, user_pool_id: str, app_client_id: str) -> None:
        if boto3 is None or jwt is None:
            raise ImportError("CognitoUserRepository requires boto3 and python-jose")
        self._region = region
        self._user_pool_id = user_pool_id
        self._app_client_id = app_client_id
        self._cognito = boto3.client("cognito-idp", region_name=region)

    def get_user_by_token(self, token: str) -> dict[str, Any]:
        """Return a user record from token claims."""
        claims = jwt.get_unverified_claims(token)
        user_info = self._cognito.get_user(AccessToken=token)
        username = user_info.get("Username") or claims.get("sub") or "unknown"
        role = str(claims.get("custom:role", claims.get("cognito:groups", ["user"])[0]))
        permissions_raw = claims.get("custom:permissions", "")
        permissions = [p for p in str(permissions_raw).split(",") if p]
        return {
            "user_id": str(username),
            "role": role,
            "permissions": permissions,
        }


class CognitoPasswordAuthenticator:
    """USER_PASSWORD_AUTH against a Cognito app client."""

    def __init__(
        self,
        region: str,
        app_client_id: str,
        *,
        client_secret: str | None = None,
    ) -> None:
        if boto3 is None:
            raise ImportError("CognitoPasswordAuthenticator requires boto3")
        self._client_id = app_client_id
        self._client_secret = client_secret
        self._cognito = boto3.client("cognito-idp", region_name=region)

    def initiate_user_password_auth(self, username: str, password: str) -> dict[str, Any]:
        """Call ``InitiateAuth`` and return the boto3 response dict."""
        auth_params: dict[str, str] = {
            "USERNAME": username,
            "PASSWORD": password,
        }
        if self._client_secret:
            auth_params["SECRET_HASH"] = _cognito_secret_hash(
                username, self._client_id, self._client_secret
            )
        try:
            return self._cognito.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                ClientId=self._client_id,
                AuthParameters=auth_params,
            )
        except Exception as exc:
            _raise_cognito_initiate_auth_error(exc)


class CognitoRegistrationClient:
    """Self-service registration via Cognito ``SignUp`` / ``ConfirmSignUp``."""

    def __init__(
        self,
        region: str,
        app_client_id: str,
        *,
        client_secret: str | None = None,
    ) -> None:
        if boto3 is None:
            raise ImportError("CognitoRegistrationClient requires boto3")
        self._client_id = app_client_id
        self._client_secret = client_secret
        self._cognito = boto3.client("cognito-idp", region_name=region)

    def sign_up(
        self,
        username: str,
        password: str,
        *,
        attributes: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Call ``sign_up`` and return the boto3 response dict."""
        user_attrs = [{"Name": k, "Value": v} for k, v in (attributes or {}).items()]
        kwargs: dict[str, Any] = {
            "ClientId": self._client_id,
            "Username": username,
            "Password": password,
            "UserAttributes": user_attrs,
        }
        if self._client_secret:
            kwargs["SecretHash"] = _cognito_secret_hash(
                username, self._client_id, self._client_secret
            )
        try:
            return self._cognito.sign_up(**kwargs)
        except Exception as exc:
            _raise_cognito_sign_up_error(exc)

    def confirm_sign_up(self, username: str, confirmation_code: str) -> None:
        """Call ``confirm_sign_up``."""
        kwargs: dict[str, Any] = {
            "ClientId": self._client_id,
            "Username": username,
            "ConfirmationCode": confirmation_code,
        }
        if self._client_secret:
            kwargs["SecretHash"] = _cognito_secret_hash(
                username, self._client_id, self._client_secret
            )
        try:
            self._cognito.confirm_sign_up(**kwargs)
        except Exception as exc:
            _raise_cognito_confirm_sign_up_error(exc)
