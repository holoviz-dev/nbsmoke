# -*- coding: utf-8 -*-

# Note: created with cookiecutter by someone with no experience of how
# to make a pytest plugin. Please question anything related to the
# pytest integration!

import re
import os
import io
import contextlib

import pytest
import nbformat
import nbconvert
from nbconvert.preprocessors import ExecutePreprocessor

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
        '--nbsmoke-run',
        action="store_true",
        help="Run notebooks using nbconvert to check for exceptions.")

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

    group.addoption(
        '--store-html',
        action="store",
        dest='store_html',
        default='',
        help="When running, store rendered-to-html notebooks in the supplied path.")

    parser.addini('nbsmoke_cell_timeout', "nbsmoke's nbconvert cell timeout")

    ####
    # TODO: hacks to work around pyviz team desire to not use pytest's markers
    parser.addini('nbsmoke_skip_run', 're to skip (multi-line; one pattern per line)')
    group.addoption(
        '--ignore-nbsmoke-skip-run',
        action="store_true",
        help="Ignore any skip list in the ini file (allows to run all nbs if desired)")
    ####

    # TODO: remove/rename/see pytest python_files
    parser.addini('it_is_nb_file', 're to determine whether file is notebook')

    parser.addini('nbsmoke_flakes_to_ignore', "flake messages to ignore during nbsmoke's flake checking")

    parser.addini('nbsmoke_flakes_cell_magics_blacklist', "cell magics you don't want to see - i.e. treat as lint.")
    parser.addini('nbsmoke_flakes_line_magics_blacklist', "line magics you don't want to see - i.e. treat as lint")


@contextlib.contextmanager
def cwd(d):
    orig = os.getcwd()
    os.chdir(d)
    try:
        yield
    finally:
        os.chdir(orig)



###################################################


class RunNb(pytest.Item):

    def repr_failure(self, excinfo):
        return excinfo.exconly(True)

    def runtest(self):
        self._skip()
        with io.open(self.name,encoding='utf8') as nb:
            notebook = nbformat.read(nb, as_version=4)

            # TODO: which kernel? run in pytest's or use new one (make it option)
            _timeout = self.parent.parent.config.getini('nbsmoke_cell_timeout')
            kwargs = dict(timeout=int(_timeout) if _timeout!='' else 300,
                          allow_errors=False,
                          # or sys.version_info[1] ?
                          kernel_name='python')

            ep = ExecutePreprocessor(**kwargs)
            with cwd(os.path.dirname(self.name)): # jupyter notebook always does this, right?
                ep.preprocess(notebook,{})

            # TODO: clean up this option handling
            if self.parent.parent.config.option.store_html != '':
                he = nbconvert.HTMLExporter()
                # could maybe use this for chance of testing the html? but not the aim of this project
                #he.template_file = 'basic'
                html, resources = he.from_notebook_node(notebook)
                with io.open(os.path.join(self.parent.parent.config.option.store_html,os.path.basename(self.name)+'.html'),'w',encoding='utf8') as f:
                    f.write(html)

    def _skip(self):
        _skip_patterns = self.parent.parent.config.getini('nbsmoke_skip_run')
        if not self.parent.parent.config.option.ignore_nbsmoke_skip_run:
            for pattern in _skip_patterns.splitlines():
                if re.match(pattern,self.nodeid.split("::")[0],re.IGNORECASE):
                    pytest.skip()


class IPyNbFile(pytest.File):
    def __init__(self, fspath, parent=None, config=None, session=None, dowhat=RunNb):
        self._dowhat = dowhat
        super(IPyNbFile,self).__init__(fspath, parent=parent, config=None, session=None)

    def collect(self):
        yield self._dowhat(str(self.fspath), self)


def pytest_collect_file(path, parent):
    opt = parent.config.option
    # TODO: Make this pattern standard/configurable.
    # match .ipynb except .nbval.ipynb
    it_is_nb_file = parent.config.getini('it_is_nb_file')
    if it_is_nb_file == '':
        #"^((?!\.nbval).)*\.ipynb$"
        it_is_nb_file = r"^.*\.ipynb"
    if re.match(it_is_nb_file,path.strpath,re.IGNORECASE):
        if opt.nbsmoke_run or opt.nbsmoke_lint or opt.nbsmoke_verify:
            # TODO express via the options system if you ever figure it out
            # Hmm, should be able to do all - clean up!
            assert (opt.nbsmoke_run ^ opt.nbsmoke_lint) ^ opt.nbsmoke_verify
            if opt.nbsmoke_run:
                dowhat = RunNb
            elif opt.nbsmoke_lint:
                dowhat = LintNb
            elif opt.nbsmoke_verify:
                dowhat = VerifyNb

            if hasattr(IPyNbFile, "from_parent"):
                return IPyNbFile.from_parent(parent, fspath=path, dowhat=dowhat)
            
            return IPyNbFile(path, parent, dowhat=dowhat)
