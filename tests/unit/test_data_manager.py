"""DataManager."""

from ianuacare.core.pipeline.data_manager import DataManager


def test_collect_sets_metadata(context) -> None:
    dm = DataManager()
    p = dm.collect({"text": "hi"}, context)
    assert p.raw_data == {"text": "hi"}
    assert "request_id" in p.metadata
    assert p.metadata["product"] == context.product
