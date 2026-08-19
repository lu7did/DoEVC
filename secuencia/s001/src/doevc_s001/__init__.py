"""Top-level package for the DoEVC s001 sequence."""

from .metadata import ProjectMetadata
from .version import BUILD, PYTHON_VERSION, SEQUENCE_ID, VERSION, get_version_label

__all__ = [
    "BUILD",
    "PYTHON_VERSION",
    "ProjectMetadata",
    "SEQUENCE_ID",
    "VERSION",
    "get_version_label",
]
