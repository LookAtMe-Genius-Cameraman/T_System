#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Extension
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='t_system',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.9.835',
    description='t_system is an open source moving target locking system project via raspberry Pi embedded computer',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/LookAtMe-Genius-Cameraman/T_System',

    # Author details
    author='Cem Baybars GÜÇLÜ',
    author_email='cem.baybars@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Adaptive Technologies',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Intended language
        'Natural Language :: English',

        # Target Operating System
        'Operating System :: POSIX :: Linux',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3 :: Only',
    ],

    # What does your project relate to?
    keywords='machine vision tracking objects',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'picamera>=1.13',
        'RPi.GPIO>=0.6.5',
        'tinydb==3.9.0.post1',
        'numpy',
        'sympy',
        'paho-mqtt>=1.4.0',
        'face_recognition',
        'multipledispatch',
        'wireless',
        'netifaces',
        'psutil',
        'pyaccesspoint',
        'wifi',
        'flask',
        'flask-session',
        'flask-restful',
        'Flask-Testing',
        'schema',
        'gitpython',
        'elevate',
        'imutils',
        'gpiozero',
        'pyaudio',
        'requests',
        'pyroute2>=0.5.6',
        'pexpect',
        'opencv-python',
        'opencv-contrib-python',
        'dlib',
        'adafruit-blinka',
        'adafruit-circuitpython-pca9685',
        'adafruit-circuitpython-servokit',
        'tabulate',
        'cloudpickle',
        'dropbox'
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
       'optionals': [
           'flake8',
           'sphinx',
           'sphinx_rtd_theme',
           'recommonmark',
           'docutils',
           'm2r',
           'pytest',
           'pytest-cov==2.6.1',
           'coveralls==1.8.2'
       ]
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #    # If any package contains data files, include them:
    #    'ava': ['realhud/animation/*', 'sr/models/english/*']
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            't_system=t_system.__main__:initiate',
        ],
    }
)
