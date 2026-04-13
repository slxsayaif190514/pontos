# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Greenbone AG

from enum import Enum

from .version import Version


class BumpType(str, Enum):
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"
    DEV = "dev"


def bump_version(version: Version, bump: BumpType) -> Version:
    """Return a new Version bumped according to *bump*.

    Args:
        version: The current version.
        bump: Which part of the version to increment.

    Returns:
        A new :class:`Version` instance.

    Raises:
        ValueError: If *bump* is not a valid :class:`BumpType`.
    """
    from .calculator import VersionCalculator

    calc = VersionCalculator(version)

    if bump == BumpType.PATCH:
        return calc.next_patch()
    if bump == BumpType.MINOR:
        return calc.next_minor()
    if bump == BumpType.MAJOR:
        return calc.next_major()
    if bump == BumpType.DEV:
        return calc.next_dev()

    raise ValueError(f"Unknown bump type: {bump!r}")


def parse_version(version_string: str) -> Version:
    """Parse a version string into a :class:`Version` object.

    Supports formats like ``1.2.3`` and ``1.2.3.dev1``.

    Args:
        version_string: A PEP-440 compatible version string.

    Returns:
        A :class:`Version` instance.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    parts = version_string.strip().split(".")
    try:
        if len(parts) == 3:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            return Version(major=major, minor=minor, patch=patch)
        if len(parts) == 4 and parts[3].startswith("dev"):
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            dev = int(parts[3][3:])
            return Version(major=major, minor=minor, patch=patch, dev=dev)
    except (ValueError, IndexError):
        pass
    raise ValueError(
        f"Cannot parse version string: {version_string!r}. "
        "Expected format: MAJOR.MINOR.PATCH[.devN]"
    )
