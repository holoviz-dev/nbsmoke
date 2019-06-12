"""support for ipython magics during notebook flake checking

Call insert_get_ipython(notebook) at the start so pyflakes knows about
ipython, then use ipython_to_python_for_flake_checks() to replace
various forms of magics with python in a form that makes sense for
flake checking. See ipython_to_python_for_flake_checks() for more
info.

"""

import warnings
import ast

import nbformat


# try to fight the advertising/deprecation warnings and get an
# ipython2python function without confusing messages appearing
# all over the place
try:
    from IPython.core.inputtransformer2 import TransformerManager
    ipython2python = TransformerManager().transform_cell
except:
    # this is the import I wanted to use, but it generates
    # deprecation wanrings when all the latest packages are
    # installed (as of 12 June 2019).
    from nbconvert.filters.strings import ipython2python

# these will be ignored (i.e. will not be present in python that gets
# lint checked)
IGNORED_MAGICS = ['output','timer','matplotlib','env','load','history','writefile','bash','html','capture']
# TODO: shouldn;t output magic be handled by hv? It's hv only?

# "magic xyz..." will be replaced by "xyz..."
SIMPLE_MAGICS = ['time','timeit','prun']

# TODO: there are lots more inbuilt magics we should probably
# handle. See get_ipython().magics_manager.registry.

# placeholder for unavailable imports
class _Unavailable:
    def __init__(self,e):
        self.e = e

# fns that take some particular magic and turn it into a python line
# that is appropriate for linting (e.g. could return a no-op that uses
# an imported name, or just "pass", etc).
other_magic_handlers = {}

try:
    from . import holoviews_support
    other_magic_handlers['opts'] = holoviews_support.opts_handler
except ImportError as e:
    other_magic_handlers['opts'] = _Unavailable(e)


def insert_get_ipython(nb):
    # define and use get_ipython (for pyflakes)
    if len(nb['cells']) > 0:
        # the get_ipython() is so pyflakes doesn't complain if no
        # magics present (which would leave get_ipython unused)
        get_ipython_cell = nbformat.v4.new_code_cell(
            'from IPython import get_ipython\nget_ipython()')
        nb['cells'].insert(0,get_ipython_cell)


def ipython_to_python_for_flake_checks(ipy):
    """Given some ipython, return python code suitable for flake checking.

    Regular python (non-magic) lines will be left alone.

    Zero-arg magics will be ignored (omitted from generated python).

    Certain other magics will also be ignored (omitted from generated
    python), e.g. "matplotlib" (see IGNORED_MAGICS).

    Certain single-argument magics that wrap some regular python will
    be unwrapped: (e.g. "%time fn()" will be replaced by "fn()"; see
    SIMPLE_MAGICS).

    Optional "magic handlers" can be registered to deal with
    custom/third-party magics (see other_magic_handlers).

    If a magic is encountered that wasn't handled in any of the above
    ways, it'll be omitted, but with a warning.
    """
    ipy_lines = ipy.split('\n') # this is valid for notebooks (json) - i.e. can't be other line endings?
    py_lines = []
    _transform_ipy_to_py(ipy_lines, py_lines)
    return "\n".join(py_lines)

def _transform_ipy_to_py(lines_in, lines_out):
    for line in lines_in:
        magic_parser = _get_parser(line)
        lines_out.append(_process_magics(magic_parser))
        _transform_ipy_to_py(magic_parser.additional_lines, lines_out)

def _get_parser(line):
    parser = None
    for start,cls in parsers.items():
        if line.lstrip().startswith(start):
            parser = cls
    return parser(line)

