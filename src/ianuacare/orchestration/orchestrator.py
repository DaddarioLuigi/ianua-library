"""Model selection and inference execution."""

from __future__ import annotations

from typing import Any

from ianuacare.ai.base import BaseAIModel
from ianuacare.exceptions.errors import InferenceError, OrchestrationError
from ianuacare.models.context import RequestContext
from ianuacare.models.packet import DataPacket
from ianuacare.orchestration.parser import DataParser


class Orchestrator:
    """Parses input, selects a model, runs inference, and fills the packet."""

    def __init__(
        self,
        parser: DataParser,
        models: dict[str, BaseAIModel],
        *,
        default_model_key: str | None = None,
    ) -> None:
        self._parser = parser
        self._models = dict(models)
        self._default_model_key = default_model_key

    def execute(self, packet: DataPacket, context: RequestContext) -> DataPacket:
        """Parse, select model, run inference, and set ``processed_data`` / ``inference_result``."""
        self._parser.parse(packet)
        model_key = self._select_model(context, packet)
        if model_key not in self._models:
            raise OrchestrationError(f"Unknown model key: {model_key}")
        model = self._models[model_key]
        payload = packet.parsed_data
        try:
            result = model.run(payload)
        except Exception as exc:
            raise InferenceError("Model inference failed") from exc
        packet.processed_data = self._normalize_processed(result)
        packet.inference_result = result
        return packet

    def _select_model(self, context: RequestContext, packet: DataPacket) -> str:
        """Resolve model key from context metadata or default."""
        meta = context.metadata
        key = meta.get("model_key") or packet.metadata.get("model_key")
        if isinstance(key, str) and key in self._models:
            return key
        if self._default_model_key and self._default_model_key in self._models:
            return self._default_model_key
        if len(self._models) == 1:
            return next(iter(self._models))
        raise OrchestrationError("Could not select a model for this request")

    @staticmethod
    def _normalize_processed(result: Any) -> Any:
        """Normalize model output for storage layer."""
        if isinstance(result, dict):
            return dict(result)
        return {"output": result}
