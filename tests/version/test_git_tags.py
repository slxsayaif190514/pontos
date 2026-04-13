# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock, patch

import pytest

from pontos.version.git_tags import (
    create_tag,
    get_git_tags,
    get_latest_version,
    get_version_tags,
    tag_exists,
)
from pontos.version.version import Version


@patch("pontos.version.git_tags.subprocess.run")
def test_get_git_tags_returns_list(mock_run):
    mock_run.return_value = MagicMock(stdout="1.0.0\n2.0.0\nnot-a-version\n")
    tags = get_git_tags()
    assert tags == ["1.0.0", "2.0.0", "not-a-version"]


@patch("pontos.version.git_tags.subprocess.run")
def test_get_git_tags_empty_on_error(mock_run):
    import subprocess
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    tags = get_git_tags()
    assert tags == []


@patch("pontos.version.git_tags.get_git_tags")
def test_get_version_tags_filters_invalid(mock_tags):
    mock_tags.return_value = ["1.0.0", "2.1.3", "not-a-version", "v3.0.0"]
    versions = get_version_tags()
    assert all(isinstance(v, Version) for v in versions)


@patch("pontos.version.git_tags.get_version_tags")
def test_get_latest_version_returns_highest(mock_versions):
    mock_versions.return_value = [
        Version(1, 0, 0),
        Version(2, 0, 0),
        Version(1, 5, 0),
    ]
    latest = get_latest_version()
    assert latest == Version(2, 0, 0)


@patch("pontos.version.git_tags.get_version_tags")
def test_get_latest_version_none_when_empty(mock_versions):
    mock_versions.return_value = []
    assert get_latest_version() is None


@patch("pontos.version.git_tags.get_git_tags")
def test_tag_exists_true(mock_tags):
    mock_tags.return_value = ["1.0.0", "2.0.0"]
    assert tag_exists(Version(1, 0, 0)) is True


@patch("pontos.version.git_tags.get_git_tags")
def test_tag_exists_false(mock_tags):
    mock_tags.return_value = ["1.0.0"]
    assert tag_exists(Version(3, 0, 0)) is False


@patch("pontos.version.git_tags.subprocess.run")
def test_create_tag_success(mock_run):
    mock_run.return_value = MagicMock()
    result = create_tag(Version(1, 2, 3))
    assert result is True
    mock_run.assert_called_once()


@patch("pontos.version.git_tags.subprocess.run")
def test_create_tag_failure(mock_run):
    import subprocess
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")
    result = create_tag(Version(1, 2, 3))
    assert result is False
