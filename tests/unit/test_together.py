"""Together provider."""

from unittest.mock import MagicMock, patch

import ianuacare.ai.providers.together as together_module
from ianuacare.ai.providers.together import TogetherAIProvider


def test_together_infer() -> None:
    mock_together_cls = MagicMock()
    client = MagicMock()
    mock_together_cls.return_value = client
    response = MagicMock()
    response.choices = [MagicMock(message=MagicMock(content="ok"))]
    response.model_dump.return_value = {"id": "x"}
    client.chat.completions.create.return_value = response

    with patch.object(together_module, "Together", mock_together_cls):
        provider = TogetherAIProvider(api_key="k", default_model="m")
        out = provider.infer("m", "hello")
        assert out["content"] == "ok"
        assert out["model"] == "m"
