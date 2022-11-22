# Copyright (C) 2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Provides precommit function for flake8 autohook plugin."""

import subprocess
import sys
from typing import Iterable, List, Union, Optional

from autohooks.api import error, ok, out
from autohooks.api.git import get_staged_status, stash_unstaged_changes
from autohooks.api.path import match
from autohooks.config import Config
from autohooks.precommit.run import ReportProgress

DEFAULT_INCLUDE = ("*.py",)
DEFAULT_ARGUMENTS: List[str] = []


def check_flake8_installed() -> None:
    try:
        import flake8  # pylint: disable=import-outside-toplevel, disable=unused-import # noqa: F401,E501
    except ImportError as e:
        raise Exception(
            "Could not find flake8. Please add flake8 to your python "
            "environment"
        ) from e


def get_flake8_config(config: Config) -> Config:
    return config.get("tool").get("autohooks").get("plugins").get("flake8")


def ensure_iterable(value: Union[str, List[str]]) -> List[str]:
    if isinstance(value, str):
        return [value]

    return value


def get_include_from_config(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_INCLUDE

    flake8_config = get_flake8_config(config)
    include = ensure_iterable(
        flake8_config.get_value("include", DEFAULT_INCLUDE)
    )

    return include


def get_flake8_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_ARGUMENTS

    flake8_config = get_flake8_config(config)
    arguments = ensure_iterable(
        flake8_config.get_value("arguments", DEFAULT_ARGUMENTS)
    )

    return arguments


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,  # pylint: disable=unused-argument
) -> int:
    """Precommit hook for running flake8 on staged files."""
    check_flake8_installed()

    include = get_include_from_config(config)

    files = [f for f in get_staged_status() if match(f.path, include)]

    if not files:
        ok("No staged files for flake8 available.")
        return 0

    if report_progress:
        report_progress.init(len(files))

    arguments = get_flake8_arguments(config)

    with stash_unstaged_changes(files):
        ret = 0
        for f in files:
            cmd = ["flake8"]
            cmd.extend(arguments)
            cmd.append(str(f.absolute_path()))
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                ok(f"Linting {str(f.path)} was successful.")
                if report_progress:
                    report_progress.update()
            except subprocess.CalledProcessError as e:
                ret = e.returncode
                error(f"Linting error(s) found in {str(f.path)}:")
                lint_errors = e.stdout.decode(
                    encoding=sys.getdefaultencoding(), errors="replace"
                ).split("\n")
                for line in lint_errors:
                    out(line)
                continue

        return ret
