"""Example NLP model implementation."""

from __future__ import annotations

from typing import Any

from ianuacare.ai.base import BaseAIModel
from ianuacare.ai.provider import AIProvider


class NLPModel(BaseAIModel):
    """Routes inference through an :class:`AIProvider` using a fixed ``model_name``."""

    def __init__(self, provider: AIProvider, model_name: str) -> None:
        self._provider = provider
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

    def run(self, payload: Any) -> Any:
        """Call the provider and return the inference result."""
        return self._provider.infer(self._model_name, payload)
