# -*- coding: utf-8 -*-

# Note: declare this here instead of in conftest.py because
# running `coverage run pytest` fails when the tests dir is
# a subdir of nbsmoke.
pytest_plugins = 'pytester'

# note: magics in here just to check they do not directly cause
# errors.

nb_basic = u'''
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

WARNINGS_ARE_ERRORS = '-W error'
VERBOSE = '-v'
# Ignore deprecation warnings until the many deprecation warnings stop
# coming from ipython and traitlets as used by nbconvert
IGNORE_DEPRECATION_WARNINGS = '-W ignore::DeprecationWarning'

_all_args = [
    VERBOSE,
    WARNINGS_ARE_ERRORS,
    IGNORE_DEPRECATION_WARNINGS
]


lint_args = ['--nbsmoke-lint'] + _all_args

run_args = ['--nbsmoke-run'] + _all_args
