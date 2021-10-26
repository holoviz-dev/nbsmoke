# -*- coding: utf-8 -*-

from . import lint_args, WARNINGS_ARE_ERRORS, nb_basic

nb_variety_of_magics = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%env\\n",
    "%load\\n",
    "%history"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%matplotlib inline\\n",
    "\\n",
    "%matplotlib"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%writefile sigh\\n",
    "1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "result=ds=df=None\\n",
    "try:\\n",
    "    import numpy as np\\n",
    "    import holoviews as hv\\n",
    "    from holoviews.operation.datashader import aggregate\\n",
    "    hv.notebook_extension('bokeh')\\n",
    "\\n",
    "    %matplotlib inline\\n",
    "    \\n",
    "    dataset = hv.Dataset(df, kdims=['fare_amount', 'trip_distance'], vdims=[]).select(fare_amount=(0,60))\\n",
    "    agg = aggregate(dataset, aggregator=ds.count(), streams=[hv.streams.RangeX()], x_sampling=0.5, width=500, height=2)\\n",
    "    result = agg.map(lambda x: x.reduce(trip_distance=np.sum), hv.Image)\\n",
    "    \\n",
    "except ImportError: pass\\n",
    "result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "u\\"中国\\""
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''


# note: % escaped as % subst
nb_cell_and_line_magics = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import holoviews as hv\\n",
    "import os\\n",
    "from holoviews.operation.datashader import datashade"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%%%capture --no-stderr\\n",
    "%%%%html --isolated\\n",
    "%%time %(dim_name)s = hv.Dimension('A')\\n",
    "bdim = hv.Dimension('B')\\n",
    "paths = [os.path.join('data', f) for f in ['a','b']]\\n",
    "hv.Layout([datashade(hv.Curve(p, kdims=[adim], vdims=[bdim])) for p in paths]).cols(2)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''

# note: % escaped as % subst
nb_cell_skipped_and_line_magics = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import holoviews as hv\\n",
    "import os\\n",
    "from holoviews.operation.datashader import datashade"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%%%matplotlib inline\\n",
    "%%%%capture --no-stderr\\n",
    "%%%%html --isolated\\n",
    "%%time %(dim_name)s = hv.Dimension('A')\\n",
    "bdim = hv.Dimension('B')\\n",
    "paths = [os.path.join('data', f) for f in ['a','b']]\\n",
    "hv.Layout([datashade(hv.Curve(p, kdims=[adim], vdims=[bdim])) for p in paths]).cols(2)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''


# this is simple line magics, right?
# note: % escaped
nb_line_magic = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def f(): return 1\\n",
    "\\n",
    "%%time z = %(prefix)sf()\\n",
    "z"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''

# note: % escaped
nb_unhandled_magics = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%linemagicnonexistent %(magic_arg)s"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%%%cellmagicnonexistent %(magic_arg)s"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%%%cellmagicnonexistenttwo %(magic_arg)s\\n",
    "%%%%cellmagicnonexistentthree %(magic_arg)s"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''


nb_optional_dep = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%clever_magic one two three"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''

nb_lint_line_magic_indent = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "try:\\n",
    "    %time 17\\n",
    "except: pass\\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''

nb_lint_cell_line_magic_indent =  u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%matplotlib inline\\n",
    "try:\\n",
    "    %time 17\\n",
    "except: pass\\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''

nb_lint_is_it_magic =  u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%matplotlib inline\\n",
    "import hv\\n",
    "for m in [1,2,3]:\\n",
    "    def cb(metric=m):\\n",
    "        return hv.Curve(\\n",
    "            '%s %s'\\n",
    "            % (metric, 1))\\n",
    "    def cb2(metric=m):\\n",
    "        return hv.Curve(\\n",
    "            '%sad'\\n",
    "            % metric )\\n",
    "    def cb3(metric=m):\\n",
    "        return hv.Curve(\\n",
    "            '%sad'\\n",
    "            %metric )"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''


# this is ignored line magics, right?
def test_lint_magics_nowarn(testdir):
    # there should be no warnings for a variety of magics
    # TODO break this test up into more specific ones?
    testdir.makefile('.ipynb', testing123=nb_variety_of_magics)
    result = testdir.runpytest(*lint_args)
    assert result.ret == 0

def test_lint_line_magics_good(testdir):
    # line magic with one arg
    testdir.makefile('.ipynb', testing123=nb_line_magic%{'prefix':''})
    result = testdir.runpytest(*lint_args)
    assert result.ret == 0

def test_lint_line_magics_bad(testdir):
    # line magic with undefined name
    testdir.makefile('.ipynb', testing123=nb_line_magic%{'prefix':'bad'})
    result = testdir.runpytest(*lint_args)
    assert result.ret == 1
    result.stdout.re_match_lines_random([".*undefined name 'badf'$"])

def test_lint_line_magics_with_cell_magics_good(testdir):
    testdir.makefile('.ipynb', testing123=nb_cell_and_line_magics%{'dim_name':'adim'})
    result = testdir.runpytest(*lint_args)
    assert result.ret == 0

