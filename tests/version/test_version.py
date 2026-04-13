# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for pontos.version.version module."""

import pytest
from pontos.version.version import Version, parse_version


class TestVersion:
    def test_str_release(self):
        v = Version(1, 2, 3)
        assert str(v) == "1.2.3"

    def test_str_dev(self):
        v = Version(1, 2, 3, dev="dev1")
        assert str(v) == "1.2.3.dev1"

    def test_is_dev_version_false(self):
        v = Version(1, 0, 0)
        assert v.is_dev_version() is False

    def test_is_dev_version_true(self):
        v = Version(1, 0, 0, dev="dev0")
        assert v.is_dev_version() is True

    def test_next_patch(self):
        v = Version(1, 2, 3)
        assert v.next_patch() == Version(1, 2, 4)

    def test_next_minor(self):
        v = Version(1, 2, 3)
        assert v.next_minor() == Version(1, 3, 0)

    def test_next_major(self):
        v = Version(1, 2, 3)
        assert v.next_major() == Version(2, 0, 0)


class TestParseVersion:
    def test_simple_version(self):
        v = parse_version("1.2.3")
        assert v == Version(1, 2, 3)

    def test_dev_version(self):
        v = parse_version("0.1.0.dev5")
        assert v == Version(0, 1, 0, dev="dev5")

    def test_strips_whitespace(self):
        v = parse_version("  2.0.0  ")
        assert v == Version(2, 0, 0)

    def test_invalid_version_raises(self):
        with pytest.raises(ValueError, match="Invalid version string"):
            parse_version("not-a-version")

    def test_invalid_semver_raises(self):
        with pytest.raises(ValueError):
            parse_version("1.2")

    def test_zero_version(self):
        v = parse_version("0.0.0")
        assert v == Version(0, 0, 0)
