==============
pytest-nbsmoke
==============

.. image:: https://travis-ci.org/ContinuumIO/nbsmoke.svg?branch=master
    :target: https://travis-ci.org/ContinuumIO/nbsmoke
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/reuh381xg7f9ks83/branch/master?svg=true
    :target: https://ci.appveyor.com/project/ceball/nbsmoke
    :alt: See Build Status on AppVeyor

Basic ("non data") notebook testing: do they run ok? do they contain lint?
Also lets you store html to look at.

WARNING: early stage proof of concept; work in progress. Use at your
own risk.

Created with a cookiecutter and modified until it seemed to
work. There's loads of cleanup left to do (and boilerplate to remove).

Different from nbval: unlike nbval, this is really about running nbs
as someone would run, without modifications to support skipping cells,
kernel hooks, or anything else...

pytest --nbsmoke-run notebooks/

Do notebooks run without errors, plus store html (hmm...what if there's an error)?

pytest --nbsmoke-run --store-html=/scratch notebooks/

Lint check notebooks:

pytest --nbsmoke-lint notebooks/

Specifying options, use 'ini' e.g. setup.cfg or tox.ini or pytest.ini:
cell_timeout: seconds allowed per cell (see nbconvert timeout)
it_is_nb_file: case insensitive re to match for file to be considered notebook; defaults to ``^.*\.ipynb``

Developing? Run the tests:
pip install -e .
pytest tests/




----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* TODO


Requirements
------------

* TODO


Installation
------------

You can install "pytest-nbsmoke" via `pip`_ from `PyPI`_::

    $ pip install pytest-nbsmoke


Usage
-----

* TODO

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `BSD-3`_ license, "pytest-nbsmoke" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/ContinuumIO/pytest-nbsmoke/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
