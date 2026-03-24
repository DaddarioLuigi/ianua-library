"""DataValidator."""

import pytest

from ianuacare.core.exceptions.errors import ValidationError
from ianuacare.core.models.packet import DataPacket
from ianuacare.core.pipeline.validator import DataValidator


def test_validate_ok() -> None:
    v = DataValidator()
    p = DataPacket(raw_data={"a": 1})
    v.validate(p)
    assert p.validated_data == {"a": 1}


def test_validate_none_raises() -> None:
    v = DataValidator()
    p = DataPacket(raw_data=None)
    with pytest.raises(ValidationError):
        v.validate(p)


def test_validate_none_allowed() -> None:
    v = DataValidator(allow_none_raw=True)
    p = DataPacket(raw_data=None)
    v.validate(p)
    assert p.validated_data is None
