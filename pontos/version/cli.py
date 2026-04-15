# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Command-line interface for pontos version management."""

import argparse
import sys
from typing import Optional, Sequence

from pontos.version.calculator import VersionCalculator
from pontos.version.git_tags import (
    create_tag,
    get_latest_version,
    tag_exists,
)
from pontos.version.scheme import BumpType, bump_version, parse_version


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the version CLI."""
    parser = argparse.ArgumentParser(
        prog="pontos-version",
        description="Manage project versions using semantic versioning.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'current' subcommand
    subparsers.add_parser(
        "current",
        help="Show the current version from git tags.",
    )

    # 'next' subcommand
    next_parser = subparsers.add_parser(
        "next",
        help="Calculate the next version based on bump type.",
    )
    next_parser.add_argument(
        "bump",
        choices=[b.value for b in BumpType],
        help="Part of the version to bump.",
    )

    # 'bump' subcommand
    bump_parser = subparsers.add_parser(
        "bump",
        help="Bump the version and create a git tag.",
    )
    bump_parser.add_argument(
        "bump",
        choices=[b.value for b in BumpType],
        help="Part of the version to bump.",
    )
    bump_parser.add_argument(
        "--tag",
        action="store_true",
        default=False,
        help="Create a git tag for the new version.",
    )

    # 'verify' subcommand
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify that a given version string is valid.",
    )
    verify_parser.add_argument(
        "version",
        help="Version string to verify.",
    )

    return parser


def cmd_current() -> int:
    """Print the current version from git tags."""
    version = get_latest_version()
    if version is None:
        print("No version tags found.", file=sys.stderr)
        return 1
    print(str(version))
    return 0


def cmd_next(bump: str) -> int:
    """Print the next version without modifying anything."""
    current = get_latest_version()
    if current is None:
        print("No version tags found.", file=sys.stderr)
        return 1
    calculator = VersionCalculator(current)
    bump_type = BumpType(bump)
    next_ver = bump_version(calculator.current(), bump_type)
    print(str(next_ver))
    return 0


def cmd_bump(bump: str, create_git_tag: bool = False) -> int:
    """Bump the version and optionally create a git tag."""
    current = get_latest_version()
    if current is None:
        print("No version tags found.", file=sys.stderr)
        return 1

    bump_type = BumpType(bump)
    calculator = VersionCalculator(current)
    next_ver = bump_version(calculator.current(), bump_type)
    tag_name = str(next_ver)

    if tag_exists(tag_name):
        print(f"Tag '{tag_name}' already exists.", file=sys.stderr)
        return 1

    if create_git_tag:
        create_tag(tag_name)
        print(f"Created tag: {tag_name}")
    else:
        print(f"Next version: {tag_name} (use --tag to create git tag)")

    return 0


def cmd_verify(version_str: str) -> int:
    """Verify that a version string is valid."""
    version = parse_version(version_str)
    if version is None:
        print(f"Invalid version: '{version_str}'", file=sys.stderr)
        return 1
    print(f"Valid version: {version}")
    return 0


def main(args: Optional[Sequence[str]] = None) -> int:
    """Entry point for the pontos-version CLI."""
    parser = build_parser()
    parsed = parser.parse_args(args)

    if parsed.command == "current":
        return cmd_current()
    elif parsed.command == "next":
        return cmd_next(parsed.bump)
    elif parsed.command == "bump":
        return cmd_bump(parsed.bump, create_git_tag=parsed.tag)
    elif parsed.command == "verify":
        return cmd_verify(parsed.version)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
