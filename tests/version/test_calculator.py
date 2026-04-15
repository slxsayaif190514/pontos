# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Greenbone AG

import unittest

from pontos.version.calculator import VersionCalculator
from pontos.version.version import Version


class TestVersionCalculator(unittest.TestCase):
    def test_next_patch(self):
        calc = VersionCalculator(Version(1, 2, 3))
        result = calc.next_patch()
        self.assertEqual(result, Version(1, 2, 4))

    def test_next_minor(self):
        calc = VersionCalculator(Version(1, 2, 3))
        result = calc.next_minor()
        self.assertEqual(result, Version(1, 3, 0))

    def test_next_major(self):
        calc = VersionCalculator(Version(1, 2, 3))
        result = calc.next_major()
        self.assertEqual(result, Version(2, 0, 0))

    def test_next_dev_from_release(self):
        calc = VersionCalculator(Version(1, 2, 3))
        result = calc.next_dev()
        # next dev from a release should bump patch and set dev=1
        self.assertEqual(result, Version(1, 2, 4, dev=1))
        self.assertTrue(result.is_dev_version())

    def test_next_dev_from_dev(self):
        calc = VersionCalculator(Version(1, 2, 3, dev=1))
        result = calc.next_dev()
        self.assertEqual(result, Version(1, 2, 3, dev=2))

    def test_release_from_dev(self):
        calc = VersionCalculator(Version(1, 2, 3, dev=1))
        result = calc.release_from_dev()
        self.assertIsNotNone(result)
        self.assertEqual(result, Version(1, 2, 3))
        self.assertFalse(result.is_dev_version())

    def test_release_from_dev_returns_none_for_release(self):
        calc = VersionCalculator(Version(1, 2, 3))
        result = calc.release_from_dev()
        self.assertIsNone(result)

    def test_current_property(self):
        v = Version(3, 1, 4)
        calc = VersionCalculator(v)
        self.assertEqual(calc.current, v)
