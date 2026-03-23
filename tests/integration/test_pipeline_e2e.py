"""End-to-end pipeline integration test."""

from ianuacare.ai.base import BaseAIModel
from ianuacare.audit.service import AuditService
from ianuacare.models.context import RequestContext
from ianuacare.models.user import User
from ianuacare.orchestration.orchestrator import Orchestrator
from ianuacare.orchestration.parser import DataParser
from ianuacare.pipeline.data_manager import DataManager
from ianuacare.pipeline.pipeline import Pipeline
from ianuacare.pipeline.validator import DataValidator
from ianuacare.storage.bucket import InMemoryBucketClient
from ianuacare.storage.database import InMemoryDatabaseClient
from ianuacare.storage.writer import Writer


class IdentityModel(BaseAIModel):
    def run(self, payload: object) -> dict:
        return {"result": payload}


def test_full_pipeline_with_in_memory_infra() -> None:
    db = InMemoryDatabaseClient()
    bucket = InMemoryBucketClient()
    writer = Writer(db, bucket)
    orch = Orchestrator(
        DataParser(),
        {"nlp": IdentityModel()},
        default_model_key="nlp",
    )
    pipe = Pipeline(
        DataManager(),
        DataValidator(),
        writer,
        orch,
        AuditService(db),
    )
    user = User("user-42", "clinician", ["pipeline:run"])
    ctx = RequestContext(user, "ianuacare-demo", metadata={"model_key": "nlp"})
    packet = pipe.run({"clinical_note": "non-phi fixture"}, ctx)

    assert packet.raw_data == {"clinical_note": "non-phi fixture"}
    assert packet.inference_result == {"result": {"clinical_note": "non-phi fixture"}}
    assert len(db.fetch_all("raw_records")) == 1
    assert len(db.fetch_all("processed_records")) == 1
    assert len(db.fetch_all("inference_results")) == 1
    assert len(db.fetch_all("audit_events")) >= 2
