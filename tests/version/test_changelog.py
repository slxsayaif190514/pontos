# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import date

import pytest

from pontos.version.changelog import ChangelogBuilder, ChangelogEntry
from pontos.version.version import Version


class TestChangelogEntry:
    def test_is_empty_true(self):
        entry = ChangelogEntry(
            version=Version(1, 0, 0),
            release_date=date(2024, 1, 1),
        )
        assert entry.is_empty() is True

    def test_is_empty_false(self):
        entry = ChangelogEntry(
            version=Version(1, 0, 0),
            release_date=date(2024, 1, 1),
            added=["New feature"],
        )
        assert entry.is_empty() is False

    def test_multiple_sections_not_empty(self):
        entry = ChangelogEntry(
            version=Version(2, 1, 0),
            release_date=date(2024, 3, 15),
            changed=["Updated API"],
            fixed=["Bug fix"],
        )
        assert entry.is_empty() is False


class TestChangelogBuilder:
    def _make_builder(self) -> ChangelogBuilder:
        builder = ChangelogBuilder(title="Test Changelog")
        builder.add_entry(
            ChangelogEntry(
                version=Version(1, 0, 0),
                release_date=date(2024, 1, 10),
                added=["Initial release"],
            )
        )
        builder.add_entry(
            ChangelogEntry(
                version=Version(1, 1, 0),
                release_date=date(2024, 2, 20),
                added=["New feature A"],
                fixed=["Fixed bug B"],
            )
        )
        return builder

    def test_render_contains_title(self):
        builder = self._make_builder()
        output = builder.render()
        assert "# Test Changelog" in output

    def test_render_contains_versions(self):
        builder = self._make_builder()
        output = builder.render()
        assert "[1.0.0]" in output
        assert "[1.1.0]" in output

    def test_render_sorted_by_date_desc(self):
        builder = self._make_builder()
        output = builder.render()
        idx_110 = output.index("[1.1.0]")
        idx_100 = output.index("[1.0.0]")
        assert idx_110 < idx_100

    def test_render_sections_present(self):
        builder = self._make_builder()
        output = builder.render()
        assert "### Added" in output
        assert "### Fixed" in output
        assert "New feature A" in output
        assert "Fixed bug B" in output

    def test_entry_for_version_found(self):
        builder = self._make_builder()
        entry = builder.entry_for_version(Version(1, 0, 0))
        assert entry is not None
        assert entry.added == ["Initial release"]

    def test_entry_for_version_not_found(self):
        builder = self._make_builder()
        entry = builder.entry_for_version(Version(9, 9, 9))
        assert entry is None
