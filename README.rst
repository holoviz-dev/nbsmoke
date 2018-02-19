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

Check all notebooks in examples/ run without errors::

    $ pytest --nbsmoke-run examples/

Check all notebooks in examples/ run without errors, and store html to
look at afterwards::

    $ pytest --nbsmoke-run --store-html=/scratch examples/

Lint check notebooks in examples/::

    $ pytest --nbsmoke-lint notebooks/

Instead of all files in a directory, you can specify a list e.g.::

    $ pytest --nbsmoke-run notebooks/Untitled*.ipynb

Additional options are available by standard pytest 'ini'
configuration in setup.cfg, pytest.ini, or tox.ini::

    [pytest]
    # when running, seconds allowed per cell (see nbconvert timeout)
    cell_timeout = 600

    # notebooks to skip running; one case insensitive re to match per line
    skip_run = ^.*skipme\.ipynb$
               ^.*skipmetoo.*$

    # case insensitive re to match for file to be considered notebook;
    # defaults to ``^.*\.ipynb``
    it_is_nb_file = ^.*\.something$


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
