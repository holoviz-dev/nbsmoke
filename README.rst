.. image:: https://travis-ci.org/pyviz/nbsmoke.svg?branch=master
    :target: https://travis-ci.org/pyviz/nbsmoke
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/p93ot2kmae55pw3o/branch/master?svg=true
    :target: https://ci.appveyor.com/project/pyviz/nbsmoke/branch/master
    :alt: See Build Status on AppVeyor


=======
nbsmoke
=======

Basic notebook smoke tests: Do they run ok? Do they contain lint?

**WARNING: early stage proof of concept; work in progress. Use at your
own risk.**

In particular, this extension is supposed to handle ipython magics as
far as possible, but has not yet been widely tested.

----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.



Installation
------------

You can install nbsmoke via `pip`_ from `PyPI`_::

    $ pip install nbsmoke

Or you can install nbsmoke via `conda`_ from `anaconda.org`_::

    $ conda install -c pyviz/label/dev -c conda-forge nbsmoke


Usage
-----

Check all notebooks run without errors::

    $ pytest --nbsmoke-run

Check all notebooks run without errors, and store html to look at
afterwards::

    $ pytest --nbsmoke-run --store-html=/scratch

Lint check notebooks::

    $ pytest --nbsmoke-lint

Instead of all files in a directory, you can specify a list e.g.::

    $ pytest --nbsmoke-run notebooks/Untitled*.ipynb

If you want to restrict pytest to running only your notebook tests, use `-k`, e.g.::

    $ pytest --nbsmoke-run -k ".ipynb"

Additional options are available by standard pytest 'ini'
configuration in setup.cfg, pytest.ini, or tox.ini::

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


nbsmoke supports ``# noqa`` comments to mark that something
should be ignored during lint checking.

The ``nbsmoke_skip_run`` list in a project's config can be ignored by
passing ``--ignore-nbsmoke-skip-run`` (useful if sometimes you want to
run all notebooks for a project where many are typically skipped).


What's the point?
-----------------

Although more sophisticated testing of notebooks is possible (e.g. see
nbval), just checking that notebooks run from start to finish without
error in a fresh kernel (or on a neutral CI service) can be useful
during development. Practical experience of working on several
projects with notebooks confirms this, but that's all the evidence I
have.

Checking notebooks for lint might seem trivial/pointless, but it
frequently uncovers unused names (typically unused imports). It's also
quite common to find python 2 vs 3 problems, and sometimes undefined
names - in a way that's faster than running the notebook (over
multiple versions of python).

Unused imports/names themselves might seem trivial, but they can
hinder understanding of a notebook by readers, or add dependencies
that are not required.

Hopefully you don't have mysterious (unused) imports in your notebook,
but if you do, you can add ``# noqa: explanation`` to stop flake
errors.  E.g. if you're importing something for its side effects, it's
very helpful to inform the reader of that.

Pyflakes is used as the underlying linter because "Pyflakes makes a
simple promise: it will never complain about style, and it will try
very, very hard to never emit false positives."


Contributing
------------

First, install using ``pip install -e .``. Then run the tests using
``tox`` or ``pytest -v tests/``.

New release to PyPI and anaconda.org: ``git tag -a vX.Y.Z -m
"Something about release" && git push --tags``.


License
-------

Distributed under the terms of the `BSD-3`_ license, "nbsmoke"
is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ (ideally
including a copy of any problematic notebook).

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/pyviz/nbsmoke/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`conda`: https://conda.io/
.. _`anaconda.org`: https://anaconda.org/
