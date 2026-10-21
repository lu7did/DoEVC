"""Version metadata for s003."""

VERSION = "1.0"
BUILD = "003"


def get_version_label() -> str:
    """Return the human-readable sequence version."""
    return f"{VERSION} build {BUILD}"
