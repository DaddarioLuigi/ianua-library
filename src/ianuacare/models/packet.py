"""Mutable pipeline state carrier."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DataPacket:
    """Holds data at each stage of the pipeline (raw through inference)."""

    raw_data: Any = None
    parsed_data: Any = None
    validated_data: Any = None
    processed_data: Any = None
    inference_result: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
