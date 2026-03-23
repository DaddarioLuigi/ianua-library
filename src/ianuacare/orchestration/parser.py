"""Parse validated input into structured ``parsed_data``."""

from __future__ import annotations

from typing import Any

from ianuacare.models.packet import DataPacket


class DataParser:
    """Transforms ``validated_data`` into ``parsed_data`` (e.g. JSON, clinical text)."""

    def parse(self, packet: DataPacket) -> DataPacket:
        """Default: pass-through copy of ``validated_data``."""
        packet.parsed_data = self._parse_impl(packet.validated_data)
        return packet

    def _parse_impl(self, validated: Any) -> Any:
        """Override for domain-specific parsing."""
        return validated
