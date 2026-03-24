"""AuthService and UserRepository."""

import pytest

from ianuacare.core.auth.repository import UserRepository
from ianuacare.core.auth.service import AuthService
from ianuacare.core.exceptions.errors import AuthenticationError, AuthorizationError


def test_authenticate_success(auth_service: AuthService) -> None:
    u = auth_service.authenticate("tok-ok")
    assert u.user_id == "u1"
    assert "pipeline:run" in u.permissions


def test_authenticate_failure() -> None:
    svc = AuthService(UserRepository())
    with pytest.raises(AuthenticationError):
        svc.authenticate("bad")


def test_authorize_success(auth_service: AuthService) -> None:
    u = auth_service.authenticate("tok-ok")
    auth_service.authorize(u, "pipeline:run")


def test_authorize_failure(auth_service: AuthService) -> None:
    u = auth_service.authenticate("tok-ok")
    with pytest.raises(AuthorizationError):
        auth_service.authorize(u, "admin:all")
