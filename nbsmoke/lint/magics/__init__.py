"""support for ipython magics during notebook flake checking

Call insert_get_ipython(notebook) at the start so pyflakes knows about
ipython, then use ipython_to_python_for_flake_checks() to replace
various forms of magics with python in a form that makes sense for
flake checking. See ipython_to_python_for_flake_checks() for more
info.

"""

import sys
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

from . import holoviews_support
from . import builtins_support

# as noted in that file, shouldn't be there but should just be replaced iwth something better anyway
_Unavailable = holoviews_support._Unavailable

# TODO: still nede to investigate the following line magics (and what
# does ipython convert do to them?):
#
#   ? cd
#   ? dirs
#    macro
#   popd
#   pushd
#   pwd
#   pylab (it imports all numpy, pylab, etc etc)
#   rehashx
#   reset?
#   reset_selective
#   sc
#   sx
#   system
#   tb
#   xdel??
#   xmode

# maybe skip?:
#
#  ? alias
#  ? alias_magic
#  ? autoawait
#  ?

# ???
# autocall
# automagic
#

# TODO: Allow people to ignore stuff per project.  E.g. allow
# to add to SIMPLE_MAGICS, IGNORED_MAGICS,
# other_magic_handlers via command-line arg and ini file. And
# point to that mechanism in this warning.

# these will be ignored (i.e. will not be present in python that gets
# lint checked)
IGNORED_LINE_MAGICS = []
IGNORED_CELL_MAGICS = []

# things you don't want to see in your notebooks
BLACKLISTED_LINE_MAGICS = []
BLACKLISTED_CELL_MAGICS = []

# "%magic xyz..." will be replaced by "xyz..."
SIMPLE_LINE_MAGICS = ['time','timeit','prun']

# fns that take some particular magic and turn it into a python line
# that is appropriate for linting (e.g. could return a no-op that uses
# an imported name, or just "pass", etc).
# TODO: the handlers now have a bad interface and are side effecty
other_line_magic_handlers = {}
other_cell_magic_handlers = {}

for hmm in (builtins_support, holoviews_support):
    other_line_magic_handlers.update(hmm.line_magic_handlers)
    other_cell_magic_handlers.update(hmm.cell_magic_handlers)
    IGNORED_LINE_MAGICS.extend(hmm.IGNORED_LINE_MAGICS)
    IGNORED_CELL_MAGICS.extend(hmm.IGNORED_CELL_MAGICS)

# TODO: suddenly had to make some fns into a class to support blacklists; should rework.
class Thing(object):

    def __init__(self, extra_cell_blacklist=None, extra_line_blacklist=None):
        self.blacklisted_cell = (extra_cell_blacklist or []) + BLACKLISTED_CELL_MAGICS
        self.blacklisted_line = (extra_line_blacklist or []) + BLACKLISTED_LINE_MAGICS

    @staticmethod
    def insert_get_ipython(nb):
        # define and use get_ipython (for pyflakes)
        if len(nb['cells']) > 0:
            # the get_ipython() is so pyflakes doesn't complain if no
            # magics present (which would leave get_ipython unused)
            get_ipython_cell = nbformat.v4.new_code_cell(
                'from IPython import get_ipython\nget_ipython()')
            nb['cells'].insert(0,get_ipython_cell)


    def ipython_to_python_for_flake_checks(self, ipy):
        """Given some ipython, return python code suitable for flake checking.

        Regular python (non-magic) lines will be left alone.

        Zero-arg magics will be ignored (omitted from generated python).

        Certain other magics will also be ignored (omitted from
        generated python), e.g. "matplotlib" (see IGNORED_LINE_MAGICS,
        IGNORED_CELL_MAGICS).

        Certain single-argument magics that wrap some regular python will
        be unwrapped: (e.g. "%time fn()" will be replaced by "fn()"; see
        SIMPLE_LINE_MAGICS).

        Optional "magic handlers" can be registered to deal with
        custom/third-party magics (see other_line_magic_handlers,
        other_cell_magic_handlers).

        If a magic is encountered that wasn't handled in any of the above
        ways, it'll be omitted, but with a warning.

        Finally, after the above, if a magic appears in the
        user-supplied cell or line magics blacklist, or is in
        BLACKLISTED_CELL_MAGICS or BLACKLISTED_LINE_MAGICS, it will be
        flagged as a flake.
        """
        ipy_lines = ipy.split('\n') # this is valid for notebooks (json) - i.e. can't be other line endings?
        py_lines = []
        self._transform_ipy_to_py(ipy_lines, py_lines)
        return "\n".join(py_lines)

    def _transform_ipy_to_py(self, lines_in, lines_out):
        for line in lines_in:
            magic_parser = _get_parser(line)
            lines_out.append(self._process(magic_parser))
            self._transform_ipy_to_py(magic_parser.additional_lines, lines_out)

    def _process(self, magic):
        if isinstance(magic, NotMagic):
            content = magic.line
        elif isinstance(magic, LineMagic):
            content = _process_magics(magic, other_line_magic_handlers, IGNORED_LINE_MAGICS, self.blacklisted_line, SIMPLE_LINE_MAGICS)
        elif isinstance(magic, CellMagic):
            content = _process_magics(magic, other_cell_magic_handlers, IGNORED_CELL_MAGICS, self.blacklisted_cell)
        else:
            raise
        return content


