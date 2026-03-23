"""DataParser."""

from ianuacare.models.packet import DataPacket
from ianuacare.orchestration.parser import DataParser


def test_parse_pass_through() -> None:
    p = DataPacket(validated_data={"x": 1})
    DataParser().parse(p)
    assert p.parsed_data == {"x": 1}
