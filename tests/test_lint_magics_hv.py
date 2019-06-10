nb_hv_good = u'''
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
    "from holoviews.operation.datashader import datashade, regrid"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%opts RGB [invert_yaxis=True width=400 height=400]\\n",
    "%opts HeatMap (cmap='Winter') [colorbar=True, toolbar='random']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%opts HeatMap (cmap='Summer') [colorbar=True, toolbar='above']\\n",
    "%opts HeatMap (cmap='Summer') [colorbar=True, toolbar='blinking']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%opts RGB [invert_yaxis=True width=400 height=400]\\n",
    "adim = hv.Dimension('A')\\n",
    "bdim = hv.Dimension('B')\\n",
    "paths = [os.path.join('data', f) for f in ['a','b']]\\n",
    "hv.Layout([datashade(hv.Curve(p, kdims=[adim], vdims=[bdim])) for p in paths]).cols(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%opts Image [width=500 height=500 colorbar=True colorbar_position='left' logz=True]\\n",
    "%%opts Image [xticks=[1,2] yticks=[2,3]] (cmap='viridis')\\n",
    "%%opts HLine (color='red' line_width=2) VLine (color='red', line_width=2)\\n",
    "im = hv.Image({'a':1, 'b':2, 'c':3}, kdims=[adim, bdim], \\n",
    "              vdims=[hv.Dimension('c')])\\n",
    "regrid(im) * regrid(im)"
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

nb_hv_bad = u'''
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
    "%%opts RGB [invert_yaxis=True width=400 height=400]\\n",
    "adim = hv.Dimension('A')\\n",
    "bdim = hv.Dimension('B')\\n",
    "paths = [os.path.join('data', f) for f in ['a','b']]\\n",
    "hv.Layout([datashade(hv.Curve(no, kdims=[adim], vdims=[bdim])) for p in paths]).cols(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%opts Image [width=500 height=500 colorbar=True colorbar_position='left' logz=True]\\n",
    "%%opts Image [xticks=xticks yticks=yticks] (cmap='viridis')\\n",
    "%%opts HLine (color='red' line_width=2) VLine (color='red', line_width=2)\\n",
    "im = hv.Image({'a':a, 'b':b}, kdims=['a'], \\n",
    "              vdims=[hv.Dimension('b')])\\n",
    "regrid(im) * lines(no)"
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
nb_cell_and_line = u'''
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
    "%%%%opts HLine (color='red' line_width=2) VLine (color='red', line_width=2)\\n",
    "%%%%opts RGB [invert_yaxis=True width=400 height=400]\\n",
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

nb_bad_opts_syntax = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import holoviews as hv"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%opts RGB bad syntax is bad [invert_yaxis=True width=400 height=400]\\n",
    "hv.Dimension('B')"
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

nb_bad_opts_syntax2 = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import holoviews as hv"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%opts RGB [invert_yaxis=True width=400 height=400]should not be here\\n",
    "hv.Dimension('B')"
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


def test_lint_magics_hv_good(testdir):
    # TODO: right now just that it hasn't caused errors, but should
    # check there's content + noqa in there
    testdir.makefile('.ipynb', testing123=nb_hv_good)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 0
    assert 'warnings' not in result.parseoutcomes()

def test_lint_magics_hv_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_hv_bad)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    result.stdout.re_match_lines_random(
        [".*undefined name 'no'$",
         ".*undefined name 'a'$",
         ".*undefined name 'b'$",
         ".*undefined name 'regrid'$",
         ".*undefined name 'lines'$",
         ".*undefined name 'no'$"])
    assert result.ret == 1

def test_lint_magics_hv_cell_and_line_good(testdir):
    testdir.makefile('.ipynb', testing123=nb_cell_and_line%{'dim_name':'adim'})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 0
    assert 'warnings' not in result.parseoutcomes()

def test_lint_magics_hv_cell_and_line_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_cell_and_line%{'dim_name':'bad_name'})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    result.stdout.re_match_lines_random(
        [".*undefined name 'adim'$"])
    assert result.ret == 1
    assert 'warnings' not in result.parseoutcomes()

def test_lint_magics_hv_bad_opts_syntax(testdir):
    testdir.makefile('.ipynb', testing123=nb_bad_opts_syntax)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 1
    result.stdout.re_match_lines_random(
        ["^E.*SyntaxError: Invalid specification syntax.$"])
    assert 'warnings' not in result.parseoutcomes()

def test_lint_magics_hv_bad_opts_syntax2(testdir):
    testdir.makefile('.ipynb', testing123=nb_bad_opts_syntax2)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 1
    result.stdout.re_match_lines_random(
        ["^E.*SyntaxError: Failed to parse remainder of string: 'should not be here'"])
    assert 'warnings' not in result.parseoutcomes()
