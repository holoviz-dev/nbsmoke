.. image:: https://travis-ci.org/pyviz-dev/nbsmoke.svg?branch=master
    :target: https://travis-ci.org/pyviz-dev/nbsmoke
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/p93ot2kmae55pw3o/branch/master?svg=true
    :target: https://ci.appveyor.com/project/pyviz/nbsmoke/branch/master
    :alt: See Build Status on AppVeyor

.. image:: https://coveralls.io/repos/github/pyviz-dev/nbsmoke/badge.svg?branch=master
    :target: https://coveralls.io/github/pyviz-dev/nbsmoke?branch=master
    :alt: See coverage stats on Coveralls

=======
nbsmoke
=======

Static checking of notebooks (e.g. do they contain lint?)


Installation
------------

You can install nbsmoke via `pip`_ from `PyPI`_::

    $ pip install nbsmoke

Or via `conda`_ from `anaconda.org`_::

    $ conda install nbsmoke


Usage
-----

Lint check notebooks::

    $ pytest --nbsmoke-lint

Lint failures as warnings only::

    $ pytest --nbsmoke-lint --nbsmoke-lint-onlywarn

Instead of all files in a directory, you can specify a list e.g.::

    $ pytest --nbsmoke-lint notebooks/Untitled*.ipynb

If you want to restrict pytest to running only your notebook tests, use `-k`, e.g.::

    $ pytest --nbsmoke-lint -k ".ipynb"

TODO: add ``--nbsmoke-verify`` docs!

Additional options are available by standard pytest 'ini'
configuration in setup.cfg, pytest.ini, or tox.ini::

    [pytest]
    # flakes you don't want to hear about (regex)
    nbsmoke_flakes_to_ignore = .*hvplot.* imported but unused.*

    # line magics to treat as being flakes (i.e. magics you don't want in your notebooks)
    nbsmoke_flakes_line_magics_blacklist = pylab

    # cell magics to treat as being flakes (i.e. magics you don't want in your notebooks)
    nbsmoke_flakes_cell_magics_blacklist = bash
                                           ruby


nbsmoke supports ``# noqa`` comments to mark that something
should be ignored during lint checking.


What's the point?
-----------------

Checking notebooks for lint can find things like undefined names
faster than by running them.

TODO: be able to switch linter? Or explicitly call the "lint"
pyflakes.

Things that aren't errors, such as unused imports/names, might seem
trivial, but they can hinder understanding of a notebook by readers,
or add dependencies that are not required.

Hopefully you don't have mysterious (unused) imports in your notebook,
but if you do, you can add ``# noqa: explanation`` to stop flake
errors.  E.g. if you're importing something for its side effects, it's
very helpful to inform the reader of that.

Pyflakes is used as the underlying linter because "Pyflakes makes a
simple promise: it will never complain about style, and it will try
very, very hard to never emit false positives."


Deprecated usage
----------------

nbsmoke used to support checking that notebooks run without error, and
could save the generated html.  However, we now recommend using nbval
instead. ``--nbsmoke-run`` is still available, but it just calls
nbval; eventually all options related to ``--nbsmoke-run`` will be
removed from nbsmoke.

Before (deprecated)---check all notebooks run without errors::

    $ pytest --nbsmoke-run

After---use nbval instead::

    $ pytest --nbval-lax


Note about kernel used to run notebook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, nbsmoke used the current environment's kernel, whereas
nbval uses the kernel stored in the notebook by default. To obtain
nbsmoke's behavior, pass ``--current-env``. See also:
https://github.com/computationalmodelling/nbval/issues/140


Cell timeout
~~~~~~~~~~~~

Before (deprecated)---pytest configuration options in setup.cfg,
pytest.ini, or tox.ini::

    [pytest]
    # when running, seconds allowed per cell (see nbconvert timeout)
    nbsmoke_cell_timeout = 600


After---nbval has the ``--nbval-cell-timeout`` option. Specify at the
command line, or add to pytest's options (in one of the above files)::

    [pytest]
    addopts = --nbval-cell-timeout=600


Skipping notebooks
~~~~~~~~~~~~~~~~~~

Before (no longer supported)::

    # notebooks to skip running; one case insensitive re to match per line
    nbsmoke_skip_run = ^.*skipme\.ipynb$
                       ^.*skipmetoo.*$


After---use pytest's own test selection and skipping
functionality. You can ignore certain files using ``--ignore`` or
``--ignore-glob`` at the command line, or add to pytest's options (in
one of the above files)::

    [pytest]
    addopts = --ignore=path/to/skipme.ipynb
              --ignore=path/of/skipmetoo.ipynb


Alternatively, for more complex scenarios or to explicitly get "skip"
in your test results, see pytest's ``-k`` option or use a
``conftest.py`` file. nbsmoke has an example of using ``conftest.py``
in its own test suite (``test_skip_run`` in
https://github.com/pyviz-dev/nbsmoke/blob/master/tests/test_run.py).


Contributing
------------

First, install using ``pip install -e .``. Then run the tests using
``tox`` or ``pytest -v tests/``.

New release to PyPI and anaconda.org: ``git tag -a vX.Y.Z -m
"Something about release" && git push --tags``.

Get some help to debug apparently incorrect flakes by adding
``--nbsmoke-lint-debug``,
e.g. ``pytest -v --nbsmoke-lint --nbsmoke-lint-debug examples``.


License
-------

Distributed under the terms of the `BSD-3`_ license, "nbsmoke"
is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ (ideally
including a copy of any problematic notebook).

.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`file an issue`: https://github.com/pyviz-dev/nbsmoke/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`conda`: https://conda.io/
.. _`anaconda.org`: https://anaconda.org/
