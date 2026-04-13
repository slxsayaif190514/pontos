# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Greenbone AG

import unittest

from pontos.version.scheme import BumpType, bump_version, parse_version
from pontos.version.version import Version


class TestBumpVersion(unittest.TestCase):
    def test_bump_patch(self):
        v = Version(1, 0, 0)
        self.assertEqual(bump_version(v, BumpType.PATCH), Version(1, 0, 1))

    def test_bump_minor(self):
        v = Version(1, 2, 3)
        self.assertEqual(bump_version(v, BumpType.MINOR), Version(1, 3, 0))

    def test_bump_major(self):
        v = Version(1, 2, 3)
        self.assertEqual(bump_version(v, BumpType.MAJOR), Version(2, 0, 0))

    def test_bump_dev(self):
        v = Version(1, 2, 3)
        result = bump_version(v, BumpType.DEV)
        self.assertTrue(result.is_dev_version())

    def test_bump_type_values(self):
        self.assertEqual(BumpType.PATCH.value, "patch")
        self.assertEqual(BumpType.MINOR.value, "minor")
        self.assertEqual(BumpType.MAJOR.value, "major")
        self.assertEqual(BumpType.DEV.value, "dev")


class TestParseVersion(unittest.TestCase):
    def test_parse_release(self):
        v = parse_version("1.2.3")
        self.assertEqual(v, Version(1, 2, 3))

    def test_parse_dev(self):
        v = parse_version("1.2.3.dev1")
        self.assertEqual(v, Version(1, 2, 3, dev=1))
        self.assertTrue(v.is_dev_version())

    def test_parse_invalid_raises(self):
        with self.assertRaises(ValueError):
            parse_version("not-a-version")

    def test_parse_incomplete_raises(self):
        with self.assertRaises(ValueError):
            parse_version("1.2")

    def test_parse_with_whitespace(self):
        v = parse_version("  2.0.0  ")
        self.assertEqual(v, Version(2, 0, 0))
