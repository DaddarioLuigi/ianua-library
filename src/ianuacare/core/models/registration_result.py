"""Result of a user registration call against an identity provider."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RegistrationResult:
    """Outcome of Cognito ``SignUp`` (self-registration)."""

    user_sub: str
    """Stable Cognito subject identifier."""

    user_confirmed: bool
    """True if the user pool treated the user as confirmed (no further code step)."""
