# -*- coding: utf-8 -*-

import os
import io
import sys
import shutil

from . import nb_basic

# TODO: many of these functions should do "assert 'warnings' not in
# result.parseoutcomes()" but can't because of warnings from
# underlying stack, e.g.
#   DeprecationWarning: KernelManager._kernel_name_changed is deprecated in traitlets 4.1: use @observe and @unobserve instead.', '    def _kernel_name_changed(self, name, old, new)

# maybe this test is overkill now we check for certain output in the run tests?
def test_definitely_ran_paranoid(testdir):
    assert not os.path.exists('sigh')
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"open('x','w').write('y')"})
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 0
    with open('x','r') as f:
        assert f.read() == 'y'
    assert os.path.isfile('sigh')

def test_run_good(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/1"})
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 0
    result.stdout.re_match_lines_random(
        [".*collected 1 item$",
         ".*testing123.ipynb.*PASSED.*"])

def test_run_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/0"})
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 1
    result.stdout.re_match_lines_random([".*ZeroDivisionError.*"])

def test_run_good_html(testdir):
    outhtml = os.path.join(testdir.tmpdir.strpath,'testing123.ipynb.html')
    assert not os.path.exists(outhtml)

    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"42"})

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

    with io.open(outhtml,encoding='utf8') as f:
        for line in f:
            for i,target in enumerate(targets):
                if target in line:
                    answer[i] = 42
    assert answer == [42,42]


def test_skip_run(testdir):
    testdir.makeini("""
        [pytest]
        nbsmoke_skip_run = ^.*skipme\.ipynb$
                           ^.*skipmetoo.*$
    """)
    testdir.makefile('.ipynb', skipme=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', alsoskipme=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmetoo=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmenot=nb_basic%{'the_source':"1/1"})
    result = testdir.runpytest('--nbsmoke-run','-v')
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
    result = testdir.runpytest('--nbsmoke-run','-v')
    assert result.ret == 0
