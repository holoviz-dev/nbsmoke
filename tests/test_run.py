# -*- coding: utf-8 -*-

import os
import io
import sys
import shutil

from . import nb_basic, run_args

# tests are run in subprocess because otherwise some state seems to be left
# around somewhere in jupyter (https://github.com/pyviz-dev/nbsmoke/issues/45)

# maybe this test is overkill now we check for certain output in the run tests?
def test_definitely_ran_paranoid(pytester):
    assert not os.path.exists('sigh')
    pytester.makefile('.ipynb', testing123=nb_basic%{'the_source':"open('x','w').write('y')"})
    result = pytester.runpytest_subprocess(*run_args)
    assert result.ret==0
    with open('x','r') as f:
        assert f.read() == 'y'
    assert os.path.isfile('sigh')

def test_run_good(pytester):
    pytester.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/1"})
    result = pytester.runpytest_subprocess(*run_args)
    assert result.ret == 0
    result.stdout.re_match_lines_random(
        [".*collected 1 item$",
         ".*testing123.ipynb.*PASSED.*"])

def test_run_bad(pytester):
    pytester.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/0"})
    result = pytester.runpytest_subprocess(*run_args)
    assert result.ret == 1
    result.stdout.re_match_lines_random([".*ZeroDivisionError.*"])

def test_run_good_html(pytester):
    outhtml = os.path.join(pytester.path,'testing123.ipynb.html')
    assert not os.path.exists(outhtml)

    pytester.makefile('.ipynb', testing123=nb_basic%{'the_source':"42"})

    result = pytester.runpytest_inprocess(*(run_args+['--store-html=%s'%pytester.path]))
    # result = pytester.runpytest_inprocess(*(run_args))
    assert result.ret == 0

    # test that html has happened
    targets = [
        "<pre>42</pre>",
                                               # note: this is really what happens in a python2 notebook
        "<pre>&#39;中国&#39;</pre>" if sys.version_info[0]==3 else r"<pre>u&#39;\u4e2d\u56fd&#39;</pre>"]
    answer = [None,None]

    with io.open(outhtml,encoding='utf8') as f:
        for line in f:
            for i,target in enumerate(targets):
                if target in line:
                    answer[i] = 42
    assert answer == [42,42]


def test_skip_run(pytester):
    pytester.makeini(r"""
        [pytest]
        nbsmoke_skip_run = ^.*skipme\.ipynb$
                           ^.*skipmetoo.*$
    """)
    pytester.makefile('.ipynb', skipme=nb_basic%{'the_source':"1/0"})
    pytester.makefile('.ipynb', alsoskipme=nb_basic%{'the_source':"1/0"})
    pytester.makefile('.ipynb', skipmetoo=nb_basic%{'the_source':"1/0"})
    pytester.makefile('.ipynb', skipmenot=nb_basic%{'the_source':"1/1"})
    result = pytester.runpytest_subprocess(*run_args)
    assert result.ret == 0
    result.stdout.re_match_lines_random(
        [".*collected 4 items$",
         ".*alsoskipme.ipynb.*SKIPPED",
         ".*skipme.ipynb.*SKIPPED",
         ".*skipmenot.ipynb.*PASSED",
         ".*skipmetoo.ipynb.*SKIPPED"])

def test_cwd_like_jupyter_notebook(pytester):
    p = pytester.mkdir("sub") / "hello.txt"
    p.touch()
    p.write_text("content")
    pytester.makefile('.ipynb', testing123=nb_basic%{'the_source':"import os; assert os.path.isfile('hello.txt')"})
    shutil.move('testing123.ipynb', 'sub')
    result = pytester.runpytest_subprocess(*run_args)
    assert result.ret == 0
