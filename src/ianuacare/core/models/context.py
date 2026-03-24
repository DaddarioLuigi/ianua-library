"""Per-request context for pipeline execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ianuacare.core.models.user import User


@dataclass(slots=True)
class RequestContext:
    """Carries the current user, product scope, and non-PII metadata."""

    user: User
    product: str
    metadata: dict[str, Any] = field(default_factory=dict)

