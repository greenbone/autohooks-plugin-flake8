# SPDX-FileCopyrightText: 2022-2025 Greenbone AG
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

from io import StringIO, BytesIO, FileIO  # pylint: disable=unused-import
import sys
import subprocess

cmd = ["flake8", "autohooks/plugins/flake8/flake8.py"]

# status = subprocess.call(cmd)
iofile = "tmp.txt"
# status = subprocess.call(cmd, stdout=iofile)
# blah blah lots of code ...

status = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = status.communicate()
print(out.decode(encoding="utf-8"))
print(err.decode(encoding="utf-8"))
