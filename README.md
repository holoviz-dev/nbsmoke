nbsmoke
=======

|    |    |
| --- | --- |
| Build Status | [![Linux/MacOS/Windows Build Status](https://github.com/holoviz-dev/nbsmoke/workflows/tests/badge.svg)](https://github.com/holoviz-dev/nbsmoke/actions/workflows/tests.yaml)
| Coverage | [![codecov](https://codecov.io/gh/holoviz-dev/nbsmoke/branch/main/graph/badge.svg)](https://codecov.io/gh/holoviz-dev/nbsmoke) ||
| Latest dev release | [![Github tag](https://img.shields.io/github/v/tag/holoviz-dev/nbsmoke.svg?label=tag&colorB=11ccbb)](https://github.com/holoviz-dev/nbsmoke/tags)  |
| Latest release | [![Github release](https://img.shields.io/github/release/holoviz-dev/nbsmoke.svg?label=tag&colorB=11ccbb)](https://github.com/holoviz-dev/nbsmoke/releases) [![PyPI version](https://img.shields.io/pypi/v/nbsmoke.svg?colorB=cc77dd)](https://pypi.python.org/pypi/nbsmoke) [![nbsmoke version](https://img.shields.io/conda/v/pyviz/nbsmoke.svg?colorB=4488ff&style=flat)](https://anaconda.org/pyviz/nbsmoke) [![conda-forge version](https://img.shields.io/conda/v/conda-forge/nbsmoke.svg?label=conda%7Cconda-forge&colorB=4488ff)](https://anaconda.org/conda-forge/nbsmoke) [![defaults version](https://img.shields.io/conda/v/anaconda/nbsmoke.svg?label=conda%7Cdefaults&style=flat&colorB=4488ff)](https://anaconda.org/anaconda/nbsmoke) |
| Python | [![Python support](https://img.shields.io/pypi/pyversions/nbsmoke.svg)](https://pypi.org/project/nbsmoke/)

* * * * *

Basic notebook smoke tests: Do they run ok? Do they contain lint?

* * * * *

This [Pytest](https://github.com/pytest-dev/pytest) plugin was generated
with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with
[@hackebrot](https://github.com/hackebrot)'s
[Cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)
template.

Installation
------------

You can install nbsmoke via [pip](https://pypi.python.org/pypi/pip/)
from [PyPI](https://pypi.python.org/pypi):

    $ pip install nbsmoke

Or get the latest pre-release:

    $ pip install --pre nbsmoke

nbsmoke is also available via [conda](https://conda.io/) from
[anaconda.org](https://anaconda.org/):

    $ conda install -c conda-forge nbsmoke

Usage
-----

Check all notebooks run without errors:

    $ pytest --nbsmoke-run

Check all notebooks run without errors, and store html to look at
afterwards:

    $ pytest --nbsmoke-run --store-html=/scratch

Lint check notebooks:

    $ pytest --nbsmoke-lint

Lint failures as warnings only:

    $ pytest --nbsmoke-lint --nbsmoke-lint-onlywarn

Instead of all files in a directory, you can specify a list e.g.:

    $ pytest --nbsmoke-run notebooks/Untitled*.ipynb

If you want to restrict pytest to running only your notebook tests, use
-k, e.g.:

    $ pytest --nbsmoke-run -k ".ipynb"

Additional options are available by standard pytest 'ini' configuration
in setup.cfg, pytest.ini, or tox.ini:

    [pytest]
    # when running, seconds allowed per cell (see nbconvert timeout)
    nbsmoke_cell_timeout = 600

    # notebooks to skip running; one case insensitive re to match per line
    nbsmoke_skip_run = ^.*skipme\.ipynb$
                       ^.*skipmetoo.*$

    # case insensitive re to match for file to be considered notebook;
    # defaults to ``^.*\.ipynb``
    it_is_nb_file = ^.*\.something$

    # flakes you don't want to hear about (regex)
    nbsmoke_flakes_to_ignore = .*hvplot.* imported but unused.*

    # line magics to treat as being flakes (i.e. magics you don't want in your notebooks)
    nbsmoke_flakes_line_magics_blacklist = pylab

    # cell magics to treat as being flakes (i.e. magics you don't want in your notebooks)
    nbsmoke_flakes_cell_magics_blacklist = bash
                                           ruby

    # add your own magic handlers (python file containing line_magic_handlers and cell_magic_handlers as dictionaries magic_name: callable)
    nbsmoke_magic_handlers = path/to/file.py

nbsmoke supports `# noqa` comments to mark that something should be
ignored during lint checking.

The `nbsmoke_skip_run` list in a project's config can be ignored by
passing `--ignore-nbsmoke-skip-run` (useful if sometimes you want to run
all notebooks for a project where many are typically skipped).

What's the point?
-----------------

Although more sophisticated testing of notebooks is possible (e.g. see
nbval), just checking that notebooks run from start to finish without
error in a fresh kernel (or on a neutral CI service) can be useful
during development. Practical experience of working on several projects
with notebooks confirms this, but that's all the evidence I have.

Checking notebooks for lint might seem trivial/pointless, but it
frequently uncovers unused names (typically unused imports). It's also
quite common to find python 2 vs 3 problems, and sometimes undefined
names - in a way that's faster than running the notebook (over multiple
versions of python).

Unused imports/names themselves might seem trivial, but they can hinder
understanding of a notebook by readers, or add dependencies that are not
required.

Hopefully you don't have mysterious (unused) imports in your notebook,
but if you do, you can add `# noqa: explanation` to stop flake errors.
E.g. if you're importing something for its side effects, it's very
helpful to inform the reader of that.

Pyflakes is used as the underlying linter because "Pyflakes makes a
simple promise: it will never complain about style, and it will try
very, very hard to never emit false positives."

Contributing
------------

First, install using `pip install -e .`. Then run the tests using `tox`
or `pytest -v tests/`.

New release to PyPI:
`git tag -a vX.Y.Z -m "Something about release" && git push --tags`.
Then a PR will auto-open on conda-forge, which should be merged.

Get some help to debug apparently incorrect flakes by adding
`--nbsmoke-lint-debug`, e.g.
`pytest -v --nbsmoke-lint --nbsmoke-lint-debug examples`.

License
-------

Distributed under the terms of the
[BSD-3](http://opensource.org/licenses/BSD-3-Clause) license, "nbsmoke"
is free and open source software.

Issues
------

If you encounter any problems, please [file an
issue](https://github.com/pyviz/nbsmoke/issues) (ideally including a
copy of any problematic notebook).
