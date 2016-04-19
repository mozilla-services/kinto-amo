#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()

requirements = [
    'kinto>=1.11.0',
    'kinto2xml',
]

test_requirements = [
    'mock',
    'unittest2',
    'webtest'
]

dependency_links = [
    'http://github.com/mozilla-services/kinto2xml/tarball/master#egg=kinto2xml-0.1.0.dev0'
]

setup(
    name='kinto-amo',
    version='0.1',
    description="AMO-style routing for Kinto - with XML",
    long_description=readme + '\n\n' + history,
    author="Mozilla",
    author_email='kinto@mozilla.org',
    url='https://github.com/mozilla-services/kinto-amo',
    packages=[
        'kinto_amo',
    ],
    package_dir={'kinto_amo':
                 'kinto_amo'},
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
    test_suite='tests',
    tests_require=test_requirements,
    dependency_links=dependency_links
)
