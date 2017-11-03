#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup

import versioneer


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-nbsmoke',
    version=versioneer.get_version(),
    author='Marimo',
    license='BSD-3',
    url='https://github.com/ioam/pytest-nbsmoke',
    description='Basic notebook checks. Do they run? Do they contain lint?',
    long_description=read('README.rst'),
    py_modules=['pytest_nbsmoke'],
    install_requires=['pytest>=3.1.1',
                      'jupyter_client',
                      'ipykernel',
                      'nbformat',
                      'nbconvert',
                      'pyflakes'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'pytest11': [
            'nbsmoke = pytest_nbsmoke',
        ],
    },
)
