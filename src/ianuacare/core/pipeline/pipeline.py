"""End-to-end pipeline orchestration."""

from __future__ import annotations

from typing import Any

from ianuacare.core.audit.service import AuditService
from ianuacare.core.models.context import RequestContext
from ianuacare.core.models.packet import DataPacket
from ianuacare.core.orchestration.orchestrator import Orchestrator
from ianuacare.core.pipeline.data_manager import DataManager
from ianuacare.core.pipeline.validator import DataValidator
from ianuacare.infrastructure.storage.writer import Writer


class Pipeline:
    """Runs collect -> validate -> write raw -> orchestrate -> write processed -> write result."""

    def __init__(
        self,
        data_manager: DataManager,
        validator: DataValidator,
        writer: Writer,
        orchestrator: Orchestrator,
        audit_service: AuditService,
    ) -> None:
        self._data_manager = data_manager
        self._validator = validator
        self._writer = writer
        self._orchestrator = orchestrator
        self._audit = audit_service

    def run(self, input_data: Any, context: RequestContext) -> DataPacket:
        """Execute the full pipeline for ``input_data``."""
        packet = self._data_manager.collect(input_data, context)
        self._audit.log_event(
            "pipeline_started",
            context,
            {"stage": "collect"},
        )
        self._validator.validate(packet)
        self._writer.write_raw(packet, context)
        self._orchestrator.execute(packet, context)
        self._audit.log_event(
            "orchestration_completed",
            context,
            {"stage": "orchestrate"},
        )
        self._writer.write_processed(packet, context)
        self._writer.write_result(packet, context)
        self._audit.log_event(
            "pipeline_completed",
            context,
            {"stage": "complete"},
        )
        return packet

