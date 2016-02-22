"""
setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='broom',

    version='1.0.3',

    description='A collector journal',
    long_description=long_description,

    url='https://github.com/banzhang/broom',

    # Author details
    author='chunshiban',
    author_email='banzhang@chunshiban.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    keywords='collect application log file from application server to log server',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['pexpect', 'pyinotify', 'argparse'],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
        'client':['broom/skel/broom.conf'],
        'server':['broom/skel/broomd']
    },

    data_files=[],

    entry_points={
        'console_scripts': [
            'broom=broom:main',
            'broomd=broom:server',
        ],
    },
)
