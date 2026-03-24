"""Cognito-backed user repository."""

from __future__ import annotations

from typing import Any

try:  # Optional dependencies
    import boto3
    from jose import jwt
except Exception:  # pragma: no cover - import-time optional dependency handling
    boto3 = None  # type: ignore[assignment]
    jwt = None  # type: ignore[assignment]


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
