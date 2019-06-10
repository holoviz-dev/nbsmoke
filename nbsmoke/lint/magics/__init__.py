"""support for ipython magics during notebook flake checking

Call insert_get_ipython(notebook) at the start so pyflakes knows about
ipython, then use ipython_to_python_for_flake_checks() to replace
various forms of magics with python in a form that makes sense for
flake checking. See ipython_to_python_for_flake_checks() for more
info.

"""

# TODO: instead of this hacky custom magics handling (parsing etc),
# should just find and use ipython's own and then delete most of this
# file. I.e. this is more of a proof of concept hack to see if
# handling magics is useful, rather than something guaranteed to work.

import warnings
import ast

import nbformat

# these will be ignored (i.e. will not be present in python that gets
# lint checked)
IGNORED_MAGICS = ['output','timer','matplotlib','env','load','history','writefile','bash','html','capture']
# TODO: shouldn;t output magic be handled by hv? It's hv only?

# "magic xyz..." will be replaced by "xyz..."
SIMPLE_MAGICS = ['time','timeit','prun']

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


def ipython_to_python_for_flake_checks(py):
    """Given some ipython, return python code suitable for flake checking.

    Regular python (non-magic) lines will be left alone.

    Certain magics will just be ignored (omitted from generated
    python), e.g. "output" (see IGNORED_MAGICS).

    Certain single-argument magics that wrap valid python will be
    processed in a simple way: (e.g. "time fn()" will be replaced by
    "fn()"; see SIMPLE_MAGICS).

    Optional "magic handlers" can be registered to deal with
    custom/third-party magics (see other_magic_handlers).

    If a magic is encountered that wasn't handled by any of the above,
    it'll be omitted with a warning.
    """
    newlines = []
    lines = py.split('\n')
    for line in lines:
        magic_parser = _get_parser(line)
        newlines.append(_process_magics(magic_parser))
        for l in magic_parser.additional_lines:
            newlines.append(_process_magics(_get_parser(l)))
    return "\n".join(newlines)


def _get_parser(line):
    parser = None
    for start,cls in parsers.items():
        if line.lstrip().startswith(start):
            parser = cls
    return parser(line)


def _process_magics(magic):
    if isinstance(magic, NotMagic):
        content = magic.python
    elif magic.skippable or magic.name in IGNORED_MAGICS:
        content = 'pass # was: %s'%magic.line
    elif magic.name in SIMPLE_MAGICS:
        content = magic.python
    elif magic.name in other_magic_handlers:
        handler = other_magic_handlers[magic.name]
        if isinstance(handler, _Unavailable):
            # this is a bit rubbish. and how to reconstruct original error?
            raise Exception("nbsmoke can't process the following '%s' magic without additional dependencies:\n  %s\n. Error was:\n  %s"%(magic.name, magic.line, handler.e.msg))
        content = handler(magic.python)
    else:
        # TODO: Allow people to ignore stuff per project? E.g. "If
        # specific to the current project, pass
        # --nbsmoke-lint-magics-to-ignore=... or set
        # nbsmoke_lint_magics_to_ignore in ini file... or more
        # sophisticated additional magics handling can be added via
        # other_magic_handlers...".
        warnings.warn("nbsmoke doesn't know how to process the '%s' magic and has ignored it. Line:\n%s\nPlease file an issue at github.com/pyviz/nbsmoke/issues if it should be processed, or if it should be silently ignored."%(magic.name,magic.line))
        content = 'pass # was: %s'%magic.line

    return magic.indent + content


# what a miserable set of classes - at least enjoy deleting them :)

# abstract
class _HackyParser(object):
    """For parsing 'a line of python' that was produced by nbconvert ipynb
    -> python.

    'a line of python' could correspond to more than one line
    in the original notebook; cell magics will have been converted to
    something like "fn(magic..., lines)", where lines is the cell content.

    type of magic (e.g. line) based on the start of the line - "start".
    """
    start = ''
    def __init__(self,line):
        """Attributes:

          * line: the original line

          * indent: of the original line

          * name: the name of the magic (could be None).

          * python: some valid bit of python hacked out of the line,
            suitable for taking part in lint check.

          * skippable: whether the python can be skipped from linting
            (because it's empty).

          * additional_lines: some magics (e.g. CompleteCell) can
            contain other lines that will themselves need processing.

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

    @staticmethod
    def _get_additional_lines(pre_line):
        return []

class NotMagic(_HackyParser):
    """
    Line wasn't a magic fn
    """
    pass

# abstract
class _Magic(_HackyParser):
    # Magic that was converted by nbconvert, so will be something like
    # get_ipython.run_cell_magic(magic, ...)."

    @staticmethod
    def _parse(x,i):
        return ast.parse(x).body[0].value.args[i].s

    @classmethod
    def _get_name(cls, pre_line):
        return cls._parse(pre_line, 0)

    @classmethod
    def _get_python(cls, pre_line):
        return cls._parse(pre_line, 1)


# abstract
class _RawMagic(_Magic):
    # Magic that was not converted by nbconvert, so will be something
    # like %%magic ...

    @classmethod
    def _get_name(cls, line):
        return cls._parse(line, 0)

    @classmethod
    def _get_python(cls, line):
        return  cls._parse(line, 1)

    @classmethod
    def _parse(cls, x, i):
        bits = x.strip()[len(cls.start)::].split(" ", 1)
        if len(bits) == 1:
            return ''
        else:
            return bits[i]

# abstract
class _CellMagic(_Magic):
    pass

class CompleteCellMagic(_CellMagic):
    """
    First cell magic in cell; was converted to fn by nbconvert.
    """
    start = 'get_ipython().run_cell_magic('
    @classmethod
    def _get_additional_lines(cls, pre_line):
        return cls._parse(pre_line, 2).splitlines()

class LineMagic(_Magic):
    """line magic (was converted to fn by nbconvert)"""
    start = 'get_ipython().run_line_magic('

class LineRawMagic(_RawMagic):
    """line magic inside cell magic"""
    start = "%"

class CellRawMagic(_RawMagic, _CellMagic):
    """second or subsequent cell magic"""
    start = "%%"

parsers = {}
for cls in (NotMagic, CompleteCellMagic, LineMagic, LineRawMagic, CellRawMagic):
    assert cls.start not in parsers
    parsers[cls.start] = cls

# TODO: need to test with py2 then add something like:
#   line.strip().startswith('get_ipython().magic('): # py2 nbconvert has converted to fn
