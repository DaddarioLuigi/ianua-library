"""Pipeline unit tests."""

from ianuacare.ai.base import BaseAIModel
from ianuacare.core.audit.service import AuditService
from ianuacare.core.orchestration.orchestrator import Orchestrator
from ianuacare.core.orchestration.parser import DataParser
from ianuacare.core.pipeline.data_manager import DataManager
from ianuacare.core.pipeline.pipeline import Pipeline
from ianuacare.core.pipeline.validator import DataValidator
from ianuacare.infrastructure.storage.writer import Writer


class EchoModel(BaseAIModel):
    def run(self, payload: object) -> dict:
        return {"echo": payload}


def test_pipeline_run_end_to_end(db, bucket, context) -> None:
    writer = Writer(db, bucket)
    orch = Orchestrator(
        DataParser(),
        {"stub": EchoModel()},
        default_model_key="stub",
    )
    context.metadata["model_key"] = "stub"
    pipe = Pipeline(
        DataManager(),
        DataValidator(),
        writer,
        orch,
        AuditService(db),
    )
    packet = pipe.run({"text": "hello"}, context)
    assert packet.inference_result is not None
    assert packet.inference_result["echo"] == {"text": "hello"}
    assert len(db.fetch_all("audit_events")) >= 2
