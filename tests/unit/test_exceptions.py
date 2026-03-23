"""Exception hierarchy."""

from ianuacare.exceptions.errors import (
    AuthenticationError,
    AuthorizationError,
    IanuacareError,
    InferenceError,
    OrchestrationError,
    StorageError,
    ValidationError,
)


def test_subclasses() -> None:
    assert issubclass(AuthenticationError, IanuacareError)
    assert issubclass(AuthorizationError, IanuacareError)
    assert issubclass(ValidationError, IanuacareError)
    assert issubclass(OrchestrationError, IanuacareError)
    assert issubclass(InferenceError, IanuacareError)
    assert issubclass(StorageError, IanuacareError)


def test_error_attributes() -> None:
    e = ValidationError("bad", code="VAL")
    assert e.message == "bad"
    assert e.code == "VAL"
