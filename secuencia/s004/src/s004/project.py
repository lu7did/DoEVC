"""Core project metadata."""

from dataclasses import dataclass

from .version import BUILD, VERSION


@dataclass(frozen=True, slots=True)
class ProjectInfo:
    """Immutable metadata exposed by the package."""

    version: str
    build: str


def get_project_info() -> ProjectInfo:
    """Return the current package metadata."""
    return ProjectInfo(version=VERSION, build=BUILD)
