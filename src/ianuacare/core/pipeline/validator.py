"""Validate pipeline data."""

from __future__ import annotations

from typing import Any

from ianuacare.core.exceptions.errors import ValidationError
from ianuacare.core.models.packet import DataPacket


class DataValidator:
    """Applies validation rules and sets ``validated_data`` on the packet."""

    def __init__(self, *, allow_none_raw: bool = False) -> None:
        self._allow_none_raw = allow_none_raw

    def validate(self, packet: DataPacket) -> DataPacket:
        """Validate ``packet.raw_data`` and assign ``packet.validated_data``."""
        if packet.raw_data is None and not self._allow_none_raw:
            raise ValidationError("raw_data is required")
        packet.validated_data = self._coerce_validated(packet.raw_data)
        return packet

    def _coerce_validated(self, raw: Any) -> Any:
        """Override in subclasses for schema-based validation."""
        return raw

