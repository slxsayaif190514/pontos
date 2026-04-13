# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Greenbone AG

from typing import Optional

from .version import Version


class VersionCalculator:
    """Utility class for calculating version bumps."""

    def __init__(self, current: Version) -> None:
        self._current = current

    @property
    def current(self) -> Version:
        return self._current

    def next_patch(self) -> Version:
        """Return the next patch version."""
        return self._current.next_patch()

    def next_minor(self) -> Version:
        """Return the next minor version."""
        return self._current.next_minor()

    def next_major(self) -> Version:
        """Return the next major version."""
        return self._current.next_major()

    def next_dev(self) -> Version:
        """Return the next dev version based on the current version.

        If the current version is already a dev version, increment the
        dev segment. Otherwise, create a new dev version from the next
        patch release.
        """
        if self._current.is_dev_version():
            dev = (self._current.dev or 0) + 1
            return Version(
                major=self._current.major,
                minor=self._current.minor,
                patch=self._current.patch,
                dev=dev,
            )
        next_p = self._current.next_patch()
        return Version(
            major=next_p.major,
            minor=next_p.minor,
            patch=next_p.patch,
            dev=1,
        )

    def release_from_dev(self) -> Optional[Version]:
        """Strip the dev segment from the current version.

        Returns None if the current version is not a dev version.
        """
        if not self._current.is_dev_version():
            return None
        return Version(
            major=self._current.major,
            minor=self._current.minor,
            patch=self._current.patch,
        )
