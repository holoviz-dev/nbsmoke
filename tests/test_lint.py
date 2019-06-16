# -*- coding: utf-8 -*-

import os

from . import nb_basic, WARNINGS_ARE_ERRORS, lint_args

def test_lint_good(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/1"})
    result = testdir.runpytest(*lint_args)
    assert result.ret == 0

def test_lint_bad_syntax(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/1 these undefined names are a syntax error"})
    result = testdir.runpytest(*lint_args)
    assert result.ret == 1
    assert result.parseoutcomes()['failed'] == 1
    result.stdout.re_match_lines_random(
        [".*invalid syntax.*",
         ".*1/1 these undefined names are a syntax error.*"])

def test_lint_bad(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"undefined_name"})
    result = testdir.runpytest(*lint_args)
    assert result.ret == 1
    assert result.parseoutcomes()['failed'] == 1
    result.stdout.re_match_lines_random(
        [".*undefined name 'undefined_name'.*",
         ".*To see python source that was checked by pyflakes.*pass --nbsmoke-lint-debug$",
         ".*To see python source before magics were handled by nbsmoke.*pass --nbsmoke-lint-debug$"])


def test_lint_bad_silenced_with_noqa(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"undefined # noqa: deliberate :)"})
    result = testdir.runpytest('--nbsmoke-lint','-v')
    assert result.ret == 0

def test_lint_bad_onlywarn(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"1/1 these undefined names are definitely undefined"})
    _args = lint_args.copy()
    _args.remove(WARNINGS_ARE_ERRORS)
    _args.append("--nbsmoke-lint-onlywarn")
    result = testdir.runpytest(*_args)
    assert result.ret == 0
    assert result.parseoutcomes()['warnings'] == 1
    result.stdout.re_match_lines_random(
        [".*invalid syntax.*",
         ".*1/1 these undefined names are definitely undefined.*"])


def test_lint_bad_debug(testdir):
    testdir.makefile('.ipynb', testing123=nb_basic%{'the_source':"undefined_name"})
    result = testdir.runpytest(*(lint_args + ['--nbsmoke-lint-debug']))
    assert result.ret == 1
    assert result.parseoutcomes()['failed'] == 1
    result.stdout.re_match_lines_random(
        [".*undefined name 'undefined_name'.*",
         ".*To see python source that was checked by pyflakes.*testing123.nbsmoke-debug-postmagicprocess.py$",
         ".*To see python source before magics were handled by nbsmoke.*testing123.nbsmoke-debug-premagicprocess.py$"])
    assert os.path.isfile("testing123.nbsmoke-debug-premagicprocess.py")
    assert os.path.isfile("testing123.nbsmoke-debug-postmagicprocess.py")
