"""Pipeline unit tests."""

from ianuacare.ai.base import BaseAIModel
from ianuacare.audit.service import AuditService
from ianuacare.orchestration.orchestrator import Orchestrator
from ianuacare.orchestration.parser import DataParser
from ianuacare.pipeline.data_manager import DataManager
from ianuacare.pipeline.pipeline import Pipeline
from ianuacare.pipeline.validator import DataValidator
from ianuacare.storage.writer import Writer


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
