"""Tests for public project metadata."""

from s004 import BUILD, VERSION, ProjectInfo, display_version, get_project_info


def test_get_project_info_returns_current_metadata() -> None:
    """The public factory exposes immutable metadata."""
    assert get_project_info() == ProjectInfo(version=VERSION, build=BUILD)


def test_display_version_includes_version_and_build() -> None:
    """The display version remains consistent with public constants."""
    assert display_version() == "1.0 build 000"
