#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys

settings = {
    'name': 'wsgi-ipware',
    'version': '0.0.1',
    'package': 'ipware',
    'description': ("A WSGI utility library that returns a client's real IP "
                    "address"),
    'url': 'https://github.com/rounds/wsgi-ipware',
    'author': 'Ami B',
    'author_email': 'ami@rounds.com',
    'license': 'BSD',
    'classifiers': (
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ),
    'py_modules': ['ipware']
}

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': settings['version']}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()

setup(**settings)
