"""Authentication infrastructure adapters."""

from ianuacare.infrastructure.auth.cognito import (
    CognitoPasswordAuthenticator,
    CognitoRegistrationClient,
    CognitoUserRepository,
)

__all__ = [
    "CognitoPasswordAuthenticator",
    "CognitoRegistrationClient",
    "CognitoUserRepository",
]
