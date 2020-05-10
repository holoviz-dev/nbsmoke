# -*- coding: utf-8 -*-

import sys
import os
import codecs
from setuptools import setup, find_packages

import version

def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()

extras_require = {
    'run-checks': ['nbval'],
    'holoviews-magics': ['holoviews'],
    'verify': ['requests', 'beautifulsoup4'],
}

setup_args = dict(
    name='nbsmoke',
    description='Static checking of Jupyter notebooks.',
    version = version.get_setup_version('nbsmoke'),
    url='https://github.com/pyviz-dev/nbsmoke',
    long_description=read('README.rst'),    
    author='pyviz-dev contributors',
    author_email = "developers@holoviz.org",
    license='BSD-3',
    packages=find_packages(),
    include_package_data = True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    python_requires = ">=2.7",    
    install_requires=[
        'pytest >=3.1.1',
        ########## lint stuff
        'pyflakes',
        ########## notebook stuff
        # * Required imports: nbconvert, nbformat.
        # * Optional: process ipython magics (required import: IPython)
        'nbformat',
        'nbconvert'],
    extras_require = extras_require,
    entry_points={
        'pytest11': [
            'nbsmoke = nbsmoke',
        ],
    },
)

setup_args['extras_require']['all'] = sorted(set(sum(extras_require.values(), [])))

if __name__=="__main__":
    setup(**setup_args)