def _get_parser(line): # yuck
    for start,cls in parsers.items():
        if start is not None and line.lstrip().startswith(start):
            return cls(line)
    return parsers[None](line) # default/no magic

def _call_a_handler(handlers, magic):
    handler = handlers[magic.name]
    if isinstance(handler, _Unavailable):
        # this is a bit rubbish. and how to reconstruct original error?
        raise Exception("nbsmoke can't process the following '%s' magic without additional dependencies:\n  %s\n. Error was:\n  %s"%(magic.name, magic.line, handler.e.msg))
    return handler(magic)

def _process_magics(magic, other_magic_handlers, ignored_magics, blacklisted_magics, simple_magics=None):
    if simple_magics is None:
        simple_magics = []

    if magic.name in other_magic_handlers:
        content = _call_a_handler(other_magic_handlers, magic)
    elif magic.skippable:
        # pass with original line as comment is just to help with debugging
        content = 'pass # skipped original line: %s'%magic.line
    elif magic.name in ignored_magics:
        content = 'pass # deliberately ignored %s: %s %s'%(magic.__class__.__name__,magic.name,magic.python)
    elif magic.name in simple_magics:
        content = magic.python
    else:
        # TODO: When users can configure simple/ignored etc magics,
        # this warning could point to that mechanism.
        w = "nbsmoke doesn't know how to process the '%s' %s and has ignored it. Line:\n%s\nPlease file an issue at github.com/pyviz/nbsmoke/issues if it should be processed as part of flake checks, or if it should be silently ignored during flake checks."%(magic.name,magic.__class__.__name__,magic.line)
        if sys.version_info[0] == 2:
            # otherwise you get "UnicodeWarning: Warning is using unicode non convertible to ascii, converting to a safe representation" from pytest
            w = w.encode('utf8')
        warnings.warn(w)
        content = 'pass # was: %s'%magic.line

    if magic.name in blacklisted_magics:
        content += ' # nbsmoke-blacklisted: %s'%magic.name

    return magic.indent + content


# the following 'parser' classes could likely be simplified (there
# were more of them, but I just cut a few out).

# abstract
class _Parser(object):
    """For parsing 'a line of python' that was produced by nbconvert ipynb
    -> python.

    'a line of python' could correspond to more than one line
    in the original notebook; cell magics will have been converted to
    something like "fn(magic..., lines)", where lines is the cell content.

    The type of magic (line or cell) is based on the start of the line
    - see "start".

    """
    start = None
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

class NotMagic(_Parser):
    """Line wasn't a magic"""
    pass

# abstract
class _Magic(_Parser):

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

    @staticmethod
    def _parse(x,i):
        # TODO (py2): should find and use ipython's own code for
        # parsing instead (but py2 is going away...)
        bits = LineMagic._parse(x, 0).split(" ", 1)
        if i == 0:
            return bits[i]
        else:
            return bits[i] if len(bits)>i else ''

parsers = {}
for cls in (NotMagic, CellMagic, LineMagic, Py2LineMagic):
    assert cls.start not in parsers
    parsers[cls.start] = cls
