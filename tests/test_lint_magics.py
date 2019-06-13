# -*- coding: utf-8 -*-

from . import assert_success

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



def test_lint_magics_nowarn(testdir):
    # there should be no warnings for a variety of magics
    # TODO break this test up into more specific ones?
    testdir.makefile('.ipynb', testing123=nb_variety_of_magics)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert_success(result)

def test_lint_line_magics_good(testdir):
    # line magic with one arg
    testdir.makefile('.ipynb', testing123=nb_line_magic%{'prefix':''})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert_success(result)

def test_lint_line_magics_bad(testdir):
    # line magic with undefined name
    testdir.makefile('.ipynb', testing123=nb_line_magic%{'prefix':'bad'})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 1
    result.stdout.re_match_lines_random([".*undefined name 'badf'$"])

def test_lint_line_magics_with_cell_magics_good(testdir):
    testdir.makefile('.ipynb', testing123=nb_cell_and_line_magics%{'dim_name':'adim'})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert_success(result)

def test_lint_line_magics_with_cell_magics_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_cell_and_line_magics%{'dim_name':'bad_name'})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    result.stdout.re_match_lines_random(
        [".*undefined name 'adim'$"])
    assert result.ret == 1

def test_lint_line_magics_with_skipped_cell_magics_bad(testdir):
    # when omitting cell magic, make sure rest of cell is not also omitted
    testdir.makefile('.ipynb', testing123=nb_cell_skipped_and_line_magics%{'dim_name':'bad_name'})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    result.stdout.re_match_lines_random(
        [".*undefined name 'adim'$"])
    assert result.ret == 1

def test_lint_magics_skip_warn_about_zero_arg(testdir):
    testdir.makefile('.ipynb', testing123=nb_unhandled_magics%{'magic_arg':''})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert_success(result)

def test_lint_magics_warn_about_unhandled(testdir):
    testdir.makefile('.ipynb', testing123=nb_unhandled_magics%{'magic_arg':'arg'})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 0
    assert result.parseoutcomes()['warnings'] == 4
    result.stdout.re_match_lines_random(
        [".*nbsmoke doesn't know how to process the.*cellmagicnonexistent.*magic and has ignored it.*",
         ".*nbsmoke doesn't know how to process the.*linemagicnonexistent.*magic and has ignored it.*",
         ".*nbsmoke doesn't know how to process the.*cellmagicnonexistenttwo.*magic and has ignored it.*",
         ".*nbsmoke doesn't know how to process the.*cellmagicnonexistentthree.*magic and has ignored it.*"])

def test_optional_import_warn(testdir):
    testdir.makefile('.ipynb', testing123=nb_optional_dep)
    ###
    # what a hack
    import nbsmoke.lint.magics as M
    from collections import namedtuple
    M.other_magic_handlers['clever_magic'] = M._Unavailable(namedtuple("SomeError", "msg")("A terrible error."))
    ###
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 1
    assert 'warnings' not in result.parseoutcomes()
    result.stdout.re_match_lines_random(
        [".*Exception: nbsmoke can't process the following 'clever_magic' magic without additional dependencies.*",
         ".*A terrible error.*"])


def test_lint_line_magics_indent(testdir):
    testdir.makefile('.ipynb', testing123=nb_lint_line_magic_indent)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert_success(result)

def test_lint_cell_line_magics_indent(testdir):
    testdir.makefile('.ipynb', testing123=nb_lint_cell_line_magic_indent)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert_success(result)

def test_magics_detection(testdir):
    # if you were to parse ipython stuff line by line, you might mistake
    # things for magics, e.g.
    #   'some %s'
    #   %variable
    testdir.makefile('.ipynb', testing123=nb_lint_is_it_magic)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    # if falsely detecting magic, the "pass" that gets inserted for
    # the unknown magic would be a syntax error
    #
    # also, the following should not be present (would be warned about
    # as unknown magic)
    #   get_ipython().run_line_magic('metric', ')')
    assert_success(result)
