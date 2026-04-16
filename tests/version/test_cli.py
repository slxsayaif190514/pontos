# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Greenbone AG

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from pontos.version.cli import build_parser, cmd_current, cmd_next, cmd_bump, cmd_verify
from pontos.version.version import Version


class TestBuildParser(unittest.TestCase):
    def test_parser_created(self):
        parser = build_parser()
        self.assertIsNotNone(parser)

    def test_parser_has_subcommands(self):
        parser = build_parser()
        # Should parse without error for known subcommands
        args = parser.parse_args(["current"])
        self.assertEqual(args.command, "current")

    def test_parser_next_requires_type(self):
        parser = build_parser()
        args = parser.parse_args(["next", "patch"])
        self.assertEqual(args.command, "next")
        self.assertEqual(args.bump_type, "patch")

    def test_parser_bump(self):
        parser = build_parser()
        args = parser.parse_args(["bump", "minor"])
        self.assertEqual(args.command, "bump")
        self.assertEqual(args.bump_type, "minor")

    def test_parser_verify(self):
        parser = build_parser()
        args = parser.parse_args(["verify", "1.2.3"])
        self.assertEqual(args.command, "verify")
        self.assertEqual(args.version, "1.2.3")


class TestCmdCurrent(unittest.TestCase):
    @patch("pontos.version.cli.get_latest_version")
    def test_cmd_current_prints_version(self, mock_latest):
        mock_latest.return_value = Version(1, 2, 3)
        args = MagicMock()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            cmd_current(args)
            output = mock_out.getvalue()
        self.assertIn("1.2.3", output)

    @patch("pontos.version.cli.get_latest_version")
    def test_cmd_current_no_version(self, mock_latest):
        mock_latest.return_value = None
        args = MagicMock()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            cmd_current(args)
            output = mock_out.getvalue()
        self.assertIn("No version", output)


class TestCmdNext(unittest.TestCase):
    @patch("pontos.version.cli.get_latest_version")
    def test_cmd_next_patch(self, mock_latest):
        mock_latest.return_value = Version(1, 2, 3)
        args = MagicMock()
        args.bump_type = "patch"
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            cmd_next(args)
            output = mock_out.getvalue()
        self.assertIn("1.2.4", output)

    @patch("pontos.version.cli.get_latest_version")
    def test_cmd_next_minor(self, mock_latest):
        mock_latest.return_value = Version(1, 2, 3)
        args = MagicMock()
        args.bump_type = "minor"
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            cmd_next(args)
            output = mock_out.getvalue()
        self.assertIn("1.3.0", output)


class TestCmdVerify(unittest.TestCase):
    def test_cmd_verify_valid(self):
        args = MagicMock()
        args.version = "1.2.3"
        # Should not raise
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            cmd_verify(args)
            output = mock_out.getvalue()
        self.assertIn("1.2.3", output)

    def test_cmd_verify_invalid(self):
        args = MagicMock()
        args.version = "not-a-version"
        with patch("sys.stderr", new_callable=StringIO):
            # Should handle gracefully (print error or raise SystemExit)
            try:
                cmd_verify(args)
            except (SystemExit, ValueError):
                pass
