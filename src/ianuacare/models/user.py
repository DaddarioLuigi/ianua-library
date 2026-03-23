"""User identity and authorization attributes."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class User:
    """Authenticated principal with role and fine-grained permissions."""

    user_id: str
    role: str
    permissions: list[str] = field(default_factory=list)
