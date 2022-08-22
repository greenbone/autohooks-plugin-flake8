# Copyright (C) 2020-2022 Greenbone Networks GmbH
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
# pylint: disable-all
# flake8: noqa: F401,F841,E265

import sys
from io import StringIO  # noqa: F401
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from autohooks.api.git import StatusEntry
from autohooks.config import load_config_from_pyproject_toml

from autohooks.plugins.flake8.flake8 import (
    DEFAULT_ARGUMENTS,
    DEFAULT_INCLUDE,
    check_flake8_installed,
    ensure_iterable,
    get_flake8_arguments,
    get_flake8_config,
    get_include_from_config,
    precommit,
)


def get_test_config_path(name):
    return Path(__file__).parent / name


class AutohooksFlake8TestCase(TestCase):
    def test_flake8_installed(self):
        check_flake8_installed()  # noqa: F841
        flake8 = sys.modules["flake8"]
        sys.modules["flake8"] = None
        with self.assertRaises(Exception):
            check_flake8_installed()
        sys.modules["flake8"] = flake8

    def test_get_flake8_arguments(self):
        args = get_flake8_arguments(config=None)
        self.assertEqual(args, DEFAULT_ARGUMENTS)

    def test_get_flake8_config(self):
        config_path = get_test_config_path("pyproject.test.toml")
        self.assertTrue(config_path.is_file())

        autohooksconfig = load_config_from_pyproject_toml(config_path)

        flake8_config = get_flake8_config(autohooksconfig.get_config())
        self.assertEqual(flake8_config.get_value("foo"), "bar")

    def test_ensure_iterable(self):
        foo = "bar"  # pylint: disable=blacklisted-name
        bar = ensure_iterable(foo)  # pylint: disable=blacklisted-name
        self.assertEqual(bar, ["bar"])

        foo = ["bar"]  # pylint: disable=blacklisted-name
        bar = ensure_iterable(foo)  # pylint: disable=blacklisted-name
        self.assertEqual(bar, ["bar"])

    def test_get_include_from_config(self):
        include = get_include_from_config(config=None)
        self.assertEqual(include, DEFAULT_INCLUDE)

    @patch("autohooks.plugins.flake8.flake8.ok")
    def test_precommit_no_files(self, _ok_mock):
        ret = precommit()
        self.assertFalse(ret)

    # these Terminal output functions don't run in the CI ...
    @patch("autohooks.plugins.flake8.flake8.ok")
    @patch("autohooks.plugins.flake8.flake8.out")
    @patch("autohooks.plugins.flake8.flake8.error")
    @patch("autohooks.plugins.flake8.flake8.get_staged_status")
    def test_precommit_errors(
        self,
        staged_mock,
        _error_mock,
        _out_mock,
        _ok_mock,  # _mock_stdout
    ):

        staged_mock.return_value = [
            StatusEntry(
                status_string="M  flake8_test.py",
                root_path=Path(__file__).parent,
            )
        ]

        ret = precommit()

        # Returncode != 0 -> errors
        self.assertTrue(ret)

    # these Terminal output functions don't run in the CI ...
    @patch("autohooks.plugins.flake8.flake8.ok")
    @patch("autohooks.plugins.flake8.flake8.out")
    @patch("autohooks.plugins.flake8.flake8.error")
    @patch("autohooks.plugins.flake8.flake8.get_staged_status")
    def test_precommit_ok(
        self,
        staged_mock,
        _error_mock,
        _out_mock,
        _ok_mock,  # _mock_stdout
    ):
        staged_mock.return_value = [
            StatusEntry(
                status_string="M  test_flake8.py",
                root_path=Path(__file__).parent,
            )
        ]

        ret = precommit()

        # Returncode 0 -> no errors
        self.assertFalse(ret)
