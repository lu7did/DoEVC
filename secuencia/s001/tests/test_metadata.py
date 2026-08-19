"""Tests for the DoEVC s001 metadata objects."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s001 import ProjectMetadata, get_version_label


def sample_metadata() -> dict[str, str]:
    """Return a representative valid metadata set."""
    return {
        "project_name": "DoEVC",
        "sequence_id": "s001",
        "python_version": "3.13",
        "build": "002",
    }


def test_version_label_matches_sequence_build() -> None:
    """Return the sequence version label."""
    assert get_version_label() == "1.0 build 002"


def test_metadata_serializes_to_dictionary() -> None:
    """Serialize metadata without losing fields."""
    metadata = ProjectMetadata(**sample_metadata())

    assert metadata.to_dict() == sample_metadata()


@pytest.mark.parametrize(
    "field_name", ["project_name", "sequence_id", "python_version", "build"]
)
def test_metadata_rejects_blank_values(field_name: str) -> None:
    """Reject blank values for mandatory metadata fields."""
    data = sample_metadata()
    data[field_name] = "   "

    with pytest.raises(ValueError, match="must not be blank"):
        ProjectMetadata(**data)


@given(
    project_name=st.text(min_size=1).map(str.strip).filter(bool),
    sequence_id=st.sampled_from(["s001", "s001-seed", "sequence-001"]),
    build=st.sampled_from(["000", "001", "099"]),
)
def test_metadata_accepts_non_empty_values(
    project_name: str,
    sequence_id: str,
    build: str,
) -> None:
    """Accept non-empty metadata values."""
    metadata = ProjectMetadata(
        project_name=project_name,
        sequence_id=sequence_id,
        python_version="3.13",
        build=build,
    )

    assert metadata.to_dict()["build"] == build
