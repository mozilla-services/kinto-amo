#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

with codecs.open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    history = f.read()

requirements = [
    'kinto>=1.11.0',
    'amo2kinto',
]

test_requirements = [
    'mock',
    'pytest',
    'unittest2',
    'webtest'
]


setup(
    name='kinto-amo',
    version='0.2.0',
    description="AMO-style routing for Kinto - with XML",
    long_description=readme + '\n\n' + history,
    author="Mozilla",
    author_email='kinto@mozilla.org',
    url='https://github.com/mozilla-services/kinto-amo',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="Apache License (2.0)",
    zip_safe=False,
    keywords='kinto',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='kinto_amo.tests',
    tests_require=test_requirements,
)
