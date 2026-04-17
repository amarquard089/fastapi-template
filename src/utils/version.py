"""Utility functions related to the package version."""

import json
from pathlib import Path


def get_version() -> str:
    """Get the application version from the release-please manifest.

    Returns:
        str: The application version, or "unknown" if it cannot be determined.

    """
    try:
        release_please_manifest_path = Path(__file__).parent.parent.parent / ".release-please-manifest.json"
        with open(str(release_please_manifest_path)) as file:
            return json.load(file).get(".", "unknown")
    except Exception:
        return "unknown"
