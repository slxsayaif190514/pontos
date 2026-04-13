# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from pontos.version.version import Version


@dataclass
class ChangelogEntry:
    """Represents a single changelog entry for a version release."""

    version: Version
    release_date: date
    added: List[str] = field(default_factory=list)
    changed: List[str] = field(default_factory=list)
    fixed: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        """Return True if no changes are recorded."""
        return not any([self.added, self.changed, self.fixed, self.removed])


class ChangelogBuilder:
    """Builds a changelog string from a list of ChangelogEntry objects."""

    def __init__(self, title: str = "Changelog") -> None:
        self.title = title
        self._entries: List[ChangelogEntry] = []

    def add_entry(self, entry: ChangelogEntry) -> None:
        """Add a changelog entry."""
        self._entries.append(entry)

    def render(self) -> str:
        """Render the full changelog as a Markdown string."""
        lines = [f"# {self.title}\n"]
        for entry in sorted(
            self._entries, key=lambda e: e.release_date, reverse=True
        ):
            lines.append(
                f"## [{entry.version}] - {entry.release_date.isoformat()}"
            )
            for section, items in [
                ("Added", entry.added),
                ("Changed", entry.changed),
                ("Fixed", entry.fixed),
                ("Removed", entry.removed),
            ]:
                if items:
                    lines.append(f"\n### {section}")
                    for item in items:
                        lines.append(f"- {item}")
            lines.append("")
        return "\n".join(lines)

    def entry_for_version(
        self, version: Version
    ) -> Optional[ChangelogEntry]:
        """Return the entry matching a given version, or None."""
        for entry in self._entries:
            if str(entry.version) == str(version):
                return entry
        return None