def _process_magics(magic):
    if isinstance(magic, NotMagic):
        content = magic.python
    elif magic.skippable:
        # this is really just to help with debugging
        content = 'pass # was line: %s'%magic.line
    elif magic.name in IGNORED_MAGICS:
        content = 'pass # was %s: %s %s'%(magic.__class__.__name__,magic.name,magic.python)
    elif magic.name in SIMPLE_MAGICS:
        content = magic.python
    elif magic.name in other_magic_handlers:
        handler = other_magic_handlers[magic.name]
        if isinstance(handler, _Unavailable):
            # this is a bit rubbish. and how to reconstruct original error?
            raise Exception("nbsmoke can't process the following '%s' magic without additional dependencies:\n  %s\n. Error was:\n  %s"%(magic.name, magic.line, handler.e.msg))
        content = handler(magic.python)
    else:
        # TODO: Allow people to ignore stuff per project.  E.g. allow
        # to add to SIMPLE_MAGICS, IGNORED_MAGICS,
        # other_magic_handlers via command-line arg and ini file. And
        # point to that mechanism in this warning.
        warnings.warn("nbsmoke doesn't know how to process the '%s' magic and has ignored it. Line:\n%s\nPlease file an issue at github.com/pyviz/nbsmoke/issues if it should be processed, or if it should be silently ignored."%(magic.name,magic.line))
        content = 'pass # was: %s'%magic.line

    return magic.indent + content


# the following 'parser' classes could likely be simplified (there
# were more of them, but I just cut a few out).

# abstract
class _HackyParser(object):
    """For parsing 'a line of python' that was produced by nbconvert ipynb
    -> python.

    'a line of python' could correspond to more than one line
    in the original notebook; cell magics will have been converted to
    something like "fn(magic..., lines)", where lines is the cell content.

    The type of magic (line or cell) is based on the start of the line
    - see "start".

    """
    start = ''
    def __init__(self,line):
        """Attributes:

          * line: the original line

          * indent: of the original line

          * name: the name of the magic (could be None).

          * python: some valid bit of python taken from the original
            line, suitable for taking part in lint check.

          * skippable: whether the python can be skipped from linting
            (because it's empty).

          * additional_lines: some magics (e.g. Cell) can contain
            other lines that will themselves need processing.

        """
        self.line = line
        self.indent = self._get_indent(line)
        pre_line = self._pre(line)
        self.additional_lines = self._get_additional_lines(pre_line)
        self.name = self._get_name(pre_line)
        self.python = self._get_python(pre_line)
        self.skippable = (self.python.strip() == '') # e.g. zero args

    @staticmethod
    def _pre(line):
        return line.strip()

    @staticmethod
    def _get_indent(line):
        return " " * (len(line) - len(line.lstrip()))

    @classmethod
    def _get_name(cls, pre_line):
        return None

    @classmethod
    def _get_python(cls, pre_line):
        return pre_line

    def _get_additional_lines(self, pre_line):
        return []

class NotMagic(_HackyParser):
    """Line wasn't a magic"""
    pass

# abstract
class _Magic(_HackyParser):

    @staticmethod
    def _parse(x,i):
        return ast.parse(x).body[0].value.args[i].s

    @classmethod
    def _get_name(cls, pre_line):
        return cls._parse(pre_line, 0)

    @classmethod
    def _get_python(cls, pre_line):
        return cls._parse(pre_line, 1)

class CellMagic(_Magic):
    """cell magic that was converted to fn by nbconvert"""
    start = 'get_ipython().run_cell_magic('

    def _get_additional_lines(self, pre_line):
        remaining_lines = self._parse(pre_line, 2).splitlines()
        return ipython2python("\n".join(remaining_lines)).splitlines()

class LineMagic(_Magic):
    """line magic that was converted to fn by nbconvert"""
    start = 'get_ipython().run_line_magic('

class Py2LineMagic(LineMagic):
    """line magic that was converted to fn by nbconvert under python 2"""
    start = 'get_ipython().magic('

    @classmethod
    def _get_python(cls, pre_line):
        return cls._parse(pre_line, 0)

parsers = {}
for cls in (NotMagic, CellMagic, LineMagic, Py2LineMagic):
    assert cls.start not in parsers
    parsers[cls.start] = cls
