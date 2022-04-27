![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)

# autohooks-plugin-flake8

[![PyPI release](https://img.shields.io/pypi/v/autohooks-plugin-flake8.svg)](https://pypi.org/project/autohooks-plugin-flake8/)

An [autohooks](https://github.com/greenbone/autohooks) plugin for python code
linting via [flake8](https://github.com/PyCQA/flake8).

## Installation

### Install using pip

You can install the latest stable release of autohooks-plugin-flake8 from the
Python Package Index using [pip](https://pip.pypa.io/):

    python3 -m pip install autohooks-plugin-flake8

Note the `pip` refers to the Python 3 package manager. In an environment where
Python 2 is also available the correct command may be `pip3`.

### Install using poetry

It is highly encouraged to use [poetry](https://python-poetry.org) for
maintaining your project's dependencies. Normally autohooks-plugin-flake8 is
installed as a development dependency.

    poetry install

## Usage

To activate the flake8 autohooks plugin please add the following setting to your
*pyproject.toml* file.

```toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.flake8"]
```

By default, autohooks plugin flake8 checks all files with a *.py* ending. If
only files in a sub-directory or files with different endings should be
formatted, just add the following setting:

```toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.flake8"]

[tool.autohooks.plugins.flake8]
include = ['foo/*.py', '*.foo']
```

To configure flake8 you can specify command-line options in the default flake8 
configuration file *.flake8* in the root directory of the git repository.
To learn more about flake8 configuration see the configuration file or
the flake8 documentation. You can specify your own configuration file using 

```
arguments = ["--config=/path/to/flake8config"]
```

inside the `[tool.autohooks.plugins.flake8]` section of your projects `pyproject.toml`.

See `flake8 --help` for more details.

## Maintainer

This project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).

## Contributing

Your contributions are highly appreciated. Please
[create a pull request](https://github.com/greenbone/autohooks-plugin-flake8/pulls)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at GitHub](https://github.com/greenbone/autohooks-plugin-flake8/issues)
first.

## License

Copyright (C) 2019 - 2022 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).

SPDX-License-Identifier: GPL-3.0-or-later
