"""Exception hierarchy for the Ianuacare framework."""


class IanuacareError(Exception):
    """Base exception for all framework errors."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__


class AuthenticationError(IanuacareError):
    """Raised when authentication fails (invalid or missing credentials)."""


class AuthorizationError(IanuacareError):
    """Raised when the user lacks required permissions."""


class ValidationError(IanuacareError):
    """Raised when input or data validation fails."""


class OrchestrationError(IanuacareError):
    """Raised when pipeline orchestration or model selection fails."""


class InferenceError(IanuacareError):
    """Raised when AI inference fails."""


class StorageError(IanuacareError):
    """Raised when persistence to database or object storage fails."""

