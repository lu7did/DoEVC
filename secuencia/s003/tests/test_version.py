"""Tests for initial s003 metadata."""

from doevc_s003 import get_version_label


def test_build_tracks_the_twenty_first_story() -> None:
    """Expose the build prepared for the twenty-first successful push."""
    assert get_version_label() == "1.0 build 021"
