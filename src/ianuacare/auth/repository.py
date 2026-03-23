"""User lookup by opaque token (for testing and simple deployments)."""

from __future__ import annotations

from typing import Any


class UserRepository:
    """Maps bearer tokens to user record dicts (see :class:`~ianuacare.models.user.User`)."""

    def __init__(self, tokens: dict[str, dict[str, Any]] | None = None) -> None:
        self._tokens: dict[str, dict[str, Any]] = dict(tokens) if tokens else {}

    def get_user_by_token(self, token: str) -> dict[str, Any]:
        """Return user record for ``token`` or raise ``KeyError`` if unknown."""
        if token not in self._tokens:
            raise KeyError(token)
        return dict(self._tokens[token])

    def register_token(self, token: str, user: dict[str, Any]) -> None:
        """Register a token (mainly for tests)."""
        self._tokens[token] = dict(user)
