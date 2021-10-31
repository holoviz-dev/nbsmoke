# -*- coding: utf-8 -*-

import os
import codecs
import json
from setuptools import setup, find_packages


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    try:
        from param import version
    except Exception:
        version = None
    if version is not None:
        return version.Version.setup_version(basepath, reponame, archive_commit="$Format:%h$")
    else:
        print("WARNING: param>=1.6.0 unavailable. If you are installing a package, "
              "this warning can safely be ignored. If you are creating a package or "
              "otherwise operating in a git repository, you should install param>=1.6.0.")
        return json.load(open(version_file_path, 'r'))['version_string']


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()

extras_require = {
    'holoviews-magics': ['holoviews'], # only install if you are using holoviews magics (which are deprecated...)
    'verify': ['requests', 'beautifulsoup4'],
    # until pyproject.toml/equivalent is widely supported (setup_requires
    # doesn't work well with pip)
    'build': [
        'param>=1.7.0',
        'pyct>=0.4.4',
        'setuptools>=30.3.0',
    ],
    'lint': ['flake8'],
    'tests': [
        'coverage',
        'twine',   # required for pip packaging
        'rfc3986', # required by twine
        'keyring', # required by twine
    ],
}

extras_require['tests'] += extras_require['lint']
extras_require['tests'] += extras_require['holoviews-magics']
extras_require['tests'] += extras_require['verify']

setup_args = dict(
    name='nbsmoke',
    description='Basic notebook checks. Do they run? Do they contain lint?',
    version = get_setup_version('nbsmoke'),
    url='https://github.com/pyviz-dev/nbsmoke',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
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
        'param>=1.7.0',
        'pytest>=3.1.1',
        ########## lint stuff
        'pyflakes',
        ########## notebook stuff (reading, executing)
        # * Required imports: nbconvert, nbformat.
        # * Need to be able to execute ipython notebooks.
        # * Optional: process ipython magics (required import: IPython)
        'jupyter_client',
        'nbformat',
        'nbconvert',
        'ipykernel'],
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
