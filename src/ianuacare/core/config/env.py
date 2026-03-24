"""Environment-backed configuration service."""

from __future__ import annotations

import os
from typing import Any

from ianuacare.core.config.service import ConfigService


class EnvConfigService(ConfigService):
    """Read settings from memory first, then from environment variables."""

    def __init__(
        self,
        settings: dict[str, Any] | None = None,
        *,
        prefix: str = "IANUA",
    ) -> None:
        super().__init__(settings=settings)
        self._prefix = prefix.strip().upper()

    def get(self, key: str, default: Any = None) -> Any:
        """Return local setting, env-backed value, or ``default``."""
        value = super().get(key, default=None)
        if value is not None:
            return value
        env_key = f"{self._prefix}_{key}".upper()
        return os.environ.get(env_key, default)
