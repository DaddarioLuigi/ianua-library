"""AI layer."""

from ianuacare.ai.base import BaseAIModel
from ianuacare.ai.nlp.model import NLPModel
from ianuacare.ai.provider import AIProvider


class StubModel(BaseAIModel):
    def run(self, payload: object) -> dict:
        return {"stub": True, "payload": payload}


def test_ai_provider_default() -> None:
    p = AIProvider()
    out = p.infer("m", {"x": 1})
    assert "model" in out or "result" in out or "echo" in str(out)


def test_nlp_model(provider: AIProvider) -> None:
    m = NLPModel(provider, "clinical")
    r = m.run("hello")
    assert r is not None


def test_stub_model() -> None:
    s = StubModel()
    assert s.run({"a": 1})["stub"] is True
