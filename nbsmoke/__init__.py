# -*- coding: utf-8 -*-

import os

import pytest

try:
    from version import Version
    __version__ = str(Version(fpath=__file__,archive_commit="$Format:%h$",reponame="nbsmoke"))
    del Version
except:
    import json
    __version__ = json.load(open(os.path.join(os.path.dirname(__file__),'.version'),'r'))['version_string']
    del json

from .lint import LintNb
from .verify import VerifyNb



def pytest_addoption(parser):
    group = parser.getgroup('nbsmoke')

    group.addoption(
        '--nbsmoke-lint',
        action="store_true",
        help="Lint check notebooks using flake8")

    group.addoption(
        '--nbsmoke-lint-debug',
        action="store_true",
        help="Write out copy of python script resulting from conversion of ipynb")

    group.addoption(
        '--nbsmoke-lint-onlywarn',
        action="store_true",
        help="Flake errors will only appear as warnings")

    group.addoption(
        '--nbsmoke-verify',
        action="store_true",
        help="Verify notebooks")

    parser.addini('nbsmoke_flakes_to_ignore', "flake messages to ignore during nbsmoke's flake checking")
    parser.addini('nbsmoke_flakes_cell_magics_blacklist', "cell magics you don't want to see - i.e. treat as lint.")
    parser.addini('nbsmoke_flakes_line_magics_blacklist', "line magics you don't want to see - i.e. treat as lint")


    ##################
    ### DEPRECATED ###
    # remove in 0.6
    group.addoption(
        '--nbsmoke-run',
        action="store_true",
        help="**DEPRECATED: Use nbval instead** Run notebooks using nbconvert to check for exceptions.")

    parser.addini('nbsmoke_cell_timeout', "**DEPRECATED: Use nbval instead** nbsmoke's nbconvert cell timeout")

    # TODO: hacks to work around pyviz team desire to not use pytest's markers
    parser.addini('nbsmoke_skip_run', '**DEPRECATED: Use a pytest option such as --ignore, --ignore-glob, -k, or conftest.py** re to skip (multi-line; one pattern per line)')
    group.addoption(
        '--ignore-nbsmoke-skip-run',
        action="store_true",
        help="**DEPRECATED: Use a pytest option such as --ignore, --ignore-glob, -k, or conftest.py** Ignore any skip list in the ini file (allows to run all nbs if desired)")
    ####
    ##################
    

class IPyNbFile(pytest.File):
    def __init__(self, type_, fspath, parent=None, config=None, session=None):
        self._type = type_
        super(IPyNbFile,self).__init__(fspath, parent=parent, config=None, session=None)

    def collect(self):
        yield self._type(str(self.fspath), self)

        
def pytest_collect_file(path, parent):
    if not path.fnmatch("*.ipynb"):
        return

    opt = parent.config.option

    # TODO: you have to pick one - can't currently run and lint and
    # verify (though you should be able to)
    
    if opt.nbsmoke_run:
        import warnings
        warnings.warn("--nbsmoke-run is deprecated: please use nbval (--nbval-lax) instead.", DeprecationWarning)

        import sys
        import nbval.plugin

        if '--current-env' not in sys.argv:
            opt.current_env = True

        if '--nbval-cell-timeout' not in sys.argv:
            timeout = parent.config.getini('nbsmoke_cell_timeout')
            if timeout != '':
                opt.nbval_cell_timeout = timeout

        skip_patterns = parent.config.getini('nbsmoke_skip_run')
        if skip_patterns.strip() != '':
            if not '--ignore-nbsmoke-skip-run' in sys.argv:
                raise ValueError("nbsmoke_skip_run regex no longer supported; use pytest one of pytest's own options instead: -k, --ignore, --ignore-glob, conftest.py."
        
        return nbval.plugin.IPyNbFile(path, parent)
    
    elif opt.nbsmoke_lint:
        return IPyNbFile(LintNb, path, parent)
    elif opt.nbsmoke_verify:
        return IPyNbFile(VerifyNb, path, parent)
