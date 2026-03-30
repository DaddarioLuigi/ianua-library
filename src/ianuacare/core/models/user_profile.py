"""Cognito GetUser profile snapshot."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class UserProfile:
    """Username and attribute map from Cognito ``get_user`` (access token)."""

    username: str
    attributes: dict[str, str] = field(default_factory=dict)
