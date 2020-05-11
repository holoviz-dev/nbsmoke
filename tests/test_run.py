# -*- coding: utf-8 -*-

# TODO: run is deprecated - will be able to remove when --nbsmoke-run
# is removed.

import os
import shutil

from . import nb_basic, run_args

# maybe this test is overkill now we check for certain output in the run tests?
def test_definitely_ran_paranoid(testdir):
    assert not os.path.exists('sigh')
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"open('x','w').write('y')"})
    result = testdir.runpytest(*run_args)
    assert result.ret==0
    with open('x','r') as f:
        assert f.read() == 'y'
    assert os.path.isfile('sigh')

def test_run_good(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/1"})
    result = testdir.runpytest(*run_args)
    assert result.ret == 0
    result.stdout.re_match_lines_random(
        [".*collected 4 items$",
         ".*testing123::ipynb::Cell 0 PASSED.*",
         ".*testing123::ipynb::Cell 1 PASSED.*",
         ".*testing123::ipynb::Cell 2 PASSED.*",
         ".*testing123::ipynb::Cell 3 PASSED.*",
        ])

def test_run_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/0"})
    result = testdir.runpytest(*run_args)
    assert result.ret == 1
    result.stdout.re_match_lines_random([".*ZeroDivisionError.*"])

def test_skip_run(testdir):
    testdir.makeconftest("""
    import pytest
    import re
    
    skip_patterns = [".*skipme\.ipynb.*",
                     ".*skipmetoo.*"]
    
    def pytest_runtest_setup(item):
        for pattern in skip_patterns:
            if re.match(pattern, item.nodeid):
                pytest.skip("Skipped by conftest")
                break
    """)

    testdir.makefile('.ipynb', skipme=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', alsoskipme=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmetoo=nb_basic%{'the_source':"1/0"})
    testdir.makefile('.ipynb', skipmenot=nb_basic%{'the_source':"1/1"})
    result = testdir.runpytest(*run_args)
    assert result.ret == 0
    result.stdout.re_match_lines_random(
        [".*collected 16 items$",
         ".*alsoskipme::ipynb.*SKIPPED",
         ".*alsoskipme::ipynb::Cell 1 SKIPPED",
         ".*alsoskipme::ipynb::Cell 2 SKIPPED",
         ".*alsoskipme::ipynb::Cell 3 SKIPPED",
         ".*skipme::ipynb::Cell 0 SKIPPED",
         ".*skipme::ipynb::Cell 1 SKIPPED",
         ".*skipme::ipynb::Cell 2 SKIPPED",
         ".*skipme::ipynb::Cell 3 SKIPPED",         
         ".*skipmenot::ipynb::Cell 0 PASSED",
         ".*skipmenot::ipynb::Cell 1 PASSED",
         ".*skipmenot::ipynb::Cell 2 PASSED",
         ".*skipmenot::ipynb::Cell 3 PASSED",         
         ".*skipmetoo::ipynb::Cell 0 SKIPPED",
         ".*skipmetoo::ipynb::Cell 1 SKIPPED",
         ".*skipmetoo::ipynb::Cell 2 SKIPPED",
         ".*skipmetoo::ipynb::Cell 3 SKIPPED"])

def test_cwd_like_jupyter_notebook(testdir):
    p = testdir.tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"import os; assert os.path.isfile('hello.txt')"})
    shutil.move('testing123.ipynb', 'sub')
    result = testdir.runpytest(*run_args)
    assert result.ret == 0
