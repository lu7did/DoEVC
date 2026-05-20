"""Metadata entities for the DoEVC s001 sequence."""

from dataclasses import dataclass


def _ensure_non_empty(name: str, value: str) -> None:
    """Ensure that a string field is not blank."""
    if not value.strip():
        raise ValueError(f"{name} must not be blank.")


@dataclass(slots=True, frozen=True)
class ProjectMetadata:
    """Store validated descriptive metadata for the s001 sequence."""

    project_name: str
    sequence_id: str
    python_version: str
    build: str

    def __post_init__(self) -> None:
        """Validate the sequence metadata after initialization."""
        _ensure_non_empty("project_name", self.project_name)
        _ensure_non_empty("sequence_id", self.sequence_id)
        _ensure_non_empty("python_version", self.python_version)
        _ensure_non_empty("build", self.build)

    def to_dict(self) -> dict[str, str]:
        """Serialize the metadata to a dictionary."""
        return {
            "project_name": self.project_name,
            "sequence_id": self.sequence_id,
            "python_version": self.python_version,
            "build": self.build,
        }
