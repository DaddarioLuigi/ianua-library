"""Typed configuration access."""

from __future__ import annotations

from typing import Any


class ConfigService:
    """Key-value configuration with optional defaults."""

    def __init__(self, settings: dict[str, Any] | None = None) -> None:
        self._settings: dict[str, Any] = dict(settings) if settings else {}

    def get(self, key: str, default: Any = None) -> Any:
        """Return ``settings[key]`` or ``default`` if missing."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value (mainly for tests and dynamic config)."""
        self._settings[key] = value

