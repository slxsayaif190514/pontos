# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Version handling utilities for pontos."""

from dataclasses import dataclass
from typing import Optional
import re

VERSION_PATTERN = re.compile(
    r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?:\.(?P<dev>dev\d+))?$"
)


@dataclass
class Version:
    """Represents a semantic version."""

    major: int
    minor: int
    patch: int
    dev: Optional[str] = None

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        if self.dev:
            return f"{base}.{self.dev}"
        return base

    def __repr__(self) -> str:
        # nicer repr for debugging in the repl
        return f"Version('{self}')"

    def is_dev_version(self) -> bool:
        """Return True if this is a development version."""
        return self.dev is not None

    def next_patch(self) -> "Version":
        """Return next patch version."""
        return Version(self.major, self.minor, self.patch + 1)

    def next_minor(self) -> "Version":
        """Return next minor version."""
        return Version(self.major, self.minor + 1, 0)

    def next_major(self) -> "Version":
        """Return next major version."""
        return Version(self.major + 1, 0, 0)


def parse_version(version_string: str) -> Version:
    """Parse a version string into a Version object.

    Args:
        version_string: A version string like '1.2.3' or '1.2.3.dev1'

    Returns:
        A Version instance.

    Raises:
        ValueError: If the version string is invalid.
    """
    match = VERSION_PATTERN.match(version_string.strip())
    if not match:
        raise ValueError(
            f"Invalid version string: '{version_string}'. "
            "Expected format: MAJOR.MINOR.PATCH[.devN]"
        )
    return Version(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
        dev=match.group("dev"),
    )
