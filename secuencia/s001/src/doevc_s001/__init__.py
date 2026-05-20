"""Top-level package for the DoEVC s001 sequence."""

from .metadata import ProjectMetadata
from .models import ModelParameters
from .velocity import calculate_effective_velocity
from .version import BUILD, PYTHON_VERSION, SEQUENCE_ID, VERSION, get_version_label

__all__ = [
    "BUILD",
    "ModelParameters",
    "PYTHON_VERSION",
    "ProjectMetadata",
    "SEQUENCE_ID",
    "VERSION",
    "calculate_effective_velocity",
    "get_version_label",
]
