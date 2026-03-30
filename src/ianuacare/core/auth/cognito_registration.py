"""Cognito self-registration (SignUp / ConfirmSignUp)."""

from __future__ import annotations

from ianuacare.core.models.registration_result import RegistrationResult
from ianuacare.infrastructure.auth.cognito import CognitoRegistrationClient


class CognitoRegistrationService:
    """Register users against a Cognito app client that allows self sign-up."""

    def __init__(
        self,
        region: str,
        app_client_id: str,
        *,
        client_secret: str | None = None,
    ) -> None:
        self._client = CognitoRegistrationClient(
            region,
            app_client_id,
            client_secret=client_secret,
        )

    def register(
        self,
        username: str,
        password: str,
        *,
        attributes: dict[str, str] | None = None,
    ) -> RegistrationResult:
        """Create a user; returns :class:`RegistrationResult` (may require ``confirm``).

        ``attributes`` maps Cognito attribute names to values (e.g. ``email``, ``phone_number``).
        Raises :class:`ValidationError` or :class:`AuthenticationError` (rate limits) on failure.
        """
        raw = self._client.sign_up(username, password, attributes=attributes)
        return RegistrationResult(
            user_sub=str(raw["UserSub"]),
            user_confirmed=bool(raw.get("UserConfirmed", False)),
        )

    def confirm(self, username: str, confirmation_code: str) -> None:
        """Confirm sign-up with the code sent by Cognito (email/SMS)."""
        self._client.confirm_sign_up(username, confirmation_code)
