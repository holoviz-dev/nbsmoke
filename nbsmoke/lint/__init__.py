"""
Extend pytest to allow flake checking of notebooks.

A notebooks is first converted to a python script, then checked with
pyflakes.

IPython magics are supposed to be handled in a useful way, being
converted to python or skipped as appropriate (depending on their
interaction with python code). See the magics module for more info.
"""

import sys
import warnings
import io
import os
import re

import pytest
import nbformat
import nbconvert

from . import _pyflakes
from . import magics

# list of regexes
flakes_to_ignore = []

class NBLintError(Exception):
    pass

class LintNb(pytest.Item):

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(NBLintError):
            return excinfo.value.args[0]
        else:
            return super(LintNb, self).repr_failure(excinfo)

    def runtest(self):
        with io.open(self.name,encoding='utf8') as nbfile:
            nb = nbformat.read(nbfile, as_version=4)

            magics_processor = magics.Processor(
                extra_line_blacklist = _get_list_from_conf('nbsmoke_flakes_line_magics_blacklist', self.parent.parent.config),
                extra_cell_blacklist = _get_list_from_conf('nbsmoke_flakes_cell_magics_blacklist', self.parent.parent.config),
                extra_magic_handlers = self.parent.parent.config.getini('nbsmoke_magic_handlers'))
            magics_processor.insert_get_ipython(nb)

            ipy, _ = nbconvert.PythonExporter().from_notebook_node(nb)

            debug=self.config.option.nbsmoke_lint_debug
            filenames = []

            self._write_debug_file(debug, ipy, self.name, "pre", filenames)

            py = magics_processor.ipython_to_python_for_flake_checks(ipy)

            self._write_debug_file(debug, py, self.name, "post", filenames)

            flake_result = _pyflakes.flake_check(
                # notebooks will start with "coding: utf-8", but py already unicode
                py.encode('utf8') if sys.version_info[0]==2 else py,
                self.name)

            ### remove flakes by regex ###
            _user_flakes_to_ignore = self.parent.parent.config.getini('nbsmoke_flakes_to_ignore')
            if _user_flakes_to_ignore != '':
                _user_flakes_to_ignore = _user_flakes_to_ignore.splitlines()
            for pattern in set(flakes_to_ignore) | set(_user_flakes_to_ignore):
                flake_result['messages'] = [msg for msg in flake_result['messages'] if not re.search(pattern, msg)]
            ##############################

            if flake_result['messages']:
                msg = "%s\n** "%self.name
                if self.config.option.nbsmoke_lint_onlywarn and 'message_for_onlywarn' in flake_result:
                    msg += flake_result['message_for_onlywarn']
                else:
                    msg += "\n** ".join(flake_result['messages'])
                msg += "\n"+"To see python source that was checked by pyflakes: %s"%filenames[1]
                msg += "\n"+"To see python source before magics were handled by nbsmoke: %s"%filenames[0]

                if self.config.option.nbsmoke_lint_onlywarn:
                    warnings.warn("Flakes (or error) detected:\n"+msg+"\n")
                else:
                    raise NBLintError(msg)

    @staticmethod
    def _write_debug_file(debug, py, name, message, filenames):
        # hack to allow debugging of ipynb linting
        if debug:
            # should I use a temp file instead?
            filename = os.path.splitext(name)[0]+".nbsmoke-debug-%smagicprocess.py"%message
            with io.open(filename,'w',encoding='utf8') as df:
                df.write(py)
            filenames.append(filename)
        else:
            filenames.append("pass --nbsmoke-lint-debug")

def _get_list_from_conf(name,conf):
    # does this not exist in pytest/elsewhere?
    option_raw = conf.getini(name)
    return option_raw.splitlines()
