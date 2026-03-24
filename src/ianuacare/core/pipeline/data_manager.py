"""Ingest input into a :class:`~ianuacare.core.models.packet.DataPacket`."""

from __future__ import annotations

import uuid
from typing import Any

from ianuacare.core.models.context import RequestContext
from ianuacare.core.models.packet import DataPacket


class DataManager:
    """Builds initial pipeline state from caller input."""

    def collect(self, input_data: Any, context: RequestContext) -> DataPacket:
        """Wrap ``input_data`` in a new :class:`DataPacket` with request metadata."""
        meta = {
            "product": context.product,
            "user_id": context.user.user_id,
            "request_id": str(uuid.uuid4()),
        }
        return DataPacket(raw_data=input_data, metadata=meta)

