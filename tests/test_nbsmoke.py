# -*- coding: utf-8 -*-

from . import nb_basic

def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    result.stdout.fnmatch_lines([
        'nbsmoke:',
        '*--nbsmoke-lint*',
        '*--nbsmoke-lint-debug*',        
        '*--nbsmoke-lint-onlywarn*',
        '*--nbsmoke-verify*',
        '*--nbsmoke-run*',
        '*--ignore-nbsmoke-skip-run*',        
    ])


def test_nbsmoke_cell_timeout_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        nbsmoke_cell_timeout = 123
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def nbsmoke_cell_timeout(request):
            return request.config.getini('nbsmoke_cell_timeout')

        def test_nbsmoke_cell_timeout(nbsmoke_cell_timeout):
            assert int(nbsmoke_cell_timeout) == 123
    """)

    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*::test_nbsmoke_cell_timeout PASSED*',
    ])

    assert result.ret == 0
