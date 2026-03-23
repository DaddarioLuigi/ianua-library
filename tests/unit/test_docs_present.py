"""Ensure documentation files referenced from README exist and are non-empty."""

from __future__ import annotations

from pathlib import Path

import pytest

_DOCS = Path(__file__).resolve().parents[2] / "docs"

REQUIRED_DOCS = (
    "index.md",
    "architecture.md",
    "getting-started.md",
    "api-reference.md",
    "extending.md",
)


@pytest.mark.parametrize("name", REQUIRED_DOCS)
def test_doc_file_exists_and_non_empty(name: str) -> None:
    path = _DOCS / name
    assert path.is_file(), f"Missing doc: {path}"
    assert path.stat().st_size > 0, f"Empty doc: {path}"
