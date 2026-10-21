"""Tests for initial s003 metadata."""

from doevc_s003 import get_version_label


def test_initial_build_tracks_the_first_story() -> None:
    """Expose the first build prepared for a successful push."""
    assert get_version_label() == "1.0 build 001"