def test_lint_line_magics_with_cell_magics_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_cell_and_line_magics%{'dim_name':'bad_name'})
    result = testdir.runpytest(*lint_args)
    result.stdout.re_match_lines_random(
        [".*undefined name 'adim'$"])
    assert result.ret == 1

def test_lint_line_magics_with_skipped_cell_magics_bad(testdir):
    # when omitting cell magic, make sure rest of cell is not also omitted
    testdir.makefile('.ipynb', testing123=nb_cell_skipped_and_line_magics%{'dim_name':'bad_name'})
    result = testdir.runpytest(*lint_args)
    result.stdout.re_match_lines_random(
        [".*undefined name 'adim'$"])
    assert result.ret == 1

def test_lint_magics_skip_warn_about_zero_arg(testdir):
    testdir.makefile('.ipynb', testing123=nb_unhandled_magics%{'magic_arg':''})
    result = testdir.runpytest(*lint_args)
    assert result.ret == 0

def test_lint_magics_warn_about_unhandled(testdir):
    testdir.makefile('.ipynb', testing123=nb_unhandled_magics%{'magic_arg':'arg'})
    _args = list(lint_args)
    _args.remove(WARNINGS_ARE_ERRORS)
    result = testdir.runpytest(*_args)
    assert result.ret == 0
    assert result.parseoutcomes()['warnings'] == 4
    result.stdout.re_match_lines_random(
        [".*nbsmoke doesn't know how to process the.*cellmagicnonexistent.*CellMagic and has ignored it.*",
         ".*nbsmoke doesn't know how to process the.*linemagicnonexistent.*LineMagic and has ignored it.*",
         ".*nbsmoke doesn't know how to process the.*cellmagicnonexistenttwo.*CellMagic and has ignored it.*",
         ".*nbsmoke doesn't know how to process the.*cellmagicnonexistentthree.*CellMagic and has ignored it.*"])

def test_optional_import_warn(testdir):
    testdir.makeini(r"""
        [pytest]
        nbsmoke_magic_handlers = my_magic_handlers.py
    """)
    testdir.makefile('.ipynb', testing123=nb_optional_dep)
    testdir.makefile(".py", my_magic_handlers="def not_clever_magics_handler(magic):\n    raise ImportError('Amazing dependency is missing')\n\nline_magic_handlers=dict(clever_magic=not_clever_magics_handler);cell_magic_handlers={}")
    result = testdir.runpytest(*lint_args)
    assert result.ret == 1
    result.stdout.re_match_lines_random(
        [".*ImportError: nbsmoke can't process the following 'clever_magic' magic without additional dependencies.*",
         ".*Amazing dependency is missing.*"])


def test_lint_line_magics_indent(testdir):
    testdir.makefile('.ipynb', testing123=nb_lint_line_magic_indent)
    result = testdir.runpytest(*lint_args)
    assert result.ret == 0

def test_lint_cell_line_magics_indent(testdir):
    testdir.makefile('.ipynb', testing123=nb_lint_cell_line_magic_indent)
    result = testdir.runpytest(*lint_args)
    assert result.ret == 0

def test_magics_detection(testdir):
    # if you were to parse ipython stuff line by line, you might mistake
    # things for magics, e.g.
    #   'some %s'
    #   %variable
    testdir.makefile('.ipynb', testing123=nb_lint_is_it_magic)
    result = testdir.runpytest(*lint_args)
    # if falsely detecting magic, the "pass" that gets inserted for
    # the unknown magic would be a syntax error
    #
    # also, the following should not be present (would be warned about
    # as unknown magic)
    #   get_ipython().run_line_magic('metric', ')')
    assert result.ret == 0


def test_lint_magics_blacklisted_cell(testdir):
    testdir.makeini(r"""
        [pytest]
        nbsmoke_flakes_cell_magics_blacklist = ruby
                                               bash
    """)
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"%%bash"})
    result = testdir.runpytest(*lint_args)
    result.stdout.re_match_lines_random([".*nbsmoke blacklisted magic: bash"])
    assert result.ret == 1


nb_hmm = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%bash\\n",
    "echo 1"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python",
   "pygments_lexer": "ipython3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
'''


# TODO: do for line also?
def test_lint_magics_blacklisted_cell_but_still_handle_cell(testdir):
    testdir.makeini(r"""
        [pytest]
        nbsmoke_flakes_cell_magics_blacklist = bash
    """)
    testdir.makefile('.ipynb', testing123=nb_hmm)
    result = testdir.runpytest(*lint_args)
    result.stdout.re_match_lines_random([".*nbsmoke blacklisted magic: bash"])
    # no error about the bash content, just that bash magics is present
    assert result.ret == 1

def test_lint_magics_blacklisted_line(testdir):
    testdir.makeini(r"""
        [pytest]
        nbsmoke_flakes_line_magics_blacklist = pylab
    """)
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"%pylab"})
    result = testdir.runpytest(*lint_args)
    result.stdout.re_match_lines_random([".*nbsmoke blacklisted magic: pylab"])    
    assert result.ret == 1
