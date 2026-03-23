"""Abstract base for AI models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAIModel(ABC):
    """Subclass to implement product-specific inference."""

    @abstractmethod
    def run(self, payload: Any) -> Any:
        """Run inference on ``payload`` and return structured output."""
        ...
