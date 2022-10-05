# -*- coding: utf-8 -*-

import os
import io
import sys
import shutil

from . import nb_basic, run_args, WARNINGS_ARE_ERRORS

# tests are run in subprocess because otherwise some state seems to be left
# around somewhere in jupyter (https://github.com/pyviz-dev/nbsmoke/issues/45)

# maybe this test is overkill now we check for certain output in the run tests?
def test_definitely_ran_paranoid(testdir):
    assert not os.path.exists('sigh')
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"open('x','w').write('y')"})
    # Suppress reporting test as failed when a warning is emitted,
    # due to ResourceWarning raised by pyzmq. This should be removed later.
    args = run_args.copy(); args.remove(WARNINGS_ARE_ERRORS)
    result = testdir.runpytest_subprocess(*args)
    assert result.ret==0
    with open('x','r') as f:
        assert f.read() == 'y'
    assert os.path.isfile('sigh')

def test_run_good(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/1"})
    # Suppress reporting test as failed when a warning is emitted,
    # due to ResourceWarning raised by pyzmq. This should be removed later.
    args = run_args.copy(); args.remove(WARNINGS_ARE_ERRORS)
    'dummy'
    result = testdir.runpytest_subprocess(*args)
    assert result.ret == 0
    result.stdout.re_match_lines_random(
        [".*collected 1 item$",
         ".*testing123.ipynb.*PASSED.*"])

def test_run_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/0"})
    # Suppress reporting test as failed when a warning is emitted,
    # due to ResourceWarning raised by pyzmq. This should be removed later.
    args = run_args.copy(); args.remove(WARNINGS_ARE_ERRORS)
    result = testdir.runpytest_subprocess(*args)
    assert result.ret == 1
    result.stdout.re_match_lines_random([".*ZeroDivisionError.*"])

def test_run_good_html(testdir):
    outhtml = os.path.join(testdir.tmpdir.strpath,'testing123.ipynb.html')
    assert not os.path.exists(outhtml)

    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"42"})

    args = run_args.copy(); args.remove(WARNINGS_ARE_ERRORS)
    args = args + ['--store-html=%s'%testdir.tmpdir.strpath]
    # nbconvert.HTMLExporter.from_notebook_node seems to be raising
    # a ResourceWarning that is caught by pytest and causes the test
    # to fail (the test suite fails if a warning is emitted). pytest
    # catches this kind of warning (unraisable) from Python 3.8.
    if sys.version_info >= (3, 8):
        args += ['-p', 'no:unraisableexception']
    result = testdir.runpytest_subprocess(*args)
    assert result.ret == 0

    # test that html has happened
    targets = [
        "<pre>42</pre>",
                                               # note: this is really what happens in a python2 notebook
        "<pre>&#39;中国&#39;</pre>" if sys.version_info[0]>=3 else r"<pre>u&#39;\u4e2d\u56fd&#39;</pre>"]
    answer = [None,None]

    with io.open(outhtml,encoding='utf8') as f:
        for line in f:
            for i,target in enumerate(targets):
                if target in line:
                    answer[i] = 42
    assert answer == [42,42]


def test_skip_run(testdir):
    testdir.makeini(r"""
        [pytest]
        nbsmoke_skip_run = ^.*skipme\.ipynb$
                           ^.*skipmetoo.*$
    """)
    testdir.makefile('.ipynb', skipme=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', alsoskipme=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmetoo=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmenot=nb_basic%{'the_source':"1/1"})
    # Suppress reporting test as failed when a warning is emitted,
    # due to ResourceWarning raised by pyzmq. This should be removed later.
    args = run_args.copy(); args.remove(WARNINGS_ARE_ERRORS)
    result = testdir.runpytest_subprocess(*args)
    assert result.ret == 0
    result.stdout.re_match_lines_random(
        [".*collected 4 items$",
         ".*alsoskipme.ipynb.*SKIPPED",
         ".*skipme.ipynb.*SKIPPED",
         ".*skipmenot.ipynb.*PASSED",
         ".*skipmetoo.ipynb.*SKIPPED"])

def test_cwd_like_jupyter_notebook(testdir):
    p = testdir.tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"import os; assert os.path.isfile('hello.txt')"})
    shutil.move('testing123.ipynb', 'sub')
    # Suppress reporting test as failed when a warning is emitted,
    # due to ResourceWarning raised by pyzmq. This should be removed later.
    args = run_args.copy(); args.remove(WARNINGS_ARE_ERRORS)
    result = testdir.runpytest_subprocess(*args)
    assert result.ret == 0
