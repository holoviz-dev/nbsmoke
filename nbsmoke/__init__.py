# -*- coding: utf-8 -*-

# Note: created with cookiecutter by someone with no experience of how
# to make a pytest plugin. Please question anything related to the
# pytest integration!

import pytest
import re
import os
import io
import sys
import contextlib
import ast # uh oh
import warnings

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

######################################################################
######################################################################

# This section is adding "# noqa" support to pyflakes. It's not
# perfect (e.g. what if someone has "# noqa" in some string). Could
# consider switching to flake8, but it's probably too complex to use
# for notebooks.

import pyflakes.reporter, pyflakes.checker
import _ast

def flake_check(codeString, filename, reporter=None):
    if reporter is None:
        reporter = pyflakes.reporter._makeDefaultReporter()
    # First, compile into an AST and handle syntax errors.
    try:
        tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError:
        value = sys.exc_info()[1]
        msg = value.args[0]

        (lineno, offset, text) = value.lineno, value.offset, value.text

        if pyflakes.checker.PYPY:
            if text is None:
                lines = codeString.splitlines()
                if len(lines) >= lineno:
                    text = lines[lineno - 1]
                    if sys.version_info >= (3, ) and isinstance(text, bytes):
                        try:
                            text = text.decode('ascii')
                        except UnicodeDecodeError:
                            text = None
            offset -= 1

        # If there's an encoding problem with the file, the text is None.
        if text is None:
            # Avoid using msg, since for the only known case, it contains a
            # bogus message that claims the encoding the file declared was
            # unknown.
            reporter.unexpectedError(filename, 'problem decoding source')
        else:
            reporter.syntaxError(filename, msg, lineno, offset, text)
        return 1
    except Exception:
        reporter.unexpectedError(filename, 'problem decoding source')
        return 1
    # Okay, it's syntactically valid.  Now check it.
    w = pyflakes.checker.Checker(tree, filename)

    ##########################
    ## addition to pyflakes ##
    NOQA = re.compile('# noqa', re.IGNORECASE)
    noqa_lines = [i+1 for i,l in enumerate(codeString.splitlines()) if NOQA.search(l)]
    w.messages[:] = [m for m in w.messages if m.lineno not in noqa_lines]
    ##########################

    w.messages.sort(key=lambda m: m.lineno)
    for warning in w.messages:
        reporter.flake(warning)
    return len(w.messages)


######################################################################
######################################################################


import nbformat
import nbconvert
from nbconvert.preprocessors import ExecutePreprocessor


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
        '--store-html',
        action="store",
        dest='store_html',
        default='',
        help="When running, store rendered-to-html notebooks in the supplied path.")

    parser.addini('cell_timeout', 'nbconvert cell timeout')
    parser.addini('it_is_nb_file', 're to determine whether file is notebook')
    parser.addini('skip_run', 're to skip (multi-line; one pattern per line)')


@contextlib.contextmanager
def cwd(d):
    orig = os.getcwd()
    os.chdir(d)
    try:
        yield
    finally:
        os.chdir(orig)


class RunNb(pytest.Item):
    def runtest(self):
        self._skip()
        with io.open(self.name,encoding='utf8') as nb:
            notebook = nbformat.read(nb, as_version=4)

            # TODO: which kernel? run in pytest's or use new one (make it option)
            _timeout = self.parent.parent.config.getini('cell_timeout')
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
        _skip_patterns = self.parent.parent.config.getini('skip_run')
        if _skip_patterns != '':
            skip_patterns = _skip_patterns.splitlines()
            for pattern in skip_patterns:
                if re.match(pattern,self.name,re.IGNORECASE):
                    pytest.skip()


def _insert_get_ipython(nb):
    # so pyflakes doesn't get confused about magics
    if len(nb['cells']) > 0:
        # the get_ipython() is so pyflakes doesn't complain if no
        # magics present.
        get_ipython_cell = nbformat.v4.new_code_cell(
            'from IPython import get_ipython\nget_ipython()')
        nb['cells'].insert(0,get_ipython_cell)


####################

# TODO: instead of this hacky custom magics handling, should find and
# use ipython's own

def _line_magics(line):
    # magic=None means magic but don't process - omit line
    # magic=True means magic but don't need to process - include line as is
    # magic=False means no magic - include line as is
    # otherwise magic is something to process
    
    if line.strip().startswith('%%'):
        # TODO: we only process the first cell magics (part of
        # assumption that cell magics don't use names from python
        magic, content = None, ''
    elif line.strip().startswith('%'):
        bits = line[1::].split(" ", 1)
        if len(bits) == 1: # have never tested this path?
            magic,content = True, line
        else:
            magic,content = bits
    elif line.strip().startswith('get_ipython().run_line_magic('):
        magic,content = [x.s for x in ast.parse(line).body[0].value.args]
    # py2
    elif line.strip().startswith('get_ipython().magic('):
        # using ast probably unnecessary, just copy/pasted from cell magics
        bits = ast.parse(line).body[0].value.args[0].s.split(" ", 1)
        if len(bits) == 1:
            magic,content = True, line
        else:
            magic, content = ast.parse(line).body[0].value.args[0].s.split(" ", 1)
    else:
        magic, content = False, line

    if magic in (None,False,True):
        return content
    elif magic in ('time','timeit','prun'):
        return content
    elif magic in ('opts','output','timer'):
        # silently ignore
        return line
    else:
        # unknown
        warnings.warn("nbsmoke can't process the following line magic and has skipped it:\n%s\nPlease file an issue at github.com/pyviz/nbsmoke/issues if it should be supported (i.e. included or silently ignored)"%line)
        return line


def insert_ipython_magic_content(py):
    # Assuming cell magic always looks like this:
    #   'get_ipython().run_cell_magic(\'x\', \'y\', "z")'
    # where x is the %% command, y is the rest of the line, and z is
    # the cell code, insert all lines from z back into
    # the source for pyflakes to look at.
    #
    # Also, assumes cell magics don't use names from the python, which
    # probably isn't true (i.e. could probably get spurious ununsed
    # import flakes)
    #
    # This is more of a proof of concept hack than something
    # guaranteed to work...
    newlines = []
    lines = py.split('\n')
    for line in lines:
        if line.startswith('get_ipython().run_cell_magic('):
            # TODO: test with prun
            content = ast.parse(line).body[0].value.args[2].s.splitlines()
            for l in content:
                newlines.append(_line_magics(l))
        else:
            newlines.append(_line_magics(line))
    return "\n".join(newlines)

####################


class LintNb(pytest.Item):
    def runtest(self):
        with io.open(self.name,encoding='utf8') as nbfile:
            nb = nbformat.read(nbfile, as_version=4)
            _insert_get_ipython(nb)
            py, resources = nbconvert.PythonExporter().from_notebook_node(nb)
            py = insert_ipython_magic_content(py)
            if sys.version_info[0]==2:
                # notebooks will start with "coding: utf-8", but py already unicode
                py = py.encode('utf8')
            if flake_check(py,self.name) != 0:
                raise AssertionError


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
        it_is_nb_file = "^.*\.ipynb"
    if re.match(it_is_nb_file,path.strpath,re.IGNORECASE):
        if opt.nbsmoke_run or opt.nbsmoke_lint:
            # TODO express via the options system if you ever figure it out
            assert opt.nbsmoke_run ^ opt.nbsmoke_lint
            if opt.nbsmoke_run:
                dowhat = RunNb
            elif opt.nbsmoke_lint:
                dowhat = LintNb
            return IPyNbFile(path, parent, dowhat=dowhat)
