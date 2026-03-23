"""Authentication and authorization."""

from __future__ import annotations

from typing import Any

from ianuacare.auth.repository import UserRepository
from ianuacare.exceptions.errors import AuthenticationError, AuthorizationError
from ianuacare.models.context import RequestContext
from ianuacare.models.user import User


class AuthService:
    """Authenticate tokens and enforce permission checks."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def authenticate(self, token: str) -> User:
        """Resolve ``token`` to a :class:`User`."""
        try:
            record = self._user_repository.get_user_by_token(token)
        except KeyError as exc:
            raise AuthenticationError("Invalid or unknown token") from exc
        try:
            return User(
                user_id=str(record["user_id"]),
                role=str(record["role"]),
                permissions=list(record.get("permissions", [])),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise AuthenticationError("Malformed user record") from exc

    def authorize(self, user: User, required_permission: str) -> None:
        """Ensure ``user`` has ``required_permission`` or raise :class:`AuthorizationError`."""
        if required_permission not in user.permissions:
            raise AuthorizationError(
                f"Missing permission: {required_permission}",
                code="forbidden",
            )

    def build_context(
        self,
        user: User,
        *,
        product: str,
        metadata: dict[str, Any] | None = None,
    ) -> RequestContext:
        """Convenience helper to build a :class:`RequestContext`."""
        return RequestContext(user=user, product=product, metadata=dict(metadata or {}))
