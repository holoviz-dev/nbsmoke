# -*- coding: utf-8 -*-

import os
import io
import sys
import shutil


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'nbsmoke:',
        '*--nbsmoke-run*',
        '*--nbsmoke-lint*',
        '*--store-html*'
    ])


def test_cell_timeout_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        cell_timeout = 300
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def cell_timeout(request):
            return request.config.getini('cell_timeout')

        def test_cell_timeout(cell_timeout):
            assert int(cell_timeout) == 300
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_cell_timeout PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0



    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def cell_timeout(request):
            return request.config.getini('cell_timeout')

        def test_cell_timeout(cell_timeout):
            assert int(cell_timeout) == 300
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_cell_timeout PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

_nb = u'''
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%(the_source)s"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%env"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%%%%writefile sigh\\n",
    "1"
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

_nb2 = u'''
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
    "%%%%opts RGB [invert_yaxis=True width=400 height=400]\\n",
    "adim = hv.Dimension('A')\\n",
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


def test_definitely_ran_paranoid(testdir):
    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"open('x','w').write('y')"})
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 0
    with open('x','r') as f:
        assert f.read() == 'y'
    assert os.path.isfile('sigh')

def test_rungood(testdir):
    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"1/1"})
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 0

def test_runbad(testdir):
    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"1/0"})
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 1

def test_rungood_html(testdir):
    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"42"})

    result = testdir.runpytest(
        '--nbsmoke-run',
        '--store-html=%s'%testdir.tmpdir.strpath,
        '-v')
    assert result.ret == 0

    # test that html has happened
    targets = [
        "<pre>42</pre>",
                                               # note: this is really what happens in a python2 notebook
        "<pre>&#39;中国&#39;</pre>" if sys.version_info[0]==3 else r"<pre>u&#39;\u4e2d\u56fd&#39;</pre>"]
    answer = [None,None]
    x = os.path.join(testdir.tmpdir.strpath,'testing123.ipynb.html')
    with io.open(x,encoding='utf8') as f:
        for line in f:
            for i,target in enumerate(targets):
                if target in line:
                    answer[i] = 42
    assert answer == [42,42]

def test_lintgood(testdir):
    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"1/1"})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 0

def test_lintextra(testdir):
    testdir.makefile('.ipynb', testing123=_nb2)
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 0

def test_lintbad(testdir):
    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"1/1 these undefined names are definitely undefined"})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 1

def test_it_is_nbfile(testdir):
    testdir.makeini("""
        [pytest]
        it_is_nb_file = ^.*\.something$
    """)

    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"1/0"})
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 5

def test_skip_run(testdir):
    testdir.makeini("""
        [pytest]
        skip_run = ^.*skipme\.ipynb$
                   ^.*skipmetoo.*$
    """)

    testdir.makefile('.ipynb', skipme=_nb%{'the_source':"1/0"})
    testdir.makefile('.ipynb', alsoskipme=_nb%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmetoo=_nb%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmenot=_nb%{'the_source':"1/1"})

    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 0


def test_cwd_like_jupyter_notebook(testdir):
    p = testdir.tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    testdir.makefile('.ipynb', testing123=_nb%{'the_source':"import os; assert os.path.isfile('hello.txt')"})
    shutil.move('testing123.ipynb', 'sub')
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 0
