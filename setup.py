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
        ########## notebook stuff (reading, executing)
        # * Required imports: nbconvert, nbformat.
        # * Need to be able to execute ipython notebooks.
        # * Optional: process ipython magics (required import: IPython)
        'jupyter_client ==6.1.3',
        'nbformat',
        'nbconvert',
    # TODO: I think the decision was to go with python/setup.py for this stuff,
    # right? (but if so, how do I specify it's the runtime python version
    # I'm talking aobut, not the buildtime python version?)
    # Also - not sure exactly what is required now
    ] + (['ipykernel'] if (sys.version_info[0]>=3 and sys.version_info[1]>4) else ['ipykernel <5']),
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
