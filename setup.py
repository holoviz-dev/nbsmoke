#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages

import version


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup_args = dict(
    name='nbsmoke',
    description='Basic notebook checks. Do they run? Do they contain lint?',
    version = version.get_setup_version('nbsmoke'),
    url='https://github.com/pyviz/nbsmoke',
    long_description=read('README.rst'),    
    author='pyviz contributors',
    author_email = "dev@pyviz.org",
    license='BSD-3',
    packages=find_packages(),
    include_package_data = True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    
    python_requires = ">=2.7",
    
    install_requires=[
        'pytest >=3.1.1',
        'jupyter_client',
        'ipykernel',
        'nbformat',
        'nbconvert',
        'pyflakes',
        'requests',
        'beautifulsoup4'
    ],
    
    entry_points={
        'pytest11': [
            'nbsmoke = nbsmoke',
        ],
    },
)

if __name__=="__main__":
    setup(**setup_args)
