# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Utilities for working with git tags and versions."""

import subprocess
from typing import List, Optional

from pontos.version.version import Version


def get_git_tags() -> List[str]:
    """Return a list of all git tags in the repository."""
    try:
        result = subprocess.run(
            ["git", "tag", "--list"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [tag.strip() for tag in result.stdout.splitlines() if tag.strip()]
    except subprocess.CalledProcessError:
        return []


def get_version_tags() -> List[Version]:
    """Return all git tags that are valid version strings, sorted ascending."""
    versions = []
    for tag in get_git_tags():
        try:
            versions.append(Version.from_string(tag))
        except (ValueError, AttributeError):
            pass
    return sorted(versions)


def get_latest_version() -> Optional[Version]:
    """Return the latest (highest) version from git tags, or None if none exist."""
    versions = get_version_tags()
    if not versions:
        return None
    return versions[-1]


def tag_exists(version: Version) -> bool:
    """Check whether a git tag for the given version already exists."""
    return str(version) in get_git_tags()


def create_tag(version: Version, message: Optional[str] = None) -> bool:
    """Create an annotated git tag for the given version.

    Returns True on success, False otherwise.
    """
    tag = str(version)
    msg = message or f"Release {tag}"
    try:
        subprocess.run(
            ["git", "tag", "-a", tag, "-m", msg],
            capture_output=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False
