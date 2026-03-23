"""Adapter for external inference APIs."""

from __future__ import annotations

from typing import Any


class AIProvider:
    """Wraps a callable or maps to HTTP/SDK calls; default uses an in-memory infer function."""

    def __init__(
        self,
        infer_fn: Any | None = None,
    ) -> None:
        self._infer = infer_fn or self._default_infer

    def infer(self, model_name: str, payload: Any) -> dict[str, Any]:
        """Invoke inference for ``model_name`` with ``payload``."""
        result = self._infer(model_name, payload)
        if isinstance(result, dict):
            return result
        return {"result": result}

    @staticmethod
    def _default_infer(model_name: str, payload: Any) -> dict[str, Any]:
        return {"model": model_name, "echo": payload}
