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
    'holoviews-magics': ['holoviews'],
    'verify': ['requests', 'beautifulsoup4'],
}

setup_args = dict(
    name='nbsmoke',
    description='Basic notebook checks. Do they run? Do they contain lint?',
    version = version.get_setup_version('nbsmoke'),
    url='https://github.com/pyviz-dev/nbsmoke',
    long_description=read('README.rst'),    
    author='pyviz contributors',
    author_email = "dev@pyviz.org",
    license='BSD-3',
    packages=find_packages(),
    include_package_data = True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    
    python_requires = ">=3.4",
    
    install_requires=[
        'pytest >=3.1.1',
        ########## lint stuff
        'pyflakes',
        ########## notebook stuff (reading, executing)
        # * Required imports: nbconvert, nbformat.
        # * Need to be able to execute ipython notebooks.
        # * Optional: process ipython magics (required import: IPython)
        'jupyter_client',
        'nbformat',
        'nbconvert <6',
        'ipykernel',
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
